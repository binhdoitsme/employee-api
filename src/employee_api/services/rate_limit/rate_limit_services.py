import time
from employee_api.services.rate_limit.store import RateLimitStore

RATE_LIMIT = 10
WINDOW = 60


class RateLimitServices:
    def __init__(self, store: RateLimitStore) -> None:
        self.store = store

    async def check_rate_limit(self, ip: str) -> None:
        now = time.time()

        timestamps = await self.store.get_access_times(ip)
        recent = [t for t in timestamps if now - t < WINDOW]

        if len(recent) >= RATE_LIMIT:
            raise ConnectionAbortedError(
                f"Rate limit exceeded. Max {RATE_LIMIT} requests per {WINDOW} seconds."
            )

        recent.append(now)
        await self.store.set_access_times(ip, recent)
