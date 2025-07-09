"""View config repository which always return the same values for now"""

from uuid import UUID

from employee_api.services.view_config.view_config import ListViewConfig
from employee_api.services.view_config.view_config_repository import (
    ViewConfigRepository,
)


class InMemoryViewConfigRepository(ViewConfigRepository):
    async def get_list_view_config(self, org_id: UUID, screen: str) -> ListViewConfig:
        return ListViewConfig(
            screen=screen,
            columns=[
                "contact_info",
                "department",
                "location",
                "position",
            ],
        )
