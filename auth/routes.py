from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db

from .crud import get_users, get_user, get_user_by_email, create_user, update_user, delete_user
from .schemas import User, UserCreate, UserSignin, UserUpdate, Token
from .utils import create_access_token, verify_password

router = APIRouter()

@router.post("/token", status_code=status.HTTP_200_OK, response_model=Token)
async def signin(user: UserSignin, db: AsyncSession = Depends(get_db)):
    db_user = await get_user_by_email(db, user.email)
    if not db_user or not verify_password(user.password, str(db_user.password)):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials")

    access_token = create_access_token(
        data={"user": User(
            id=db_user.id,
            email=db_user.email,
            first_name=str(db_user.first_name),
            last_name=str(db_user.last_name),
            is_active=bool(db_user.is_active),
            is_staff=bool(db_user.is_staff)
        )}
    )
    return Token(access_token=access_token, token_type='Bearer')

@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def create_new_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    existing_user = await get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="user with that email already exists"
        )

    db_user = await create_user(db, user)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error creating account")

    return {"detail": "Account created successfully"}


@router.get("/users", response_model=List[User], status_code=status.HTTP_200_OK)
async def read_users(db: AsyncSession = Depends(get_db), offset: int | None = None, limit: int | None = None):
    users = await get_users(db, offset, limit)
    return users


@router.get("/users/{user_id}", response_model=User, status_code=status.HTTP_200_OK)
async def read_user(user_id: UUID, db: AsyncSession = Depends(get_db)):
    user = await get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
    return user


@router.put("/user/{user_id}", response_model=User, status_code=status.HTTP_200_OK)
async def update_user_info(user_id: UUID, user_update: UserUpdate, db: AsyncSession = Depends(get_db)):
    updated_user = await update_user(db, user_id, user_update)
    if not updated_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
    return updated_user


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_info(user_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await delete_user(db, user_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
    return result
