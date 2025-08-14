from uuid import uuid4

from sqlalchemy import DECIMAL, UUID, Column, ForeignKey, Integer, String, Text, text
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import relationship

from db.base import Base

from ..db.models.assotiations import order_menu_association
from ..db.models.enums import MenuCategory
from ..db.models.mixins import Timestamp


class MenuCategory(Enum):
    MAIN_COURSES = "main_courses"
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

    reviews = relationship("Review", back_populates="item")
    orders = relationship("Order", secondary=order_menu_association, back_populates="items")

    def __repr__(self):
        return f"{self.__class__.name}: {self.name}"
    

class Review(Base, Timestamp):
    __tablename__ = "reviews"

    id = Column(UUID, default=uuid4, primary_key=True)
    message = Column(Text, nullable=False)
    rating = Column(Integer, nullable=False)

    menu_id = Column(ForeignKey("menu.id"), nullable=False)
    customer_id = Column(ForeignKey("customers.id"), nullable=False)

    item = relationship("Menu", back_populates="reviews")
    customer = relationship("Customer", back_populates="reviews")

    def __repr__(self):
        return f"{self.__class__.__name__}: {str(self.message)[:15]}... {self.rating}"
