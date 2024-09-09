from ..base import Base
from .mixins import Timestamp
from sqlalchemy import Column, UUID, String, Text, DECIMAL, Integer, ForeignKey
from uuid import uuid4
from .enums import MenuCategory
from sqlalchemy.orm import relationship
from .assotiations import order_menu_association


class Menu(Base, Timestamp):
    __tablename__ = "menu"

    id = Column(UUID, default=uuid4, primary_key=True)
    name = Column(String, index=True, nullable=False)
    description = Column(Text, nullable=False)
    price = Column(DECIMAL, nullable=False)
    category = Column(String, nullable=False, default=MenuCategory.OTHER.value)
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
