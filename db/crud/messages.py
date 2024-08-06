from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID
from db.models import messages as models
from db.schemas import messages as schemas


async def get_messages(db: AsyncSession, offset: int | None = None, limit: int | None = None):
    results = await db.execute(select(models.Message).offset(offset).limit(limit))
    return results.scalars().all()


async def get_message(db: AsyncSession, id: UUID):
    result = await db.execute(select(models.Message).where(models.Message.id == id))
    return result.scalars().first()


async def create_message(db: AsyncSession, message: schemas.MessageCreate):
    message_data = message.model_dump()
    db_message = models.message(**message_data)
    db.add(db_message)
    await db.commit()
    await db.refresh(db_message)
    return db_message


"""
There will be no implementation for  the message update since these messages are 
only sent and do not need to be updated, only read
"""


async def delete_message(db: AsyncSession, id: UUID):
    message = await get_message(db, id)
    if not message:
        return None
    
    await db.delete(message)
    await db.commit()
    return {"message": "Message deleted successfully"}