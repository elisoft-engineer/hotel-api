from ..base import Base
from .mixins import Timestamp
from sqlalchemy import Column, UUID, String, Text, ForeignKey
from uuid import uuid4

class Notification(Base, Timestamp):
    __tablename__ = "notifications"

    id = Column(UUID, default=uuid4, primary_key=True)
    message = Column(String)
    user_id = Column(ForeignKey()) # I shall have to come back for this

    def __repr__(self):
        return self.message