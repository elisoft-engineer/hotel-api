from uuid import uuid4

from sqlalchemy import UUID, Boolean, Column, String, text
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import declarative_mixin, relationship

from db.base import Base

from .enums import UserType
from .mixins import Timestamp

"""
A base user class is more robust and precise as we just have to subclass it to
manage both the admins and customers.
"""


@declarative_mixin
class User:
    __abstract__ = True

    id = Column(UUID, primary_key=True, default=uuid4)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)


class Admin(Base, User, Timestamp):
    __tablename__ = "admins"
    employee_id = Column(String, index=True)
    user_type = Column(
        postgresql.ENUM(*[e.value for e in UserType], name="user_type", create_type=False),
        default=UserType.ADMIN.value,
        server_default=text(f"'{UserType.ADMIN.value}'::user_type"),
        nullable=False
    )


class Customer(Base, User, Timestamp):
    __tablename__ = "customers"

    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    user_type = user_type = Column(
        postgresql.ENUM(*[e.value for e in UserType], name="user_type", create_type=False),
        default=UserType.CUSTOMER.value,
        server_default=text(f"'{UserType.CUSTOMER.value}'::user_type"),
        nullable=False
    )

    reviews = relationship("Review", back_populates="customer")
    orders = relationship("Order", back_populates="customer")

    def __repr__(self):
        return f"{self.__class__.__name__}: {self.email}"
