from enum import Enum
from uuid import uuid4

from sqlalchemy import DECIMAL, UUID, Column, ForeignKey, Table, text
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import relationship

from core.database import Base
from core.models import Timestamp

order_menu_association = Table(
    "order_menu",
    Base.metadata,
    Column("order_id", UUID, ForeignKey("orders.id", ondelete="CASCADE"), primary_key=True),
    Column("menu_id", UUID, ForeignKey("menu.id", ondelete="CASCADE"), primary_key=True)
)


class OrderStatus(Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


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

