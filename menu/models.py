from enum import Enum
from uuid import uuid4

from sqlalchemy import DECIMAL, UUID, Column, String, Text, text
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import relationship

from core.database import Base
from core.models import Timestamp
from orders.models import order_menu_association


class MenuCategory(Enum):
    MAIN_COURSES = "main courses"
    DRINKS = "drinks"
    OTHER = "other"
    # TODO: Add the enum types later


class Menu(Base, Timestamp):
    __tablename__ = "menu"

    id = Column(UUID, default=uuid4, primary_key=True)
    name = Column(String, index=True, nullable=False)
    description = Column(Text, nullable=False)
    price = Column(DECIMAL, nullable=False)
    category = Column(
        postgresql.ENUM(*[e.value for e in MenuCategory], name="menu_category", create_type=False),
        default=MenuCategory.OTHER.value,
        server_default=text(f"'{MenuCategory.OTHER.value}'::menu_category"),
        nullable=False
    )
    image = Column(String, nullable=True)
    thumbnail = Column(String, nullable=True)

    orders = relationship("Order", secondary=order_menu_association, back_populates="items")
    reviews = relationship("Review", back_populates="menu_item", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(name='{self.name}', price={self.price})>"
