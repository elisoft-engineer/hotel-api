from pydantic import BaseModel
from uuid import UUID


class NotificationBase(BaseModel):
    message: str


class NotificationCreate(NotificationBase):
    user_id: UUID
    user_type: str


"""
For the Update schema, we only need to update the status
"""


class Notification(NotificationBase):
    id: UUID
    user_id: UUID
    status: str

    class Config:
        from_attributes: bool = True
