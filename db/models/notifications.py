from ..base import Base
from .mixins import Timestamp
from sqlalchemy import Column, UUID, String, Enum
from .enums import NotificationStatus
from uuid import uuid4


class Notification(Base, Timestamp):
    __tablename__ = "notifications"

    id = Column(UUID, default=uuid4, primary_key=True)
    message = Column(String)
    user_id = Column(UUID)  # to store the id of any kind of user
    status = Column(Enum(NotificationStatus, name="notification_status"), default=NotificationStatus.UNREAD)

    def __repr__(self):
        return self.message
