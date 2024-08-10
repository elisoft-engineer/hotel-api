from pydantic import BaseModel
from uuid import UUID
from typing import List
from decimal import Decimal
from .menu import Menu


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
        from_attributes = True
