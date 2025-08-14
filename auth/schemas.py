from pydantic import BaseModel

# Handle the token data schema later

# class TokenData(BaseModel):

class Token(BaseModel):
    access_token: str
    token_type: str


from typing import List
from uuid import UUID

from pydantic import BaseModel, EmailStr

from .notifications import Notification


class AbstractUser(BaseModel):
    email: EmailStr


class AdminBase(AbstractUser):
    employee_id: str


class AdminCreate(AdminBase):
    password: str


class AdminSignin(AbstractUser):
    password: str


class AdminUpdate(AdminBase):
    pass


class Admin(AdminBase):
    id: UUID
    is_active: bool
    user_type: str
    notifications: List[Notification] = []

    class Config:
        from_attributes: bool = True


class CustomerBase(AbstractUser):
    pass


class CustomerCreate(CustomerBase):
    password: str


class CustomerSignin(CustomerBase):
    password: str


class CustomerUpdate(CustomerBase):
    first_name: str
    last_name: str


class Customer(CustomerBase):
    id: UUID
    first_name: str
    last_name: str
    is_active: bool
    user_type: str
    notifications: List[Notification] = []

    from_attributes: bool = True

