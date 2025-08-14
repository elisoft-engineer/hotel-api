from decimal import Decimal
from typing import List
from uuid import UUID

from pydantic import BaseModel

from menu.schemas import Menu


class OrderBase(BaseModel):
    customer_id: UUID



class OrderCreate(OrderBase):
    item_ids: List[UUID]


"""
The update schema will not be implemented since we don't the only attribute to
be changed is the status of the order
"""


class Order(OrderBase):
    id: UUID
    status: str
    items: List[Menu] = []
    amount: Decimal

    class Config:
        from_attributes: bool = True
