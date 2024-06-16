import os
import shutil

from fastapi import FastAPI, Depends, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from api.crud.donut import delete_donut, update_donut
from api.database_dir.database import engine, get_db
from api.models_dir.models import Base, Donut as DonutModel
from api.schemas_dir.schemas import Donut, DonutCreate, DonutUpdate

app = FastAPI()

IMAGE_DIR = "api/images"

# Check folder existence
os.makedirs(IMAGE_DIR, exist_ok=True)

# DB creation, if needed
Base.metadata.create_all(bind=engine)


# POST /donuts/ - Create Donut
@app.post("/donuts/", response_model=Donut)
def create_donut(donut: DonutCreate, db: Session = Depends(get_db)):
    try:
        db_donut = DonutModel(name=donut.name, description=donut.description, price=donut.price)
        db.add(db_donut)
        db.commit()
        db.refresh(db_donut)
        return db_donut
    except SQLAlchemyError as e:
        print(f"Error creating donut: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


# POST /donuts/{donut_id}/upload-image/ - Upload Image
@app.post("/donuts/{donut_id}/upload-image/")
def upload_image(donut_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    db_donut = db.query(DonutModel).filter(DonutModel.id == donut_id).first()
    if db_donut is None:
        raise HTTPException(status_code=404, detail="Donut not found")

    file_location = f"{IMAGE_DIR}/{donut_id}.png"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    db_donut.image_filename = file_location
    db.commit()
    db.refresh(db_donut)
    return {"info": "Image uploaded successfully"}


# GET /donuts/{donut_id} - Get Donut by ID
@app.get("/donuts/{donut_id}", response_model=Donut)
def get_donut(donut_id: int, db: Session = Depends(get_db)):
    db_donut = db.query(DonutModel).filter(DonutModel.id == donut_id).first()
    if db_donut is None:
        raise HTTPException(status_code=404, detail="Donut not found")

    return db_donut


# GET /donuts/{donut_id}/image - Get Donut Image by ID
@app.get("/donuts/{donut_id}/image")
def get_image(donut_id: int, db: Session = Depends(get_db)):
    db_donut = db.query(DonutModel).filter(DonutModel.id == donut_id).first()
    if db_donut is None or db_donut.image_filename is None:
        raise HTTPException(status_code=404, detail="Image not found")

    return FileResponse(db_donut.image_filename)


# PUT /donuts/{donut_id} - Update Donut
@app.put("/donuts/{donut_id}", response_model=Donut)
def update_donut_endpoint(donut_id: int, donut: DonutUpdate, db: Session = Depends(get_db)):
    return update_donut(db, donut_id, donut)


# DELETE /donuts/{donut_id} - Delete Donut
@app.delete("/donuts/{donut_id}")
def delete_donut_endpoint(donut_id: int, db: Session = Depends(get_db)):
    return delete_donut(db, donut_id)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
    )
