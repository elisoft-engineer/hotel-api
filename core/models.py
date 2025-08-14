from sqlalchemy import Column, DateTime
from sqlalchemy.orm import declarative_mixin
from sqlalchemy.sql import func


@declarative_mixin
class Timestamp:
    __abstract__ = True

    created_at = Column(DateTime(timezone=True), default=func.now())
    modified_at = Column(DateTime(timezone=True), default=func.now())