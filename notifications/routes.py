from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from notifications.crud import (
    delete_notification,
    get_notification,
    get_notifications,
    patch_notification,
    patch_notifications,
)
from notifications.models import NotificationStatus
from notifications.schemas import Notification

router = APIRouter(prefix="/notifications", tags=["notifications"])

@router.get("", response_model=List[Notification], status_code=status.HTTP_200_OK)
async def retrieve_notifications(
    notification_status: str | None = None,
    user_id: UUID = Depends(),  # TODO: implememnt the middlewares
    db: AsyncSession = Depends(get_db),
    offset: int | None = None,
    limit: int | None = None
):
    model_notification_status = NotificationStatus(notification_status) \
        if notification_status in [s.value for s in NotificationStatus] else None
    notifications = await get_notifications(db, user_id, model_notification_status, offset, limit)
    return notifications


@router.patch("", status_code=status.HTTP_200_OK)
async def mark_all_notifications_as_read(
    user_id: UUID | None = None, db: AsyncSession = Depends(get_db)
):
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Permission denied"
        )
    return await patch_notifications(db, user_id)


@router.patch("/{notification_id}", status_code=status.HTTP_200_OK)
async def mark_notification_as_read(
    notification_id: UUID, user_id: UUID = Depends(), db: AsyncSession = Depends(get_db)
):
    notification = await get_notification(db, notification_id)
    if not notification:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notification not found")
    if not user_id or notification.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Permission denied")
    return await patch_notification(db, notification_id)


@router.delete("/{notification_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_notification_info(
    notification_id: UUID, user_id: UUID | None = None, db: AsyncSession = Depends(get_db)
):
    notification = await get_notification(db, notification_id)
    if not notification:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notification not found")
    if not user_id or notification.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Permission denied")
    return await delete_notification(db, notification_id)
