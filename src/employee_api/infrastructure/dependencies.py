import os

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from employee_api.infrastructure.db.employee_repository import EmployeeRepositoryOnSqla
from employee_api.infrastructure.in_memory.rate_limiter_store import (
    InMemoryRateLimitStore,
)
from employee_api.infrastructure.in_memory.view_config_repository import (
    InMemoryViewConfigRepository,
)
from employee_api.services.employee.employee_repository import EmployeeRepository
from employee_api.services.employee.employee_services import EmployeeServices
from employee_api.services.rate_limit.rate_limit_services import RateLimitServices
from employee_api.services.view_config.view_config_repository import (
    ViewConfigRepository,
)

DATABASE_URL = os.environ["DATABASE_URL"]

engine = create_async_engine(DATABASE_URL, echo=True, future=True)
async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


def get_rate_limiter() -> RateLimitServices:
    store = InMemoryRateLimitStore()
    return RateLimitServices(store)


def get_sqla_async_session() -> AsyncSession:
    return async_session()


def get_employee_repository(
    session: AsyncSession = get_sqla_async_session(),
):
    return EmployeeRepositoryOnSqla(session=session)


def get_employee_services() -> EmployeeServices:
    return EmployeeServices(
        repository=get_employee_repository(), cache=None
    )  # NO cache provider for brevity


def get_view_config_repository() -> ViewConfigRepository:
    return InMemoryViewConfigRepository()
