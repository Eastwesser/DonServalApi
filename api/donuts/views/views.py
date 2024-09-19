import os
import shutil

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession

from ...core.db_helper import db_helper
from ..crud.donut import create_donut, get_donut_by_id, update_donut, delete_donut
from api.donuts.schemas.schemas import DonutCreate, DonutRead, DonutUpdate

router = APIRouter(tags=["Donuts"])

IMAGE_DIR = "images"
os.makedirs(IMAGE_DIR, exist_ok=True)


@router.post("/", response_model=DonutRead)
async def create_donut_endpoint(
        donut: DonutCreate,
        db: AsyncSession = Depends(db_helper.session_dependency)
):
    return await create_donut(db, donut)


@router.get("/{donut_id}", response_model=DonutRead)
async def read_donut(
        donut_id: int,
        db: AsyncSession = Depends(db_helper.session_dependency)
):
    return await get_donut_by_id(db, donut_id)


@router.put("/{donut_id}", response_model=DonutRead)
async def update_donut_endpoint(
        donut_id: int,
        donut: DonutUpdate,
        db: AsyncSession = Depends(db_helper.session_dependency)
):
    return await update_donut(db, donut_id, donut)


@router.delete("/{donut_id}")
async def delete_donut_endpoint(
        donut_id: int,
        db: AsyncSession = Depends(db_helper.session_dependency)
):
    await delete_donut(db, donut_id)
    return {"message": "Donut deleted successfully"}


@router.post("/{donut_id}/upload-image/")
async def upload_image(
        donut_id: int,
        file: UploadFile = File(...),
        db: AsyncSession = Depends(db_helper.session_dependency)
):
    db_donut = await get_donut_by_id(db, donut_id)
    file_location = f"{IMAGE_DIR}/{donut_id}.png"

    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    db_donut.image_filename = file_location
    await db.commit()
    await db.refresh(db_donut)
    return {"info": "Image uploaded successfully"}


@router.get("/{donut_id}/image")
async def get_image(
        donut_id: int,
        db: AsyncSession = Depends(db_helper.session_dependency)
):
    db_donut = await get_donut_by_id(db, donut_id)
    if db_donut.image_filename is None:
        raise HTTPException(status_code=404, detail="Image not found")
    return FileResponse(db_donut.image_filename)
