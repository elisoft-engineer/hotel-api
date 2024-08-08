from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID
from db.models import orders as models
from db.schemas import orders as schemas
from db.models.enums import OrderStatus


async def get_orders(db: AsyncSession, offset: int | None = None, limit: int | None = None):
    results = await db.execute(select(models.Order).offset(offset).limit(limit))
    return results.scalars().all()


async def get_customer_orders(
    db: AsyncSession,
    customer_id: UUID,
    offset: int | None = None,
    limit: int | None = None
):
    results = await db.execute(
        select(models.Order).where(models.Order.customer_id == customer_id).offset(offset).limit(limit)
    )
    return results.scalars().all()


async def get_order(db: AsyncSession, order_id: UUID):
    result = await db.execute(select(models.Order).where(models.Order.id == order_id))
    return result.scalars().first()


async def create_order(db: AsyncSession, order: schemas.OrderCreate):
    order_data = order.model_dump()
    # I need to check out how to create all the relationship of order <-> menu items


# The update crud only updates the order status
async def update_order(db: AsyncSession, order_id: UUID, order_status: OrderStatus):
    order = await get_order(db, order_id)
    if not order:
        return None
    
    setattr(order, "status", order_status)
    db.add(order)
    await db.commit()
    await db.refresh(order)
    return order


async def delete_order(db: AsyncSession, order_id: UUID):
    order = await get_order(db, order_id)
    if not order:
        return None
    
    await db.delete(order)
    await db.commit()
    return {"message": "Order deleted successfully"}
