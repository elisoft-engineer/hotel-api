from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from menu import models, schemas


async def get_menu(db: AsyncSession, offset: int | None = None, limit: int | None = None):
    results = await db.execute(select(models.Menu).offset(offset).limit(limit))
    return results.scalars().all()


async def get_menu_item(db: AsyncSession, menu_id: UUID):
    result = await db.execute(select(models.Menu).where(models.Menu.id == menu_id))
    return result.scalars().first()


async def create_menu(db: AsyncSession, menu: schemas.MenuCreate):
    menu_data = menu.model_dump()
    db_menu = models.Menu(**menu_data)
    db.add(db_menu)
    await db.commit()
    await db.refresh(db_menu)
    return db_menu


async def update_menu(db: AsyncSession, menu_id: UUID, menu_update: schemas.MenuUpdate):
    menu = await get_menu_item(db, menu_id)
    if not menu:
        return None

    update_data = menu_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(menu, key, value)

    db.add(menu)
    await db.commit()
    await db.refresh(menu)
    return menu


async def delete_menu(db: AsyncSession, menu_id: UUID):
    menu = await get_menu_item(db, menu_id)
    if not menu:
        return None

    await db.delete(menu)
    await db.commit()
    return {"detail": "Menu item deleted successfully"}
