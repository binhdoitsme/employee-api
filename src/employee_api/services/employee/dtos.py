from uuid import UUID

from pydantic import BaseModel, field_validator, Field

from .employee import ContactInfo, Department, EmployeeStatus, Location, Position
from .employee_filters import EmployeeFilters


class SearchEmployeeCriteria(BaseModel):
    filters: EmployeeFilters = Field(
        ..., description="Filtering options for employees (org, query, status, etc)"
    )
    limit: int = Field(50, description="Maximum number of results per page (max 50)")
    page: int = Field(1, description="Page number for pagination (1-based)")

    @field_validator("limit")
    @classmethod
    def limit_max_50(cls, v):
        if v > 50:
            raise ValueError("limit must not exceed 50")
        return v


class EmployeeOut(BaseModel):
    # id: UUID = Field(..., description="Employee unique identifier (UUID)")
    first_name: str | None = Field(None, description="First name of the employee")
    last_name: str | None = Field(None, description="Last name of the employee")
    contact_info: ContactInfo | None = Field(
        None, description="Contact information (email, phone)"
    )
    department: str | None = Field(None, description="Department Name if any")
    location: str | None = Field(None, description="Location name if any")
    position: str | None = Field(None, description="Position name if any")
    status: EmployeeStatus | None = Field(
        None, description="Employment status (ACTIVE, NOT_STARTED, TERMINATED)"
    )

    class Config:
        from_attributes = True
