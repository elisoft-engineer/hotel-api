from uuid import UUID

from pydantic import BaseModel, EmailStr


class MessageBase(BaseModel):
    name: str
    email: EmailStr
    detail: str


class MessageCreate(MessageBase):
    pass


class Message(MessageBase):
    id: UUID

    class Config:
        from_attributes: bool = True
