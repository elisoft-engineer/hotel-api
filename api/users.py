from fastapi import APIRouter, Depends, status, HTTPException
from db.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from db.schemas.users import Customer, Admin, CustomerUpdate, AdminUpdate
from typing import List
from uuid import UUID
from db.crud.users import get_customers, get_customer, update_customer, delete_customer, get_admins, get_admin, update_admin, delete_admin


router = APIRouter()

# Customer routes

@router.get("/customers", response_model=List[Customer], status_code=status.HTTP_200_OK)
async def read_customers(db: AsyncSession = Depends(get_db), offset: int | None = None, limit: int | None = None):
    customers = await get_customers(db, offset, limit)
    return customers


@router.get("/customers/{id}", response_model=Customer, status_code=status.HTTP_200_OK)
async def read_customer(id: UUID, db: AsyncSession = Depends(get_db)):
    customer = await get_customer(db, id)
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    return customer


@router.put("/customer/{id}", response_model=Customer, status_code=status.HTTP_200_OK)
async def update_customer_info(id: UUID, customer_update: CustomerUpdate, db: AsyncSession = Depends(get_db)):
    updated_customer = await update_customer(db, id, customer_update)
    if not updated_customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    return updated_customer


@router.delete("/customers/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_customer_info(id: UUID, db: AsyncSession = Depends(get_db)):
    result = await delete_customer(db, id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    return result


# Admin routes

@router.get("/admins", response_model=List[Admin], status_code=status.HTTP_200_OK)
async def read_admins(db: AsyncSession = Depends(get_db), offset: int | None = None, limit: int | None = None):
    admins = await get_admins(db, offset, limit)
    return admins


@router.get("/admins/{id}", response_model=Admin, status_code=status.HTTP_200_OK)
async def read_admin(id: UUID, db: AsyncSession = Depends(get_db)):
    admin = get_admin(db, id)
    if not admin:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Admin not found")
    return admin


@router.put("/admins/{id}", response_model=Admin, status_code=status.HTTP_200_OK)
async def update_admin_info(id: UUID, admin_update: AdminUpdate, db: AsyncSession = Depends(get_db)):
    updated_admin = await update_admin(db, id, admin_update)
    if not updated_admin:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Admin not found")
    return updated_admin


@router.delete("/admins/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_admin_info(id: UUID, db: AsyncSession = Depends(get_db)):
    result = await delete_admin(db, id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Admin not found")
    return result
