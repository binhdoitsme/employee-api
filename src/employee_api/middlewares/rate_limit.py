from functools import wraps
from typing import Any, Awaitable, Callable

from fastapi import HTTPException, Request
from starlette.requests import Request

from employee_api.infrastructure.dependencies import get_rate_limiter


def get_client_ip(request: Request) -> str:
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    if not request.client:
        return ""
    return request.client.host


def rate_limit() -> (
    Callable[[Callable[..., Awaitable[Any]]], Callable[..., Awaitable[Any]]]
):
    limiter = get_rate_limiter()

    def decorator(func: Callable[..., Awaitable[Any]]) -> Callable[..., Awaitable[Any]]:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            request: Request | None = None
            # Find the request object in args or kwargs
            for arg in list(args) + list(kwargs.values()):
                if isinstance(arg, Request):
                    request = arg
                    break
            if request is None:
                raise RuntimeError("Request object not found for rate limiting.")
            ip = get_client_ip(request)
            try:
                await limiter.check_rate_limit(ip)
                print("Not RATE LIMITED")
            except ConnectionAbortedError as e:
                raise HTTPException(status_code=429, detail=e.args[0])
            return await func(*args, **kwargs)

        return wrapper

    return decorator
