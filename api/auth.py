from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.security import create_access_token, verify_password
from db.crud.users import (
    create_admin,
    create_customer,
    get_admin_by_email,
    get_customer_by_email,
)
from db.schemas.auth import Token
from db.schemas.users import (
    Admin,
    AdminCreate,
    AdminSignin,
    Customer,
    CustomerCreate,
    CustomerSignin,
)
from db.session import get_db

router = APIRouter()

"""
This file handles all the endpoints for user account creation and signin
"""

@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def create_new_customer(customer: CustomerCreate, db: AsyncSession = Depends(get_db)):
    existing_customer = await get_customer_by_email(db, customer.email)
    if existing_customer:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Customer with that email already exists"
        )

    db_customer = await create_customer(db, customer)
    if not db_customer:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error creating account")

    return {"detail": "Account created successfully"}


@router.post("/signin", status_code=status.HTTP_200_OK, response_model=Token)
async def signin(customer: CustomerSignin, db: AsyncSession = Depends(get_db)):
    db_customer = await get_customer_by_email(db, customer.email)
    if not db_customer or not verify_password(customer.password, db_customer.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = create_access_token(
        data={"user": Customer(
            id=db_customer.id,
            email=db_customer.email,
            first_name=str(db_customer.first_name),
            last_name=str(db_customer.last_name),
            is_active=bool(db_customer.is_active),
            user_type=str(db_customer.user_type)
        )}
    )
    return {"access_token": access_token, "token_type": "Bearer"}


@router.post("/admin/signup", status_code=status.HTTP_201_CREATED)
async def create_new_admin(admin: AdminCreate, db: AsyncSession = Depends(get_db)):
    existing_admin = await get_admin_by_email(db, admin.email)
    if existing_admin:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Admin with that email already exists"
        )

    db_admin = await create_admin(db, admin)
    if not db_admin:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating account"
        )

    return {"detail": "Account created successfully"}


@router.post("/admin/signin", response_model=Token, status_code=status.HTTP_200_OK)
async def admin_signin(admin: AdminSignin, db: AsyncSession = Depends(get_db)):
    db_admin = await get_admin_by_email(db, admin.email)
    if not db_admin or not verify_password(admin.password, db_admin.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    access_token = create_access_token(data={"user": db_admin})
    return {"access_token": access_token, "token_type": "Bearer"}
