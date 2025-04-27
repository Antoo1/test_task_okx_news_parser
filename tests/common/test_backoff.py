from unittest.mock import patch, AsyncMock

import pytest

from src.common.backoff import backoff


class TemporaryError(Exception):
    """Исключение, при котором нужно повторять попытку."""
    pass

class PermanentError(Exception):
    """Исключение, при котором повторять не нужно."""
    pass

# Счетчик вызовов для тестовых функций
call_counter = 0

@pytest.fixture(autouse=True)
def reset_counter():
    """Сбрасывает счетчик перед каждым тестом."""
    global call_counter
    call_counter = 0


@pytest.fixture
def mock_sleep():
    mock = AsyncMock()
    with patch('asyncio.sleep', mock):
        yield mock

async def test_success_first_try(mock_sleep):
    global call_counter

    @backoff(retry_count=3, exceptions=(TemporaryError,))
    async def my_func():
        global call_counter
        call_counter += 1
        return "Success"

    result = await my_func()

    assert result == "Success"
    assert call_counter == 1
    mock_sleep.assert_not_called()

@pytest.mark.asyncio
async def test_retry_and_succeed(mock_sleep):
    global call_counter

    @backoff(retry_count=3, exceptions=(TemporaryError,))
    async def fail_once_then_succeed():
        global call_counter
        call_counter += 1
        if call_counter == 1:
            raise TemporaryError("First attempt failed")
        return "Success after retry"

    result = await fail_once_then_succeed()

    assert result == "Success after retry"
    assert call_counter == 2
    mock_sleep.assert_called_once_with(1)


@pytest.mark.asyncio
async def test_retry_all_attempts_and_fail(mock_sleep):
    global call_counter
    retry_attempts = 3

    @backoff(retry_count=retry_attempts, exceptions=(TemporaryError,))
    async def always_fail():
        global call_counter
        call_counter += 1
        raise TemporaryError(f"Attempt {call_counter} failed")

    with pytest.raises(TemporaryError, match=f"Attempt {retry_attempts} failed"):
        await always_fail()

    assert call_counter == retry_attempts
    assert mock_sleep.call_count == retry_attempts - 1
