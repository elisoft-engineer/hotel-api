from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    password: str


class UserSignin(UserBase):
    password: str


class UserUpdate(UserBase):
    first_name: str
    last_name: str


class User(UserBase):
    id: UUID
    first_name: str
    last_name: str
    is_active: bool
    is_staff: bool

    from_attributes: bool = True

