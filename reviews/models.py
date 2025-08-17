from uuid import uuid4

from sqlalchemy import Column, Text, ForeignKey, Integer, UUID
from sqlalchemy.orm import relationship

from core.database import Base
from core.models import Timestamp


class Review(Base, Timestamp):
    __tablename__ = "reviews"

    id = Column(UUID, default=uuid4, primary_key=True)
    message = Column(Text, nullable=False)
    rating = Column(Integer, nullable=False)

    menu_id = Column(ForeignKey("menu.id"), nullable=False)
    user_id = Column(ForeignKey("users.id"), nullable=False)

    menu_item = relationship("Menu", back_populates="reviews")
    user = relationship("User", back_populates="reviews")

    def __repr__(self):
        return f"{self.__class__.__name__}: {str(self.message)[:15]}... {self.rating}"