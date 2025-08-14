from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from menu import models, schemas

"""
This file takes care of the menu db crud utilities that are used in the api endpoints
Exception handling is taken care of in the API endpoints since we cannot raise an
HTTPException from the crud utilities
"""

# These are the CRUD utilities for menu items

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


# These are the CRUD utilities for reviews

async def get_reviews(db: AsyncSession, menu_id: UUID, offset: int | None = None, limit: int | None = None):
    results = await db.execute(
        select(models.Review).where(models.Review.menu_id == menu_id).offset(offset).limit(limit))
    return results.scalars().all()


async def get_review(db: AsyncSession, review_id: UUID):
    result = await db.execute(select(models.Review).where(models.Review.id == review_id))
    return result.scalars().first()


async def create_review(db: AsyncSession, review: schemas.ReviewCreate):
    review_data = review.model_dump()
    db_review = models.Review(**review_data)
    db.add(db_review)
    await db.commit()
    await db.refresh(db_review)
    return db_review


async def update_review(db: AsyncSession, review_id: UUID, review_update: schemas.ReviewUpdate):
    review = await get_review(db, review_id)
    if not review:
        return None

    update_data = review_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(review, key, value)

    db.add(review)
    await db.commit()
    await db.refresh(review)
    return review


async def delete_review(db: AsyncSession, review_id: UUID):
    review = await get_review(db, review_id)
    if not review:
        return None

    await db.delete(review)
    await db.commit()
    return {"detail": "Review deleted successfully"}
