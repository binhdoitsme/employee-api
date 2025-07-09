from sqlalchemy import Column, Enum as SAEnum, ForeignKey, String, Index
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import DeclarativeBase, relationship, Mapped, mapped_column
from typing import Optional
from uuid import UUID

from employee_api.services.employee.employee import EmployeeStatus


class Base(DeclarativeBase):
    pass


class DepartmentTable(Base):
    __tablename__ = "department"

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    employees: Mapped[list["EmployeeTable"]] = relationship(
        "EmployeeTable", back_populates="department"
    )


class PositionTable(Base):
    __tablename__ = "position"

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    employees: Mapped[list["EmployeeTable"]] = relationship(
        "EmployeeTable", back_populates="position"
    )


class LocationTable(Base):
    __tablename__ = "location"

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    employees: Mapped[list["EmployeeTable"]] = relationship(
        "EmployeeTable", back_populates="location"
    )


class EmployeeTable(Base):
    __tablename__ = "employee"
    __table_args__ = (
        Index(
            "ix_employee_status_location_department_company",
            "status", "location_id", "department_id", "company_id"
        ),
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    org_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    company_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    phone_number: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    department_id: Mapped[Optional[UUID]] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("department.id"), nullable=True
    )
    position_id: Mapped[Optional[UUID]] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("position.id"), nullable=True
    )
    location_id: Mapped[Optional[UUID]] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("location.id"), nullable=True
    )
    status: Mapped[EmployeeStatus] = mapped_column(SAEnum(EmployeeStatus), nullable=False)

    department: Mapped[Optional[DepartmentTable]] = relationship(
        "DepartmentTable", back_populates="employees"
    )
    position: Mapped[Optional[PositionTable]] = relationship(
        "PositionTable", back_populates="employees"
    )
    location: Mapped[Optional[LocationTable]] = relationship(
        "LocationTable", back_populates="employees"
    )
