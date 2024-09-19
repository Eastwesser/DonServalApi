import shutil
from pathlib import Path
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from api.donuts.schemas.schemas import DonutCreate, DonutRead, DonutUpdate
from ..crud.donut import create_donut, get_donut_by_id, update_donut, delete_donut
from ...core.db_helper import db_helper

router = APIRouter(tags=["Donuts"])

IMAGE_DIR = Path("images")
IMAGE_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/", response_model=DonutRead)
async def create_donut_endpoint(
        donut: DonutCreate,
        session: AsyncSession = Depends(db_helper.session_dependency)
):
    return await create_donut(session, donut)


@router.get("/{donut_id}", response_model=DonutRead)
async def read_donut(
        donut_id: int,
        session: AsyncSession = Depends(db_helper.session_dependency)
):
    donut = await get_donut_by_id(session, donut_id)
    if not donut:
        raise HTTPException(status_code=404, detail="Donut not found")
    return donut


@router.put("/{donut_id}", response_model=DonutRead)
async def update_donut_endpoint(
        donut_id: int,
        donut: DonutUpdate,
        session: AsyncSession = Depends(db_helper.session_dependency)
):
    updated_donut = await update_donut(session, donut_id, donut)
    if not updated_donut:
        raise HTTPException(status_code=404, detail="Donut not found")
    return updated_donut


@router.delete("/{donut_id}")
async def delete_donut_endpoint(
        donut_id: int,
        session: AsyncSession = Depends(db_helper.session_dependency)
):
    success = await delete_donut(session, donut_id)
    if not success:
        raise HTTPException(status_code=404, detail="Donut not found")
    return {"message": "Donut deleted successfully"}


@router.post("/{donut_id}/upload-image/")
async def upload_image(
        donut_id: int,
        file: UploadFile = File(...),
        session: AsyncSession = Depends(db_helper.session_dependency)
):
    db_donut = await get_donut_by_id(session, donut_id)
    if not db_donut:
        raise HTTPException(status_code=404, detail="Donut not found")

    file_location = IMAGE_DIR / f"{donut_id}.png"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    db_donut.image_filename = str(file_location)
    await session.commit()
    await session.refresh(db_donut)
    return {"info": "Image uploaded successfully"}


@router.get("/{donut_id}/image")
async def get_image(
        donut_id: int,
        session: AsyncSession = Depends(db_helper.session_dependency)
):
    db_donut = await get_donut_by_id(session, donut_id)
    if not db_donut or not db_donut.image_filename:
        raise HTTPException(status_code=404, detail="Image not found")
    return FileResponse(db_donut.image_filename)
