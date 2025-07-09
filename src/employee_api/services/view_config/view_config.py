from pydantic import BaseModel


class ListViewConfig(BaseModel):
    screen: str
    columns: list[str]
