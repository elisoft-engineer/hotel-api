from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID

from auth.crud import (
    create_admin,
    create_customer,
    get_admin_by_email,
    get_customer_by_email,
    delete_admin,
    delete_customer,
    get_admin,
    get_admins,
    get_customer,
    get_customers,
    update_admin,
    update_customer,
)
from auth.schemas import Token
from auth.schemas import (
    Admin,
    AdminCreate,
    AdminUpdate,
    AdminSignin,
    Customer,
    CustomerCreate,
    CustomerUpdate,
    CustomerSignin,
)
from core.database import get_db
from core.security import create_access_token, verify_password

router = APIRouter()

"""
This file handles all the endpoints for user account creation and signin
"""

@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def create_new_customer(customer: CustomerCreate, db: AsyncSession = Depends(get_db)):
    existing_customer = await get_customer_by_email(db, customer.email)
    if existing_customer:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
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
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials")

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
            status_code=status.HTTP_400_BAD_REQUEST,
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
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid credentials"
        )

    access_token = create_access_token(data={"user": db_admin})
    return {"access_token": access_token, "token_type": "Bearer"}


@router.get("/customers", response_model=List[Customer], status_code=status.HTTP_200_OK)
async def read_customers(db: AsyncSession = Depends(get_db), offset: int | None = None, limit: int | None = None):
    customers = await get_customers(db, offset, limit)
    return customers


@router.get("/customers/{customer_id}", response_model=Customer, status_code=status.HTTP_200_OK)
async def read_customer(customer_id: UUID, db: AsyncSession = Depends(get_db)):
    customer = await get_customer(db, customer_id)
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    return customer


@router.put("/customer/{customer_id}", response_model=Customer, status_code=status.HTTP_200_OK)
async def update_customer_info(customer_id: UUID, customer_update: CustomerUpdate, db: AsyncSession = Depends(get_db)):
    updated_customer = await update_customer(db, customer_id, customer_update)
    if not updated_customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    return updated_customer


@router.delete("/customers/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_customer_info(customer_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await delete_customer(db, customer_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    return result


# Admin routes

@router.get("/admins", response_model=List[Admin], status_code=status.HTTP_200_OK)
async def read_admins(db: AsyncSession = Depends(get_db), offset: int | None = None, limit: int | None = None):
    admins = await get_admins(db, offset, limit)
    return admins


@router.get("/admins/{admin_id}", response_model=Admin, status_code=status.HTTP_200_OK)
async def read_admin(admin_id: UUID, db: AsyncSession = Depends(get_db)):
    admin = await get_admin(db, admin_id)
    if not admin:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Admin not found")
    return admin


@router.put("/admins/{admin_id}", response_model=Admin, status_code=status.HTTP_200_OK)
async def update_admin_info(admin_id: UUID, admin_update: AdminUpdate, db: AsyncSession = Depends(get_db)):
    updated_admin = await update_admin(db, admin_id, admin_update)
    if not updated_admin:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Admin not found")
    return updated_admin


@router.delete("/admins/{admin_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_admin_info(admin_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await delete_admin(db, admin_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Admin not found")
    return result

