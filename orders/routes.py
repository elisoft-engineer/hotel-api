from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from orders.crud import (
    create_order,
    delete_order,
    get_order,
    get_orders,
    update_order,
)
from orders.schemas import Order, OrderCreate
from core.database import get_db

"""
The following are the api endpoints for orders
"""

router = APIRouter(prefix="/orders", tags=["orders"])


@router.get("/", response_model=List[Order], status_code=status.HTTP_200_OK)
async def read_orders(
        customer_id: UUID | None = None,
        order_status: str | None = None,
        db: AsyncSession = Depends(get_db),
        offset: int | None = None,
        limit: int | None = None
):
    return await get_orders(db, customer_id, order_status, offset, limit)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_new_order(order: OrderCreate, db: AsyncSession = Depends(get_db)):
    db_order = await create_order(db, order)
    if not db_order:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error creating order")
    return {"detail": "Order created successfully"}


@router.get("/{order_id}", response_model=Order, status_code=status.HTTP_200_OK)
async def read_order(order_id: UUID, db: AsyncSession = Depends(get_db)):
    order = await get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return order


@router.patch("/{order_id}", response_model=Order, status_code=status.HTTP_200_OK)
async def update_order_info(
        order_id: UUID, order_status: str | None = None, db: AsyncSession = Depends(get_db)
):
    result = await update_order(db, order_id, order_status)
    if not result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Order status parameter wrong")
    return result


@router.delete("/{order_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order_info(order_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await delete_order(db, order_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return result
