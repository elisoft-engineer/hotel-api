from uuid import UUID

from pydantic import BaseModel


class NotificationBase(BaseModel):
    message: str


class NotificationCreate(NotificationBase):
    user_id: UUID
    user_type: str


class Notification(NotificationBase):
    id: UUID
    user_id: UUID
    status: str

    class Config:
        from_attributes: bool = True
