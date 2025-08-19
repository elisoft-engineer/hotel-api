import shutil
from decimal import Decimal
from os import path
from typing import List
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from PIL import Image
from sqlalchemy.ext.asyncio import AsyncSession

from core.conf import settings
from core.database import get_db
from menu.crud import create_menu, delete_menu, get_menu, get_menu_item, update_menu
from menu.models import MenuCategory
from menu.schemas import Menu, MenuCreate, MenuUpdate
from menu.utils import generate_unique_filename

router = APIRouter(prefix="/menu", tags=["menu"])


@router.get("", response_model=List[Menu], status_code=status.HTTP_200_OK)
async def retrieve_menu(
    db: AsyncSession = Depends(get_db), offset: int | None = None, limit: int | None = None
):
    menu = await get_menu(db, offset, limit)
    return menu

THUMB_WIDTH = 300
RETINA_FACTOR = 1
JPEG_QUALITY = 80
WEBP_QUALITY = 80

@router.post("", status_code=status.HTTP_201_CREATED)
async def create_new_menu_item(
    name: str = Form(...),
    description: str = Form(...),
    price: Decimal = Form(...),
    category: MenuCategory = Form(...),
    image: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):
    image_filename = generate_unique_filename(image.filename)
    image_path = path.join(settings.MENU_IMAGES_DIR, image_filename)

    # stream-save the uploaded file to disk to avoid loading whole file into memory
    with open(image_path, "wb") as image_buffer:
        image_buffer.write(image.file.read())

    # generate thumbnail(s)
    with Image.open(image_path) as img:
        if img.mode not in ("RGB", "L"):
            img = img.convert("RGB")

        aspect = img.width / img.height
        thumb_w = THUMB_WIDTH
        thumb_h = int(round(thumb_w / aspect))
        thumb_filename = f"thumb_{image_filename}"
        thumb_path = path.join(settings.MENU_THUMBNAILS_DIR, thumb_filename)
        thumb = img.copy()
        thumb = thumb.resize((thumb_w, thumb_h), resample=Image.Resampling.LANCZOS)

        thumb.save(thumb_path, format="JPEG", quality=JPEG_QUALITY, optimize=True)
    
    menu = MenuCreate(
        name=name,
        description=description,
        price=price,
        category=category,
        image=image_path,
        thumbnail=thumb_path
    )

    db_menu = await create_menu(db, menu)
    if not db_menu:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating menu item"
        )
    return {"detail": "Menu item created successfully"}


@router.get("/{menu_id}", response_model=Menu, status_code=status.HTTP_200_OK)
async def retrieve_menu_item(menu_id: UUID, db: AsyncSession = Depends(get_db)):
    menu_item = await get_menu_item(db, menu_id)
    if not menu_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Menu item not found"
        )
    return menu_item


@router.put("/{menu_id}", response_model=Menu, status_code=status.HTTP_200_OK)
async def update_menu_item(
    menu_id: UUID,
    name: str = Form(...),
    description: str = Form(...),
    price: Decimal = Form(...),
    category: MenuCategory = Form(...),
    image: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):
    update_data = MenuUpdate(
        name=name,
        description=description,
        price=price,
        category=category,
        image=None,
        thumbnail=None
    )

    if image:
        image_filename = generate_unique_filename(image.filename)
        image_path = path.join(settings.MENU_IMAGES_DIR, image_filename)

        # stream-save the uploaded file to disk to avoid loading whole file into memory
        with open(image_path, "wb") as image_buffer:
            image_buffer.write(image.file.read())

        # generate thumbnail(s)
        with Image.open(image_path) as img:
            if img.mode not in ("RGB", "L"):
                img = img.convert("RGB")

            aspect = img.width / img.height
            thumb_w = THUMB_WIDTH
            thumb_h = int(round(thumb_w / aspect))
            thumb_filename = f"thumb_{image_filename}"
            thumb_path = path.join(settings.MENU_THUMBNAILS_DIR, thumb_filename)
            thumb = img.copy()
            thumb = thumb.resize((thumb_w, thumb_h), resample=Image.Resampling.LANCZOS)

            thumb.save(thumb_path, format="JPEG", quality=JPEG_QUALITY, optimize=True)

            update_data.image = image_path
            update_data.thumbnail = thumb_path

    updated_menu_item = await update_menu(db, menu_id, update_data)
    if not updated_menu_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Menu item not found"
        )
    return updated_menu_item


@router.delete("/{menu_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_menu_item(menu_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await delete_menu(db, menu_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Menu item not found"
        )
    return result
