from fastapi import HTTPException
from sqlalchemy.orm import Session

from api.models_dir.models import Donut as DonutModel
from api.schemas_dir.schemas import DonutCreate, DonutUpdate


def create_donut(db: Session, donut: DonutCreate):
    db_donut = DonutModel(name=donut.name, description=donut.description, price=donut.price)
    db.add(db_donut)
    db.commit()
    db.refresh(db_donut)
    return db_donut


def get_donut(db: Session, donut_id: int):
    db_donut = db.query(DonutModel).filter(DonutModel.id == donut_id).first()
    if db_donut is None:
        raise HTTPException(status_code=404, detail="Donut not found")
    return db_donut


def update_donut(db: Session, donut_id: int, donut: DonutUpdate):
    db_donut = db.query(DonutModel).filter(DonutModel.id == donut_id).first()
    if db_donut is None:
        raise HTTPException(status_code=404, detail="Donut not found")

    for key, value in donut.dict(exclude_unset=True).items():
        setattr(db_donut, key, value)

    db.commit()
    db.refresh(db_donut)
    return db_donut


def delete_donut(db: Session, donut_id: int):
    db_donut = db.query(DonutModel).filter(DonutModel.id == donut_id).first()
    if db_donut is None:
        raise HTTPException(status_code=404, detail="Donut not found")
    db.delete(db_donut)
    db.commit()
    return {"message": "Donut deleted successfully"}
