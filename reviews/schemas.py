from uuid import UUID

from pydantic import BaseModel


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
        from_attributes: bool = True
