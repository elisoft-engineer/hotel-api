from ..base import Base
from .mixins import Timestamp
from sqlalchemy import Column, UUID, String, Boolean
from sqlalchemy.orm import declarative_mixin, relationship
from uuid import uuid4


"""
A base user class is more robust and precise as we just have to subclass it to
manage both the admins and customers.
"""


@declarative_mixin
class User():
    __abstract__ = True

    id = Column(UUID, primary_key=True, default=uuid4)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)


class Admin(Base, User, Timestamp):
    employee_id = Column(String, index=True)
    # the employee id can be used as an alternative for authentication


class Customer(Base, User, Timestamp):
    __tablename__ = "users"

    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)

    reviews = relationship("Review", back_populates="customer")

    def __repr__(self):
        return f"{self.__class__.__name__}: {self.email}"
