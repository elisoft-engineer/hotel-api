from sqlalchemy import Table, Column, UUID, ForeignKey
from ..base import Base

order_menu_association = Table(
    "order_menu",
    Base.metadata,
    Column("order_id", UUID, ForeignKey("orders.id", ondelete="CASCADE"), primary_key=True),
    Column("menu_id", UUID, ForeignKey("menu.id", ondelete="CASCADE"), primary_key=True)
)