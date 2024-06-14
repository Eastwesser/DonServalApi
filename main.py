import os
import shutil

from fastapi import FastAPI, Depends, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from schemas_dir.schemas import Donut, DonutCreate
from sqlalchemy.orm import Session

from database_dir.database import engine, get_db
from models_dir.models import Base, Donut as DonutModel

app = FastAPI()

Base.metadata.create_all(bind=engine)

IMAGES_DIR = "images"
if not os.path.exists(IMAGES_DIR):
    os.makedirs(IMAGES_DIR)


@app.post("/donuts/", response_model=Donut)
def create_donut(donut: DonutCreate, db: Session = Depends(get_db)):
    db_donut = DonutModel(name=donut.name, description=donut.description)
    db.add(db_donut)
    db.commit()
    db.refresh(db_donut)
    return db_donut


@app.post("/donuts/{donut_id}/upload-image/")
def upload_image(donut_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    db_donut = db.query(DonutModel).filter(DonutModel.id == donut_id).first()
    if db_donut is None:
        raise HTTPException(status_code=404, detail="Donut not found")

    file_location = f"{IMAGES_DIR}/{donut_id}.jpg"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    db_donut.image_path = file_location
    db.commit()
    db.refresh(db_donut)
    return {"info": "Image uploaded successfully"}


@app.get("/donuts/{donut_id}", response_model=Donut)
def get_donut(donut_id: int, db: Session = Depends(get_db)):
    db_donut = db.query(DonutModel).filter(DonutModel.id == donut_id).first()
    if db_donut is None:
        raise HTTPException(status_code=404, detail="Donut not found")

    return db_donut


@app.get("/donuts/{donut_id}/image")
def get_image(donut_id: int, db: Session = Depends(get_db)):
    db_donut = db.query(DonutModel).filter(DonutModel.id == donut_id).first()
    if db_donut is None or db_donut.image_path is None:
        raise HTTPException(status_code=404, detail="Image not found")

    return FileResponse(db_donut.image_path)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
