import urllib.parse
from asyncio import TimeoutError
from aiohttp import ClientSession, TCPConnector, ClientError
from async_lru import alru_cache

from src.common.backoff import backoff
from src.infrastructure.config import config
from src.infrastructure.logger import logger

TIMEOUT = .5


class ServerError(Exception):
    ...


class OKXPageProvider:
    def __init__(self):
        headers = {'user-agent': config.USER_AGENT}
        self._session = ClientSession(
            connector=TCPConnector(limit_per_host=config.LIMIT_RPS),
            headers=headers
        )

    @alru_cache(maxsize=100)
    @backoff(3, (ClientError, TimeoutError, ServerError), timeout=TIMEOUT)
    async def get_page_by_number(self, page_number: int) -> str:
        url = 'https://www.okx.com/help/section/announcements-latest-announcements/page/{page_num}'
        url = url.format(page_num=page_number)

        resp = await self._session.get(url=url)
        if resp.status >= 500:
            raise ServerError(f'External Server: {resp.content[:200]}')
        resp.raise_for_status()
        logger.debug(f'loaded {url}')
        return await resp.text()

    async def get_main_page(self):
        return await self.get_page_by_number(1)

    @alru_cache(maxsize=100)
    @backoff(3, (ClientError, TimeoutError, ServerError))
    async def get_news_page_by_url(self, url: str) -> str:
        _url = 'https://www.okx.com/'
        url = urllib.parse.urljoin(_url, url)

        resp = await self._session.get(url=url)
        if resp.status >= 500:
            raise ServerError(f'External Server: {resp.content[:200]}')
        resp.raise_for_status()
        logger.debug(f'loaded {url}')
        return await resp.text()
