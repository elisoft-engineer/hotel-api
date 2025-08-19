from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from menu.models import MenuCategory


class MenuBase(BaseModel):
    name: str
    description: str
    price: Decimal
    category: MenuCategory


class MenuCreate(MenuBase):
    image: str
    thumbnail: str


class MenuUpdate(MenuBase):
    image: Optional[str]
    thumbnail: Optional[str]


class Menu(MenuBase):
    id: UUID
    image: str
    thumbnail: str

    class Config:
        from_attributes: bool = True
