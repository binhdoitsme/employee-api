import pytest
from employee_api.services.rate_limit.rate_limit_services import RateLimitServices
from unittest.mock import AsyncMock


@pytest.mark.asyncio
async def test_check_rate_limit_allows_under_limit():
    store = AsyncMock()
    store.get_access_times.return_value = []
    limiter = RateLimitServices(store)
    await limiter.check_rate_limit("127.0.0.1")
    store.set_access_times.assert_called()


@pytest.mark.asyncio
async def test_check_rate_limit_raises_on_exceed():
    import time
    store = AsyncMock()
    # Simulate 10 requests in the current window
    now = time.time()
    store.get_access_times.return_value = [now] * 10
    limiter = RateLimitServices(store)
    with pytest.raises(ConnectionAbortedError):
        await limiter.check_rate_limit("127.0.0.1")
