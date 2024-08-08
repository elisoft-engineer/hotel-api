from fastapi import APIRouter, Depends, status, HTTPException
from db.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from db.crud.messages import create_message, get_message, get_messages, delete_message
from db.schemas.messages import Message, MessageCreate
from typing import List
from uuid import UUID

router = APIRouter(prefix="/messages", tags=["messages"])

"""
This file handles the api endpoints for messages
"""


@router.get("/", response_model=List[Message], status_code=status.HTTP_200_OK)
async def read_messages(db: AsyncSession = Depends(get_db), offset: int | None = None, limit: int | None = None):
    messages = await get_messages(db, offset, limit)
    return messages


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_new_message(message: MessageCreate, db: AsyncSession = Depends(get_db)):
    db_message = await create_message(db, message)
    if not db_message:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error creating message")
    return {"detail": "Message created successfully"}


@router.get("/{message_id}", response_model=Message, status_code=status.HTTP_200_OK)
async def read_message(message_id: UUID, db: AsyncSession = Depends(get_db)):
    message = await get_message(db, message_id)
    if not message:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message not found")
    return message


@router.delete("/{message_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_message_info(message_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await delete_message(db, message_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message not found")
    return result
