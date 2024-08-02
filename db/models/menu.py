from sqlalchemy import Column, UUID, String, Text, DECIMAL, Enum, Integer, ForeignKey
from .category import MenuCategory
from uuid import uuid4
from ..base import Base
from .mixins import Timestamp
from sqlalchemy.orm import relationship

class Menu(Base, Timestamp):
    __tablename__ = "menu"

    id = Column(UUID, default=uuid4, primary_key=True)
    name = Column(String, nullable=False, index=True)
    description = Column(Text(), nullable=False)
    price = Column(DECIMAL, nullable=False)
    category = Column(Enum(MenuCategory, name="menu_category"))
    image = Column(String, nullable=True)
    thumbnail = Column(String, nullable=True)

    

class Review(Base, Timestamp):
    __tablename__ = "reviews"

    id = Column(UUID, default=uuid4, primary_key=True)
    message = Column(Text(), nullable=False)
    rating = Column(Integer, nullable=False)

    menu_id = Column(ForeignKey("menu.id"))
    customer_id = Column(ForeignKey("customer.id"))

    menu = relationship("Menu", back_populates="reviews")
