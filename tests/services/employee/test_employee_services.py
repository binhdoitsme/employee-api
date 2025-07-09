from unittest.mock import AsyncMock

import pytest

from employee_api.services.employee.dtos import EmployeeOut, SearchEmployeeCriteria
from employee_api.services.employee.employee_filters import EmployeeFilters
from employee_api.services.employee.employee_services import (
    EmployeeServices,
    SearchResult,
)


@pytest.mark.asyncio
async def test_employee_services_search_returns_result():
    # Arrange
    from uuid import uuid4

    mock_repo = AsyncMock()
    valid_id = uuid4()
    mock_repo.search.return_value = (
        [
            EmployeeOut(
                id=valid_id,
                first_name=None,
                last_name=None,
                contact_info=None,
                department=None,
                location=None,
                position=None,
                status=None,
            )
        ],
        1,
    )
    service = EmployeeServices(repository=mock_repo, cache=None)
    criteria = SearchEmployeeCriteria(
        filters=EmployeeFilters(org_id=valid_id, query=None), limit=50, page=1
    )
    # Act
    result = await service.search(criteria, selected_fields=["id"])
    # Assert
    assert isinstance(result, SearchResult)
    assert result.total == 1
    assert len(result.results) == 1
