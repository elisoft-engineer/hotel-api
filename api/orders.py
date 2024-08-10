from fastapi import APIRouter, Depends, HTTPException, status
from db.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from db.schemas.orders import Order, OrderCreate
from db.crud.orders import get_orders, get_order, create_order, complete_order, complete_orders, delete_order
from db.models.enums import OrderStatus
from uuid import UUID
from typing import List

router = APIRouter(prefix="/orders", tags=["orders"])

"""
The following are the api endpoints for orders
"""


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


@router.patch("/")
