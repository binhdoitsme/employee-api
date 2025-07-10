from uuid import UUID
from sqlalchemy import func, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from employee_api.infrastructure.db.models import (
    EmployeeTable,
    DepartmentTable,
    PositionTable,
    LocationTable,
)
from employee_api.services.employee.dtos import EmployeeOut
from employee_api.services.employee.employee import (
    ContactInfo,
    Department,
    Location,
    Position,
)
from employee_api.services.employee.employee_filters import EmployeeFilters
from employee_api.services.employee.employee_repository import EmployeeRepository


class EmployeeRepositoryOnSqla(EmployeeRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def search(
        self,
        org_id: str,
        filters: EmployeeFilters,
        limit: int = 50,
        offset: int = 0,
        selected_fields: list[str] | None = None,
    ) -> tuple[list[EmployeeOut], int]:
        if not selected_fields:
            raise ValueError("must provide selected_fields")

        # Build dynamic projection columns and track joins
        columns = [
            EmployeeTable.id,
            EmployeeTable.status.label("status"),
            EmployeeTable.first_name.label("first_name"),
            EmployeeTable.last_name.label("last_name"),
        ]
        joins = {}

        for f in selected_fields:
            if f in {"id", "status", "first_name", "last_name"}:
                continue  # already included
            elif f == "contact_info":
                columns.append(EmployeeTable.email.label("email"))
                columns.append(EmployeeTable.phone_number.label("phone_number"))
            elif f == "department":
                columns.append(DepartmentTable.id.label("department_id"))
                columns.append(DepartmentTable.name.label("department_name"))
                joins["department"] = EmployeeTable.department_id == DepartmentTable.id
            elif f == "position":
                columns.append(PositionTable.id.label("position_id"))
                columns.append(PositionTable.name.label("position_name"))
                joins["position"] = EmployeeTable.position_id == PositionTable.id
            elif f == "location":
                columns.append(LocationTable.id.label("location_id"))
                columns.append(LocationTable.name.label("location_name"))
                joins["location"] = EmployeeTable.location_id == LocationTable.id

        # Shared filtering
        base_where = [EmployeeTable.org_id == UUID(org_id)]

        if filters.query:
            base_where.append(
                or_(
                    EmployeeTable.first_name.ilike(f"%{filters.query}%"),
                    EmployeeTable.last_name.ilike(f"%{filters.query}%"),
                )
            )
        if filters.status:
            base_where.append(EmployeeTable.status.in_(filters.status))
        if filters.locations:
            base_where.append(EmployeeTable.location_id.in_(filters.locations))
        if filters.companies:
            base_where.append(EmployeeTable.company_id.in_(filters.companies))
        if filters.departments:
            base_where.append(EmployeeTable.department_id.in_(filters.departments))
        if filters.positions:
            base_where.append(EmployeeTable.position_id.in_(filters.positions))

        # Main SELECT query
        stmt = select(*columns).where(*base_where)
        if "department" in joins:
            stmt = stmt.join(DepartmentTable, joins["department"], isouter=True)
        if "position" in joins:
            stmt = stmt.join(PositionTable, joins["position"], isouter=True)
        if "location" in joins:
            stmt = stmt.join(LocationTable, joins["location"], isouter=True)

        result = await self.session.execute(stmt.limit(limit).offset(offset))
        rows = result.all()

        employees = []
        seen_ids = set()

        for row in rows:
            data = dict(
                zip([c.key if hasattr(c, "key") else c._label for c in columns], row)
            )
            emp_kwargs = {
                "id": data.get("id"),
                "status": data.get("status"),
                "first_name": data.get("first_name"),
                "last_name": data.get("last_name"),
            }

            if "email" in data or "phone_number" in data:
                emp_kwargs["contact_info"] = ContactInfo(
                    email=data.get("email"),
                    phone_number=data.get("phone_number"),
                )

            if data.get("department_name"):
                emp_kwargs["department"] = data["department_name"]
            if data.get("location_name"):
                emp_kwargs["location"] = data["location_name"]
            if data.get("position_name"):
                emp_kwargs["position"] = data["position_name"]

            emp_id = emp_kwargs["id"]
            if emp_id and emp_id in seen_ids:
                continue
            seen_ids.add(emp_id)
            employees.append(EmployeeOut(**emp_kwargs))

        # Count query (with same WHERE clause, no joins)
        count_stmt = (
            select(func.count())
            .select_from(EmployeeTable)
            .where(*base_where)
        )
        count_result = await self.session.execute(count_stmt)
        total = count_result.scalar_one()

        return employees, total
