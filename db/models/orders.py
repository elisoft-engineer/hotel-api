from uuid import uuid4

from sqlalchemy import DECIMAL, UUID, Column, ForeignKey, text
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import relationship

from db.base import Base

from .assotiations import order_menu_association
from .enums import OrderStatus
from .mixins import Timestamp


class Order(Base, Timestamp):
    __tablename__ = "orders"

    id = Column(UUID, default=uuid4, primary_key=True)
    amount = Column(DECIMAL, nullable=False)
    status = Column(
        postgresql.ENUM(*[e.value for e in OrderStatus], name="order_status", create_type=False),
        default=OrderStatus.PENDING.value,
        server_default=text(f"'{OrderStatus.PENDING.value}'::order_status"),
        nullable=False
    )

    customer_id = Column(ForeignKey("customers.id"), nullable=False)

    customer = relationship("Customer", back_populates="orders")
    items = relationship("Menu", secondary=order_menu_association, back_populates="orders")
