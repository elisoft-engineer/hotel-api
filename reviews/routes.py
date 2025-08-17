from typing import List
from uuid import UUID

from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from reviews.crud import get_reviews, get_review, create_review, update_review, delete_review
from reviews.schemas import Review, ReviewCreate, ReviewUpdate


router = APIRouter(prefix="/menu/{menu_id}/reviews", tags=["reviews"])

@router.get("", response_model=List[Review], status_code=status.HTTP_200_OK)
async def read_menu_item_reviews(
    menu_id: UUID, db: AsyncSession = Depends(get_db),
    offset: int | None = None,
    limit: int | None = None
):
    reviews = await get_reviews(db, menu_id, offset, limit)
    return reviews


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_new_review(review: ReviewCreate, db: AsyncSession = Depends(get_db)):
    db_review = await create_review(db, review)
    if not db_review:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error creating review"
        )
    return {"detail": "Review created successfully"}


@router.get("/{review_id}", response_model=Review, status_code=status.HTTP_200_OK)
async def read_review(menu_id: UUID, review_id: UUID, db: AsyncSession = Depends(get_db)):
    review = await get_review(db, review_id)
    if not review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")
    if menu_id != review.menu_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error in the details")
    return review


@router.put("/{review_id}", response_model=Review, status_code=status.HTTP_200_OK)
async def update_review_info(
    menu_id: UUID, review_id: UUID, review_update: ReviewUpdate, db: AsyncSession = Depends(get_db)
):
    review = await get_review(db, review_id)
    if not review or review.menu_id != menu_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong review id or menu id"
        )
    updated_review = await update_review(db, review_id, review_update)
    if not updated_review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")
    return updated_review


@router.delete("/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_review_info(menu_id: UUID, review_id: UUID, db: AsyncSession = Depends(get_db)):
    review = await get_review(db, review_id)
    if not review or review.menu_id != menu_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong review id or menu id"
        )
    result = await delete_review(db, review_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")
    return result
