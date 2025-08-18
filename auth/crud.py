from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from auth import models, schemas
from auth.utils import get_password_hash


async def get_users(db: AsyncSession, offset: int | None = None, limit: int | None = None):
    results = await db.execute(select(models.User).offset(offset).limit(limit))
    return results.scalars().all()


async def get_user(db: AsyncSession, user_id: UUID):
    result = await db.execute(select(models.User).where(models.User.id == user_id))
    return result.scalars().first()


async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(models.User).where(models.User.email == email))
    return result.scalars().first()


async def create_user(db: AsyncSession, user: schemas.UserCreate):
    user_data = user.model_dump()
    user_data['password'] = get_password_hash(user.password)
    db_user = models.User(**user_data)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def update_user(db: AsyncSession, user_id: UUID, user_update: schemas.UserUpdate):
    user = await get_user(db, user_id)
    if not user:
        return None

    update_data = user_update.model_dump(exclude_unset=True)
    for key, value in update_data:
        setattr(user, key, value)

    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def toggle_active_status(db: AsyncSession, user_id: UUID):
    user = await get_user(db, user_id)
    if not user:
        return None
    setattr(user, "is_active", not bool(user.is_active))
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def delete_user(db: AsyncSession, user_id: UUID):
    user = await get_user(db, user_id)
    if not user:
        return None

    await db.delete(user)
    await db.commit()
    return {"detail": "user account deleted successfully"}
