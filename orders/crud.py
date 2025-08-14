from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from orders import models, schemas

from menu.crud import get_menu_item

async def get_orders(
        db: AsyncSession,
        customer_id: UUID,
        order_status: str | None = None,
        offset: int | None = None,
        limit: int | None = None
):
    # this block is executed when a customer id is parsed
    if customer_id:
        # if the order status is parsed, filter the order list using the status provided
        if order_status and order_status in [status.value for status in models.OrderStatus]:
            results = await db.execute(
                select(models.Order).where(
                    models.Order.customer_id == customer_id and models.Order.status == order_status).offset(
                    offset).limit(limit)
            )
        else:
            # where the order status is not provided, return all the customer orders
            results = await db.execute(
                select(models.Order).where(models.Order.customer_id == customer_id).offset(offset).limit(limit)
            )
    else:
        # where there is no specified customer and the order status is parsed
        if order_status and order_status in [status.value for status in models.OrderStatus]:
            results = await db.execute(
                select(models.Order).where(models.Order.status == order_status).offset(offset).limit(limit)
            )
        else:
            # no customer and no order status parsed ... return all the orders with pagination using offset and limit
            results = await db.execute(select(models.Order).offset(offset).limit(limit))
    return results.scalars().all()


# crud for getting a single order
async def get_order(db: AsyncSession, order_id: UUID):
    result = await db.execute(select(models.Order).where(models.Order.id == order_id))
    return result.scalars().first()


# crud for creating an order
async def create_order(db: AsyncSession, order: schemas.OrderCreate):
    # first create the order and add the details later
    db_order = models.Order(customer_id=order.customer_id)
    db.add(db_order)
    await db.commit()
    await db.refresh(db_order)

    # calculate the total amount
    total_amount = 0
    for item_id in order.item_ids:
        menu_item = await get_menu_item(db, item_id)
        # append the menu if and only if the menu item exists
        if menu_item:
            db_order.items.append(menu_item)
            total_amount += menu_item.price
    # update the amount
    db_order.amount = total_amount
    db.add(db_order)
    await db.commit()
    await db.refresh(db_order)
    return db_order


# The update crud only updates the order status
async def update_order(db: AsyncSession, order_id: UUID, order_status: str | None = None):
    order = await get_order(db, order_id)
    if not order or order_status not in [status.value for status in models.OrderStatus]:
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
