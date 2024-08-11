from fastapi import APIRouter, Depends, status, HTTPException
from db.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from db.crud.notifications import create_notification, get_notifications, \
    patch_notifications, patch_notification, get_notification, delete_notification
from db.schemas.notifications import Notification, NotificationCreate
from typing import List
from uuid import UUID

router = APIRouter(prefix="/notifications", tags=["notifications"])

"""
This file handles the api endpoints for notifications
"""


# Creation of the notifications
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_new_notification(notification: NotificationCreate, db: AsyncSession = Depends(get_db)):
    db_notification = await create_notification(db, notification)
    if not db_notification:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error creating notification")
    return {"detail": "Notification created successfully"}


# Getting the user notifications whether unread or all of them, with pagination through offset and limit.
@router.get("/", response_model=List[Notification], status_code=status.HTTP_200_OK)
async def read_user_notifications(
        user_id: UUID | None = None,
        notification_status: str | None = None,
        db: AsyncSession = Depends(get_db),
        offset: int | None = None,
        limit: int | None = None
):
    notifications = await get_notifications(db, user_id, notification_status, offset, limit)
    return notifications


# Marking all user notifications as read
@router.patch("/", response_model=List[Notification], status_code=status.HTTP_200_OK)
async def mark_user_notifications_as_read(user_id: UUID | None = None, db: AsyncSession = Depends(get_db)):
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Permission denied")
    return await mark_all_notifications_as_read(db, user_id)


# Marking one notification as read
@router.patch("/{notification_id}", status_code=status.HTTP_200_OK)
async def mark_user_notification_as_read(
        notification_id: UUID,
        user_id: UUID | None = None,
        db: AsyncSession = Depends(get_db)
):
    notification = await get_notification(db, notification_id)
    if not notification:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notification not found")
    if not user_id or notification.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Permission denied")
    return await mark_notification_as_read(db, notification_id)


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
