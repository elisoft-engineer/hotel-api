from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from reviews import models, schemas

async def get_reviews(
    db: AsyncSession, menu_id: UUID, offset: int | None = None, limit: int | None = None
):
    results = await db.execute(
        select(models.Review).where(
            models.Review.menu_id == menu_id).offset(offset).limit(limit)
        )
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
