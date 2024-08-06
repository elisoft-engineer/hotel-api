from pydantic import BaseModel, EmailStr
from uuid import UUID


class MessageBase(BaseModel):
    name: str
    email: EmailStr
    detail: str


class MessageCreate(MessageBase):
    pass


class Message(MessageBase):
    id: UUID

    class Config:
        from_attributes = True