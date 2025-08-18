from enum import Enum
from uuid import uuid4

from sqlalchemy import UUID, Column, String, text, ForeignKey
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import relationship

from core.database import Base
from core.models import Timestamp


class NotificationStatus(Enum):
    READ = "read"
    UNREAD = "unread"


class Notification(Base, Timestamp):
    __tablename__ = "notifications"

    id = Column(UUID, default=uuid4, primary_key=True)
    message = Column(String, nullable=False)
    user_id = Column(ForeignKey("users.id"), nullable=False)
    status = Column(
        postgresql.ENUM(*[e.value for e in NotificationStatus], name="notification_status", create_type=False),
        default=NotificationStatus.UNREAD.value,
        server_default=text(f"'{NotificationStatus.UNREAD.value}'::notification_status"),
        nullable=False
    )

    user = relationship("User", back_populates="notifications")

    def __repr__(self):
        return f"{self.__class__.__name__}: {self.message}"
