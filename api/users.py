from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from db.crud.users import (
    delete_admin,
    delete_customer,
    get_admin,
    get_admins,
    get_customer,
    get_customers,
    update_admin,
    update_customer,
)
from db.schemas.users import Admin, AdminUpdate, Customer, CustomerUpdate
from db.session import get_db

router = APIRouter(tags=["users"])


# Customer routes

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
