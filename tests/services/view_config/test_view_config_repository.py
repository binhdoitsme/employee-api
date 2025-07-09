import pytest
from employee_api.services.view_config.view_config_repository import ViewConfigRepository
from employee_api.services.view_config.view_config import ListViewConfig
from unittest.mock import AsyncMock
from uuid import uuid4

@pytest.mark.asyncio
async def test_get_list_view_config():
    repo = AsyncMock(spec=ViewConfigRepository)
    repo.get_list_view_config.return_value = ListViewConfig(screen="list_employees", columns=["id", "first_name"])
    config = await repo.get_list_view_config(uuid4(), screen="list_employees")
    assert config.screen == "list_employees"
    assert "id" in config.columns
