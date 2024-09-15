import os
import shutil

from fastapi import (
    FastAPI,
    Depends,
    File,
    UploadFile,
    HTTPException,
)
from fastapi.responses import FileResponse
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from api.crud.donut import (
    create_donut,
    delete_donut,
    get_donut,
)
from api.database.database import engine, get_db
from api.models.models import Base, Donut as DonutModel
from api.schemas.schemas import (
    Donut,
    DonutCreate,
    DonutUpdate,
)

app = FastAPI(
    title="DonServal API",
    description="Serval Donut API for the donut shop",
    version="1.0.0",
)

IMAGE_DIR = "api/images"
os.makedirs(IMAGE_DIR, exist_ok=True)

# Create the database tables if they don't exist
Base.metadata.create_all(bind=engine)


# POST /donuts/ - Create Donut
@app.post("/donuts/", response_model=Donut, tags=["Donuts"])
async def create_donut_endpoint(donut: DonutCreate, db: AsyncSession = Depends(get_db)):
    try:
        return await create_donut(db, donut)
    except SQLAlchemyError as e:
        print(f"Error creating donut: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


# POST /donuts/{donut_id}/upload-image/ - Upload Image
@app.post("/donuts/{donut_id}/upload-image/", tags=["Donuts"])
async def upload_image(donut_id: int, file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    db_donut = await get_donut(db, donut_id)
    if db_donut is None:
        raise HTTPException(status_code=404, detail="Donut not found")

    file_location = f"{IMAGE_DIR}/{donut_id}.png"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    db_donut.image_filename = file_location
    await db.commit()
    await db.refresh(db_donut)
    return {"info": "Image uploaded successfully"}


# GET /donuts/{donut_id} - Get Donut by ID
@app.get("/donuts/{donut_id}", response_model=Donut, tags=["Donuts"])
async def read_donut(donut_id: int, db: AsyncSession = Depends(get_db)):
    return await get_donut(db, donut_id)


# GET /donuts/{donut_id}/image - Get Donut Image by ID
@app.get("/donuts/{donut_id}/image", tags=["Donuts"])
async def get_image(donut_id: int, db: AsyncSession = Depends(get_db)):
    db_donut = await get_donut(db, donut_id)
    if db_donut is None or db_donut.image_filename is None:
        raise HTTPException(status_code=404, detail="Image not found")
    return FileResponse(db_donut.image_filename)


# PUT /donuts/{donut_id} - Update Donut
@app.put("/donuts/{donut_id}", response_model=Donut, tags=["Donuts"])
def update_donut_endpoint(donut_id: int, donut: DonutUpdate, db: Session = Depends(get_db)):
    db_donut = db.query(DonutModel).filter(DonutModel.id == donut_id).first()
    if db_donut is None:
        raise HTTPException(status_code=404, detail="Donut not found")

    update_data = donut.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_donut, key, value)

    db.commit()
    db.refresh(db_donut)
    return db_donut


# DELETE /donuts/{donut_id} - Delete Donut
@app.delete("/donuts/{donut_id}", tags=["Donuts"])
async def delete_donut_endpoint(donut_id: int, db: AsyncSession = Depends(get_db)):
    return await delete_donut(db, donut_id)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
    )
