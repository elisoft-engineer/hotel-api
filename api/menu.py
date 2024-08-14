from fastapi import APIRouter, Depends, status, HTTPException, Form, UploadFile, File
from db.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from db.crud.menu import get_menu, create_menu, get_menu_item, update_menu, delete_menu, get_reviews, get_review, \
    create_review, update_review, delete_review
from db.schemas.menu import Menu, MenuCreate, MenuUpdate, Review, ReviewCreate, ReviewUpdate
from typing import List
from decimal import Decimal
from uuid import UUID, uuid4
from PIL import Image
from os import path
from core.config import settings

router = APIRouter(prefix="/menu", tags=["menu"])

"""
The following are the api endpoints associated with the menu.
"""


@router.get("/", response_model=List[Menu], status_code=status.HTTP_200_OK)
async def read_menu(db: AsyncSession = Depends(get_db), offset: int | None = None, limit: int | None = None):
    menu = await get_menu(db, offset, limit)
    return menu

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_new_menu_item(
        name: str = Form(...),
        description: str = Form(...),
        price: Decimal = Form(...),
        category: str = Form(...),
        image: UploadFile = File(...),
        db: AsyncSession = Depends(get_db)
):
    # Rename the image to avoid conflicts during writing in the file system
    image_filename = f"{uuid4().hex}_{image.filename}"
    image_path = path.join(settings.MENU_IMAGES_DIR, image_filename)

    # Save the image
    with open(image_path, "wb") as image_buffer:
        image_buffer.write(image.file.read())

    # Generate thumbnail and save it
    with Image.open(image_path) as img:
        thumbnail_filename = f"thumb_{uuid4().hex}_{image_filename}"
        thumbnail_path = path.join(settings.MENU_THUMBNAILS_DIR, thumbnail_filename)
        aspect_ratio = img.size[0] / img.size[1]
        output_width = 300
        img.thumbnail((output_width, output_width * aspect_ratio))
        img.save(thumbnail_path)

    # Create the menu_create obj and parse it to create_menu
    menu = MenuCreate(
        name=name,
        description=description,
        price=price,
        category=category,
        image=image_path,
        thumbnail=thumbnail_path
    )

    db_menu = await create_menu(db, menu)
    if not db_menu:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error creating menu item")
    return {"detail": "Menu item created successfully"}


@router.get("/{menu_id}", response_model=Menu, status_code=status.HTTP_200_OK)
async def read_menu_item(menu_id: UUID, db: AsyncSession = Depends(get_db)):
    menu_item = await get_menu_item(db, menu_id)
    if not menu_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Menu item not found")
    return menu_item


@router.put("/{menu_id}", response_model=Menu, status_code=status.HTTP_200_OK)
async def update_menu_item_info(menu_id: UUID, menu_update: MenuUpdate, db: AsyncSession = Depends(get_db)):
    updated_menu_item = update_menu(db, menu_id, menu_update)
    if not updated_menu_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Menu item not found")
    return updated_menu_item


@router.delete("/{menu_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_menu_item_info(menu_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await delete_menu(db, menu_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Menu item not found")
    return result


"""
The following are the api endpoints associated with the menu reviews.
"""


@router.get("/{menu_id}/reviews", response_model=List[Review], status_code=status.HTTP_200_OK)
async def read_menu_item_reviews(
        menu_id: UUID, db: AsyncSession = Depends(get_db), offset: int | None = None, limit: int | None = None
):
    reviews = get_reviews(db, menu_id, offset, limit)
    return reviews


"""
As for the creation of reviews, I shall work on the scenario where a customer had previously reviewed an menu
item. We can maybe update the existing one or otherwise. As of the time of this docstring, the ReviewCreate and
ReviewUpdate are quite different, thus I am going to create the two endpoints independent of each other.
"""


@router.post("/{menu_id}/reviews", status_code=status.HTTP_201_CREATED)
async def create_new_review(review: ReviewCreate, db: AsyncSession = Depends(get_db)):
    db_review = await create_review(db, review)
    if not db_review:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error creating review")
    return {"detail": "Review created successfully"}


@router.get("/{menu_id}/reviews/{review_id}", response_model=Review, status_code=status.HTTP_200_OK)
async def read_review(menu_id: UUID, review_id: UUID, db: AsyncSession = Depends(get_db)):
    review = await get_review(db, review_id)
    if not review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")
    if menu_id != review.menu_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error in the details")
    return review


@router.put("/{menu_id}/reviews/{review_id}", response_model=Review, status_code=status.HTTP_200_OK)
async def update_review_info(
        menu_id: UUID, review_id: UUID, review_update: ReviewUpdate, db: AsyncSession = Depends(get_db)
):
    review = await get_review(db, review_id)
    if not review or review.menu_id != menu_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong review id or menu id")
    updated_review = await update_review(db, review_id, review_update)
    if not updated_review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")
    return updated_review


@router.delete("/{menu_id}/reviews/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_review_info(menu_id: UUID, review_id: UUID, db: AsyncSession = Depends(get_db)):
    review = await get_review(db, review_id)
    if not review or review.menu_id != menu_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong review id or menu id")
    result = await delete_review(db, review_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")
    return result
