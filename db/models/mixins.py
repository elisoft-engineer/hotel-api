from sqlalchemy.orm import declarative_mixin
from datetime import datetime, timezone
from sqlalchemy import Column, DateTime
from sqlalchemy.sql import func

@declarative_mixin
class Timestamp:
    __abstract__ = True

    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    modified_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)