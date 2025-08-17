from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from notifications import models, schemas


async def get_notifications(
        db: AsyncSession,
        user_id: UUID,
        notification_status: str | None = None,
        offset: int | None = None,
        limit: int | None = None
):
    if notification_status and notification_status in [status.value for status in models.NotificationStatus]:
        results = await db.execute(
            select(models.Notification).where(
                models.Notification.user_id == user_id and models.Notification.status == notification_status
                ).offset(offset).limit(limit)
        )
    else:
        results = await db.execute(
            select(models.Notification).where(models.Notification.user_id == user_id)\
                .offset(offset).limit(limit)
        )
    return results.scalars().all()


async def patch_notifications(db: AsyncSession, user_id: UUID):
    unread_notifications = await get_notifications(
        db, user_id, notification_status=models.NotificationStatus.UNREAD.value
    )

    for notification in unread_notifications:
        setattr(notification, "status", models.NotificationStatus.READ.value)
        db.add(notification)
        await db.commit()
        await db.refresh(notification)

    return {"detail": "Notifications read successfully"}


async def get_notification(db: AsyncSession, notification_id: UUID):
    result = await db.execute(
        select(models.Notification).where(models.Notification.id == notification_id)
    )
    return result.scalars().first()


async def create_notification(db: AsyncSession, user_id: UUID, message: str):
    db_notification = models.Notification(user_id=user_id, message=message)
    db.add(db_notification)
    await db.commit()
    await db.refresh(db_notification)
    return db_notification


async def patch_notification(db: AsyncSession, notification_id: UUID):
    notification = await get_notification(db, notification_id)
    if not notification:
        return None
    
    setattr(notification, "status", models.NotificationStatus.READ.value)
    db.add(notification)
    await db.commit()
    await db.refresh(notification)
    return {"detail": "Notification read successfully"}


async def delete_notification(db: AsyncSession, notification_id: UUID):
    notification = get_notification(db, notification_id)
    if not notification:
        return None

    await db.delete(notification)
    await db.commit()
    return {"detail": "Notification deleted successfully"}
