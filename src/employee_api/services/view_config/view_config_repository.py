from typing import Protocol
from uuid import UUID

from employee_api.services.view_config.view_config import ListViewConfig


class ViewConfigRepository(Protocol):
    async def get_list_view_config(
        self, org_id: UUID, screen: str
    ) -> ListViewConfig: ...
