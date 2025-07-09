from typing import Protocol

from .dtos import EmployeeOut
from .employee_filters import EmployeeFilters


class EmployeeRepository(Protocol):
    async def search(
        self,
        org_id: str,
        filters: EmployeeFilters,
        limit: int = 50,
        offset: int = 0,
        selected_fields: list[str] | None = None,
    ) -> tuple[list[EmployeeOut], int]:
        """
        Search employees by filters scoped to the given organization.

        - org_id: ID of the requesting organization
        - filters: department, position, location, query, etc.
        - limit/offset: pagination
        - selected_fields: which fields to include (based on org config)

        Returns a list of serialized employee DTOs (not ORM models).
        """
        ...
