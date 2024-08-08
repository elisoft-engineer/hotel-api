from sqlalchemy.orm import declarative_mixin
from datetime import datetime, timezone
from sqlalchemy import Column, DateTime
from sqlalchemy.sql import func

"""
Almost all the database models require the timestamps fields. It's better to
have the Timestamp class and then have it subclassed by all the models for
better code.
"""


@declarative_mixin
class Timestamp:
    __abstract__ = True

    created_at = Column(DateTime(timezone=True), default=func.now())
    modified_at = Column(DateTime(timezone=True), default=func.now())
