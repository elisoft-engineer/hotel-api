from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID
from db.models import notifications as models
from db.models.enums import NotificationStatus
from db.schemas import notifications as schemas


async def get_user_notifications(
    db: AsyncSession,
    user_id: UUID,
    offset: int | None = None,
    limit: int | None = None
):
    results = await db.execute(
        select(models.Notification).where(models.Notification.user_id == user_id).offset(offset).limit(limit)
    )
    return results.scalars().all()  # Look up how to order the status


async def get_user_unread_notifications(
    db: AsyncSession,
    user_id: UUID,
    offset: int | None = None,
    limit: int | None = None
):
    results = await db.execute(
        select(models.Notification).where(models.Notification.user_id == user_id and models.Notification.status == NotificationStatus.UNREAD).offset(offset).limit(limit)
    )
    return results.scalars().all()


async def get_user_read_notifications(
    db: AsyncSession,
    user_id: UUID,
    offset: int | None = None,
    limit: int | None = None
):
    results = await db.execute(
        select(models.Notification).where(models.Notification.user_id == user_id and models.Notification.status == NotificationStatus.READ).offset(offset).limit(limit)
    )
    return results.scalars().all()


async def get_notification(db: AsyncSession, notification_id: UUID):
    result = await db.execute(select(models.Notification).where(models.Notification.id == notification_id))
    return result.scalars().first()


async def create_notification(db: AsyncSession, notification: schemas.NotificationCreate):
    notification_data = notification.model_dump()
    db_notification = models.Notification(**notification_data)
    db.add(db_notification)
    await db.commit()
    await db.refresh(db_notification)
    return db_notification


async def mark_notification_as_read(db: AsyncSession, notification_id: UUID):
    notification = await get_notification(db, notification_id)
    if not notification:
        return None
    
    setattr(notification, "status", NotificationStatus.READ)
    db.add(notification)
    await db.commit()
    await db.refresh(notification)
    return {"detail": "Notification read successfully"}


async def mark_all_notifications_as_read(db: AsyncSession, user_id: UUID):
    unread_notifications = get_user_unread_notifications(db, user_id)

    for notification in unread_notifications:  # confirm about the unread_notifications sequence
        setattr(notification, "status", NotificationStatus.READ)
        db.add(notification)
        await db.commit()
        await db.refresh(notification)

    return {"detail": "Notifications read successfully"}
