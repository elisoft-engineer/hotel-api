from ..base import Base
from .mixins import Timestamp
from sqlalchemy import Column, UUID, String, Text, DECIMAL, Enum, Integer, ForeignKey
from uuid import uuid4
from .enums import MenuCategory
from sqlalchemy.orm import relationship


class Menu(Base, Timestamp):
    __tablename__ = "menu"

    id = Column(UUID, default=uuid4, primary_key=True)
    name = Column(String, index=True)
    description = Column(Text())
    price = Column(DECIMAL)
    category = Column(Enum(MenuCategory, name="menu_category"), default=MenuCategory.OTHER)
    image = Column(String, nullable=True)
    thumbnail = Column(String, nullable=True)

    reviews = relationship("Review", back_populates="item")

    def __repr__(self):
        return f"{self.__class__.name}: {self.name}"
    

class Review(Base, Timestamp):
    __tablename__ = "reviews"

    id = Column(UUID, default=uuid4, primary_key=True)
    message = Column(Text())
    rating = Column(Integer)  # validate for a range of 1 to 5 in the front-end

    menu_id = Column(ForeignKey("menu.id"))
    customer_id = Column(ForeignKey("customer.id"))

    menu = relationship("Menu", back_populates="reviews")
    customer = relationship("Customer", back_populates="reviews")

    def __repr__(self):
        return f"{self.__class__.__name__}: {str(self.message)[:15]}... {self.rating}"
