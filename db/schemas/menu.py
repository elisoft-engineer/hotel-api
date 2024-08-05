from pydantic import BaseModel
from models.enums import MenuCategory
from uuid import UUID

class MenuBase(BaseModel):
    name: str
    description: str
    price: float
    category: MenuCategory

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
        from_attributes = True

class ReviewBase(BaseModel):
    message: str
    rating: int

class ReviewCreate(ReviewBase):
    menu_id: UUID
    customer_id: UUID

class ReviewUpdate(ReviewBase):
    pass

class Review(ReviewBase):
    id: UUID
    menu_id: UUID
    customer_id: UUID

    class Config:
        from_attributes = True
