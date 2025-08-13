from ..base import Base
from .mixins import Timestamp
from sqlalchemy import Column, UUID, String, Text
from uuid import uuid4


class Message(Base, Timestamp):
    __tablename__ = "messages"

    id = Column(UUID, default=uuid4, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    detail = Column(Text, nullable=False)

    def __repr__(self):
        return str(self.name)
