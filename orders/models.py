from uuid import uuid4

from sqlalchemy import DECIMAL, UUID, Column, ForeignKey, text
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import relationship

from db.base import Base

from ..db.models.assotiations import order_menu_association
from ..db.models.enums import OrderStatus
from ..db.models.mixins import Timestamp


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

from sqlalchemy import UUID, Column, ForeignKey, Table

from ..base import Base

order_menu_association = Table(
    "order_menu",
    Base.metadata,
    Column("order_id", UUID, ForeignKey("orders.id", ondelete="CASCADE"), primary_key=True),
    Column("menu_id", UUID, ForeignKey("menu.id", ondelete="CASCADE"), primary_key=True)
)