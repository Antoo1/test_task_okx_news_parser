import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from aiohttp import ClientResponse, ClientError
from src.domain.page_provider import OKXPageProvider, ServerError
import urllib.parse


@pytest.fixture
def mock_session():
    return AsyncMock()


@pytest.fixture
async def page_provider(mock_session):
    session = AsyncMock()
    session.__aenter__.return_value = mock_session

    with patch('aiohttp.ClientSession', return_value=session):
        provider = OKXPageProvider()
        provider._session = session  # Replace the session with our mock
        return provider


class TestGetPageByNumber:
    async def test_success(self, page_provider, mock_session):
        page_num = 2
        expected_url = f'https://www.okx.com/help/section/announcements-latest-announcements/page/{page_num}'
        expected_content = "<html>Test content</html>"

        mock_response = AsyncMock(spec=ClientResponse)
        mock_response.status = 200
        mock_response.text.return_value = expected_content
        mock_session.get.return_value = mock_response

        result = await page_provider.get_page_by_number(page_num)

        mock_session.get.assert_called_once_with(url=expected_url)
        assert result == expected_content

    async def test_server_error(self, page_provider, mock_session):
        page_num = 3
        mock_response = AsyncMock(spec=ClientResponse)
        mock_response.status = 500
        mock_response.content.read.return_value = b"Server error"
        mock_session.get.return_value = mock_response

        with pytest.raises(ServerError):
            await page_provider.get_page_by_number(page_num)

    async def test_client_error_retry(self, page_provider, mock_session):
        page_num = 4
        mock_session.get.side_effect = [ClientError("First error"), ClientError("Second error")]

        mock_response = AsyncMock(spec=ClientResponse)
        mock_response.status = 200
        mock_response.text.return_value = "Success after retry"
        mock_session.get.side_effect = [
            ClientError("First error"),
            ClientError("Second error"),
            mock_response
        ]

        result = await page_provider.get_page_by_number(page_num)

        assert mock_session.get.call_count == 3
        assert result == "Success after retry"

    @pytest.mark.asyncio
    async def test_cache_works(self, page_provider, mock_session):
        page_num = 5
        expected_content = "<html>Cached content</html>"

        mock_response = AsyncMock(spec=ClientResponse)
        mock_response.status = 200
        mock_response.text.return_value = expected_content
        mock_session.get.return_value = mock_response

        result1 = await page_provider.get_page_by_number(page_num)

        result2 = await page_provider.get_page_by_number(page_num)

        mock_session.get.assert_called_once()  # Only called once due to caching
        assert result1 == expected_content
        assert result2 == expected_content


class TestGetNewsPageByUrl:
    async def test_success(self, page_provider, mock_session):
        relative_url = "/help/article/123"
        full_url = urllib.parse.urljoin("https://www.okx.com/", relative_url)
        expected_content = "<html>News content</html>"

        mock_response = AsyncMock(spec=ClientResponse)
        mock_response.status = 200
        mock_response.text.return_value = expected_content
        mock_session.get.return_value = mock_response

        result = await page_provider.get_news_page_by_url(relative_url)

        mock_session.get.assert_called_once_with(url=full_url)
        assert result == expected_content

    async def test_absolute_url(self, page_provider, mock_session):
        absolute_url = "https://www.okx.com/help/article/123"
        expected_content = "<html>News content</html>"

        mock_response = AsyncMock(spec=ClientResponse)
        mock_response.status = 200
        mock_response.text.return_value = expected_content
        mock_session.get.return_value = mock_response

        result = await page_provider.get_news_page_by_url(absolute_url)

        mock_session.get.assert_called_once_with(url=absolute_url)
        assert result == expected_content
