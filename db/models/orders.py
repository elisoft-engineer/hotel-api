from uuid import uuid4

from sqlalchemy import DECIMAL, UUID, Column, ForeignKey, String
from sqlalchemy.orm import relationship

from ..base import Base
from .assotiations import order_menu_association
from .enums import OrderStatus
from .mixins import Timestamp


class Order(Base, Timestamp):
    __tablename__ = "orders"

    id = Column(UUID, default=uuid4, primary_key=True)
    amount = Column(DECIMAL, nullable=False)
    status = Column(String, nullable=False, default=OrderStatus.PENDING.value)

    customer_id = Column(ForeignKey("customers.id"), nullable=False)

    customer = relationship("Customer", back_populates="orders")
    items = relationship("Menu", secondary=order_menu_association, back_populates="orders")
