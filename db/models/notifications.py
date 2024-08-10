from ..base import Base
from .mixins import Timestamp
from sqlalchemy import Column, UUID, String
from .enums import NotificationStatus, UserType
from uuid import uuid4


class Notification(Base, Timestamp):
    __tablename__ = "notifications"

    id = Column(UUID, default=uuid4, primary_key=True)
    message = Column(String)
    user_id = Column(UUID)
    user_type = Column(String, nullable=True)
    status = Column(String, nullable=False, default=NotificationStatus.UNREAD.value)

    def __repr__(self):
        return f"{self.__class__.__name__}: {self.message}"
