from uuid import uuid4

from sqlalchemy import UUID, Boolean, Column, String
from sqlalchemy.orm import relationship

from core.database import Base
from core.models import Timestamp


class User(Base, Timestamp):
    __tablename__ = "users"

    id = Column(UUID, primary_key=True, default=uuid4)
    email = Column(String, unique=True, index=True, nullable=False)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_staff = Column(Boolean, default=False)

    orders = relationship("Order", back_populates="user")
    notifications = relationship("Notification", back_populates="user", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"{self.__class__.__name__}: {self.email}"
