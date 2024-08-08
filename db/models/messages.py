from ..base import Base
from .mixins import Timestamp
from sqlalchemy import Column, UUID, String, Text
from uuid import uuid4


class Message(Base, Timestamp):
    __tablename__ = "messages"

    id = Column(UUID, default=uuid4, primary_key=True)
    name = Column(String)
    email = Column(String)
    detail = Column(Text)

    def __repr__(self):
        return self.name
