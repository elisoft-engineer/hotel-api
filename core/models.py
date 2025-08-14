@declarative_mixin
class Timestamp:
    __abstract__ = True

    created_at = Column(DateTime(timezone=True), default=func.now())
    modified_at = Column(DateTime(timezone=True), default=func.now())