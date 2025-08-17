from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db

from .crud import get_users, get_user, get_user_by_email, create_user, update_user,\
    delete_user
from .schemas import RefreshRequest, TokenResponse, User, UserCreate, UserSignin,\
    UserUpdate, AuthResponse, VerifyRequest
from .utils import create_token, TokenType, verify_password, verify_token

token_router = APIRouter(prefix="/token", tags=["auth"])

@token_router.post("", status_code=status.HTTP_200_OK, response_model=AuthResponse)
async def signin(user: UserSignin, db: AsyncSession = Depends(get_db)):
    db_user = await get_user_by_email(db, user.email)
    if not db_user or not verify_password(user.password, str(db_user.password)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials"
        )
    
    data = {"user": User(
        id=db_user.id,
        email=db_user.email,
        first_name=str(db_user.first_name),
        last_name=str(db_user.last_name),
        is_active=bool(db_user.is_active),
        is_staff=bool(db_user.is_staff)
    )}

    access_token = create_token(TokenType.ACCESS, data)
    refresh_token = create_token(TokenType.REFRESH, {'sub': data['user'].id})

    return AuthResponse(
        access_token=access_token, refresh_token=refresh_token, token_type='Bearer'
    )


@token_router.post('/refresh', response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def refresh_access_token(payload: RefreshRequest, db: AsyncSession = Depends(get_db)):
    token = payload.refresh
    claims = verify_token(token, TokenType.REFRESH)
    user_id = claims.get('sub')
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload"
        )

    user = await get_user(db, user_id)
    if not user or not getattr(user, "is_active", True):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User inactive or not found"
        )
    
    access_payload = {"user": User(
        id=user.id,
        email=user.email,
        first_name=str(user.first_name),
        last_name=str(user.last_name),
        is_active=bool(user.is_active),
        is_staff=bool(user.is_staff)
    )}

    new_token = create_token(TokenType.ACCESS, access_payload)
    return TokenResponse(token=new_token, token_type='Bearer')


@token_router.post("/verify", status_code=status.HTTP_200_OK)
async def verify_refresh_token(payload: VerifyRequest):
    _ = verify_token(payload.refresh, TokenType.REFRESH)
    return Response(None, status.HTTP_200_OK)


user_router = APIRouter(prefix="/users", tags=["users"])

@user_router.post("", status_code=status.HTTP_201_CREATED)
async def create_new_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    existing_user = await get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="user with that email already exists"
        )

    db_user = await create_user(db, user)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error creating account"
        )

    return {"detail": "Account created successfully"}


@user_router.get("", response_model=List[User], status_code=status.HTTP_200_OK)
async def retrieve_user_list(
    db: AsyncSession = Depends(get_db), offset: int | None = None, limit: int | None = None
):
    users = await get_users(db, offset, limit)
    return users


@user_router.get("/{user_id}", response_model=User, status_code=status.HTTP_200_OK)
async def retrieve_user_info(user_id: UUID, db: AsyncSession = Depends(get_db)):
    user = await get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
    return user


@user_router.put("/{user_id}", response_model=User, status_code=status.HTTP_200_OK)
async def update_user_info(
    user_id: UUID, user_update: UserUpdate, db: AsyncSession = Depends(get_db)
):
    updated_user = await update_user(db, user_id, user_update)
    if not updated_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
    return updated_user


@user_router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_info(user_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await delete_user(db, user_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
    return result
