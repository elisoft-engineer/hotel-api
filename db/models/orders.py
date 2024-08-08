from ..base import Base
from .mixins import Timestamp
from sqlalchemy import Column, UUID, DECIMAL, ForeignKey, Enum
from uuid import uuid4
from .enums import OrderStatus
from sqlalchemy.orm import relationship
from .assotiations import order_menu_association


class Order(Base, Timestamp):
    __tablename__ = "orders"

    id = Column(UUID, default=uuid4, primary_key=True)
    amount = Column(DECIMAL)
    customer_id = Column(ForeignKey("customers.id"))
    status = Column(Enum(OrderStatus, name="order_status"), default=OrderStatus.PENDING)

    customer = relationship("Customer", back_populates="orders")
    items = relationship("Menu", secondary=order_menu_association, back_populates="orders")
