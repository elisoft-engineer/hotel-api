from pydantic import BaseModel
from uuid import UUID
from typing import List
from decimal import Decimal
from .menu import Menu
from db.models.enums import OrderStatus


class OrderBase(BaseModel):
    amount: Decimal
    customer_id: UUID
    items: List[Menu] = []


class OrderCreate(OrderBase):
    pass


"""
The update schema will not be implemented since we don't the only attribute to
be changed is the status of the order
"""


class Order(OrderBase):
    id: UUID
    status: OrderStatus

    class Config:
        from_attributes = True
