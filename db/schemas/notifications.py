from pydantic import BaseModel
from uuid import UUID
from db.models.enums import NotificationStatus, UserType


class NotificationBase(BaseModel):
    message: str


class NotificationCreate(NotificationBase):
    user_id: UUID
    user_type: UserType


"""
For the Update schema, we only need to update the status
"""


class Notification(NotificationBase):
    id: UUID
    user_id: UUID
    status: NotificationStatus

    class Config:
        from_attributes = True
