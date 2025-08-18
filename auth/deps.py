from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from auth.crud import get_user_by_email
from auth.schemas import User
from auth.utils import decode_token
from core.database import get_db


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(
    token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)
) -> User:
    payload = decode_token(token)
    email = payload.get("user")["email"]
    user = get_user_by_email(db, email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Sign in to continue",
        )
    return user


async def staff_required(user: User = Depends(get_current_user)):
    if not user.is_staff:
        raise HTTPException(
            detail="Only staff can access this endpoint",
            status_code=status.HTTP_403_FORBIDDEN
        )
    return user


async def customer_required(user: User = Depends(get_current_user)):
    if user.is_staff:
        raise HTTPException(
            detail="Only customers can access this endpoint",
            status_code=status.HTTP_403_FORBIDDEN
        )
    return user


async def self_or_staff_required(user_id: UUID, user: User = Depends(get_current_user)):
    if not user.id == user_id or user.is_staff:
        raise HTTPException(
            detail="Permission Denied",
            status_code=status.HTTP_403_FORBIDDEN
        )
    return user
