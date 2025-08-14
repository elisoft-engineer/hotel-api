from uuid import uuid4

from sqlalchemy import UUID, Column, String, Text

from ..base import Base
from ..db.models.mixins import Timestamp


class Message(Base, Timestamp):
    __tablename__ = "messages"

    id = Column(UUID, default=uuid4, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    detail = Column(Text, nullable=False)

    def __repr__(self):
        return str(self.name)
