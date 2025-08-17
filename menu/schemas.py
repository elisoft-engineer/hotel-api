from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel


class MenuBase(BaseModel):
    name: str
    description: str
    price: Decimal
    category: str


class MenuCreate(MenuBase):
    image: str
    thumbnail: str


class MenuUpdate(MenuBase):
    pass


class Menu(MenuBase):
    id: UUID
    image: str
    thumbnail: str

    class Config:
        from_attributes: bool = True
