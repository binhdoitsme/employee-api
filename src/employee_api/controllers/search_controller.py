from fastapi import APIRouter, Depends, Request

from employee_api.infrastructure.dependencies import (
    get_employee_services,
    get_view_config_repository,
)
from employee_api.middlewares.rate_limit import rate_limit
from employee_api.services.employee.employee_services import (
    EmployeeServices,
    SearchResult,
)
from employee_api.services.view_config.view_config_repository import (
    ViewConfigRepository,
)

from ..services.employee.dtos import SearchEmployeeCriteria

search_router = APIRouter()


@search_router.post("/search", response_model=SearchResult)
@rate_limit()
async def search_employees(
    request: Request,
    criteria: SearchEmployeeCriteria,
    employee_service: EmployeeServices = Depends(get_employee_services),
    view_config_repository: ViewConfigRepository = Depends(get_view_config_repository),
):
    view_config = await view_config_repository.get_list_view_config(
        criteria.filters.org_id, screen="list_employees"
    )
    return await employee_service.search(
        criteria=criteria, selected_fields=view_config.columns
    )
