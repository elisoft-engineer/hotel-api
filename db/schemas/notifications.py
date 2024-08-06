from pydantic import BaseModel
from uuid import UUID
from models.enums import NotificationStatus


class NotificationBase(BaseModel):
    message: str


class NotificationCreate(NotificationBase):
    user_id: UUID # Update this later in accordance to the model


"""
For the Update schema, we only need to update the status
"""


class Notification(NotificationBase):
    id: UUID
    user_id: UUID
    status: NotificationStatus

    class Config:
        from_attributes = True
