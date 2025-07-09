from uuid import uuid4
import pytest
from employee_api.services.employee.dtos import SearchEmployeeCriteria, EmployeeOut
from employee_api.services.employee.employee_filters import EmployeeFilters
from employee_api.services.employee.employee import ContactInfo, Department, EmployeeStatus, Location, Position


def test_search_employee_criteria_limit_validation():
    filters = EmployeeFilters(org_id=uuid4(), query=None)
    # Valid limit
    SearchEmployeeCriteria(filters=filters, limit=10, page=1)
    # Invalid limit
    with pytest.raises(ValueError):
        SearchEmployeeCriteria(filters=filters, limit=100, page=1)


def test_employee_out_fields():
    emp = EmployeeOut(
        id=uuid4(),
        first_name="John",
        last_name="Doe",
        contact_info=ContactInfo(email="john@example.com", phone_number="123"),
        department=Department(id=uuid4(), name="HR"),
        location=Location(id=uuid4(), name="NYC"),
        position=Position(id=uuid4(), name="Manager"),
        status=EmployeeStatus.ACTIVE,
    )
    assert emp.first_name == "John"
    assert emp.status == EmployeeStatus.ACTIVE
