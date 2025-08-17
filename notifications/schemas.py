from uuid import UUID

from pydantic import BaseModel


class Notification(BaseModel):
    id: UUID
    message: str
    user_id: UUID
    status: str

    class Config:
        from_attributes: bool = True
