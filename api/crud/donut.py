from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from api.models.models import Donut as DonutModel
from api.schemas.schemas import DonutCreate, DonutUpdate


async def create_donut(db: AsyncSession, donut: DonutCreate):
    db_donut = DonutModel(name=donut.name, description=donut.description, price=donut.price)
    db.add(db_donut)
    await db.commit()
    await db.refresh(db_donut)
    return db_donut


async def get_donut(db: AsyncSession, donut_id: int):
    result = await db.execute(select(DonutModel).filter(DonutModel.id == donut_id))
    db_donut = result.scalar_one_or_none()
    if db_donut is None:
        raise HTTPException(status_code=404, detail="Donut not found")
    return db_donut


async def update_donut(db: AsyncSession, donut_id: int, donut: DonutUpdate):
    db_donut = await get_donut(db, donut_id)
    if db_donut is None:
        raise HTTPException(status_code=404, detail="Donut not found")

    for key, value in donut.model_dump(exclude_unset=True).items():
        setattr(db_donut, key, value)

    await db.commit()
    await db.refresh(db_donut)
    return db_donut


async def delete_donut(db: AsyncSession, donut_id: int):
    db_donut = await get_donut(db, donut_id)
    if db_donut is None:
        raise HTTPException(status_code=404, detail="Donut not found")

    await db.delete(db_donut)
    await db.commit()
    return {"message": "Donut deleted successfully"}
