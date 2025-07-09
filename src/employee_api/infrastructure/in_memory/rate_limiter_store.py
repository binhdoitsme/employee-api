from collections import defaultdict
from typing import List

from employee_api.services.rate_limit.store import RateLimitStore

_access_log = defaultdict[str, List[float]](list)


class InMemoryRateLimitStore(RateLimitStore):
    async def get_access_times(self, ip: str) -> list[float]:
        return _access_log[ip]

    async def set_access_times(self, ip: str, timestamps: list[float]) -> None:
        _access_log[ip] = timestamps
