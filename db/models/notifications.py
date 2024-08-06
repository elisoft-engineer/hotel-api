from ..base import Base
from .mixins import Timestamp
from sqlalchemy import Column, UUID, String, ForeignKey, Enum
from .enums import NotificationStatus
from uuid import uuid4

class Notification(Base, Timestamp):
    __tablename__ = "notifications"

    id = Column(UUID, default=uuid4, primary_key=True)
    message = Column(String)
    user_id = Column(ForeignKey()) # I shall have to come back for this
    status = Column(Enum(NotificationStatus, name="notification_status"), default=NotificationStatus.UNREAD)

    def __repr__(self):
        return self.message