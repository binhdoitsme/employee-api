from pydantic import BaseModel

from ..common.cache import CacheProvider
from .dtos import EmployeeOut, SearchEmployeeCriteria
from .employee_repository import EmployeeRepository


class SearchResult(BaseModel):
    results: list[EmployeeOut]
    total: int
    page: int
    limit: int


class EmployeeServices:
    def __init__(
        self, repository: EmployeeRepository, cache: CacheProvider | None
    ) -> None:
        self.repository = repository
        self.cache = cache

    async def search(
        self, criteria: SearchEmployeeCriteria, selected_fields: list[str]
    ) -> SearchResult:
        # TODO: cache hit first
        # cached = await self.cache.get(str(criteria))
        # if cached: return result

        offset = (criteria.page - 1) * criteria.limit
        employees, total = await self.repository.search(
            org_id=str(criteria.filters.org_id),
            filters=criteria.filters,
            limit=criteria.limit,
            offset=offset,
            selected_fields=selected_fields,
        )
        result = SearchResult(
            results=[EmployeeOut.model_validate(emp) for emp in employees],
            total=total,
            page=criteria.page,
            limit=criteria.limit,
        )
        # TODO: cache store
        # cached = await self.cache.set(str(criteria), result)
        return result
