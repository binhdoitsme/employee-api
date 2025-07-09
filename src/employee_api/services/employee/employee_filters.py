from uuid import UUID

from pydantic import BaseModel

from .employee import EmployeeStatus


class EmployeeFilters(BaseModel):
    org_id: UUID
    query: str | None
    status: list[EmployeeStatus] = []
    locations: list[UUID] = []  # location ids only
    companies: list[UUID] = []  # company IDs
    departments: list[UUID] = []  # department IDs
    positions: list[UUID] = []  # positionIDs
