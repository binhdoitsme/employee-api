from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class ContactInfo(BaseModel):
    email: Optional[str]
    phone_number: Optional[str]


class Department(BaseModel):
    id: UUID
    name: str


class Position(BaseModel):
    id: UUID
    name: str


class Location(BaseModel):
    id: UUID
    name: str


class EmployeeStatus(Enum):
    ACTIVE = "ACTIVE"
    NOT_STARTED = "NOT_STARTED"
    TERMINATED = "TERMINATED"


class Employee(BaseModel):
    id: UUID
    # assume we have organization, and many companies within one organization
    org_id: UUID
    company_id: UUID
    first_name: str
    last_name: str
    contact_info: ContactInfo
    department: Department | None
    location: Location | None
    position: Position | None
    status: EmployeeStatus
