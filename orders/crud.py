from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from menu.crud import get_menu_item
from orders import models, schemas


async def get_orders(
    db: AsyncSession,
    user_id: UUID | None = None,
    order_status: models.OrderStatus | None = None,
    offset: int | None = None,
    limit: int | None = None
):
    if user_id:
        if order_status:
            results = await db.execute(
                select(models.Order).where(
                    models.Order.user_id == user_id and models.Order.status == order_status)
                    .offset(offset).limit(limit)
            )
        else:
            results = await db.execute(
                select(models.Order).where(models.Order.user_id == user_id).offset(offset).limit(limit)
            )
    else:
        if order_status and order_status in [status.value for status in models.OrderStatus]:
            results = await db.execute(
                select(models.Order).where(models.Order.status == order_status).offset(offset).limit(limit)
            )
        else:
            results = await db.execute(select(models.Order).offset(offset).limit(limit))
    return results.scalars().all()


async def get_order(db: AsyncSession, order_id: UUID):
    result = await db.execute(select(models.Order).where(models.Order.id == order_id))
    return result.scalars().first()


async def create_order(db: AsyncSession, order: schemas.OrderCreate):
    db_order = models.Order(user_id=order.user_id)
    db.add(db_order)
    await db.commit()
    await db.refresh(db_order)

    total_amount = 0
    for item_id in order.item_ids:
        menu_item = await get_menu_item(db, item_id)
        if menu_item:
            db_order.items.append(menu_item)
            total_amount += menu_item.price
    
    db_order.amount = total_amount
    db.add(db_order)
    await db.commit()
    await db.refresh(db_order)
    return db_order


async def update_order(
    db: AsyncSession, order_id: UUID, order_status: models.OrderStatus | None = None
):
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
    return {"detail": "Order deleted successfully"}
