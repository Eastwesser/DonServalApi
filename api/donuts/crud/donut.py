from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from api.core.models.donut import Donut
from api.donuts.schemas.schemas import DonutCreate, DonutUpdate


async def create_donut(db: AsyncSession, donut: DonutCreate):
    new_donut = Donut(**donut.dict())
    db.add(new_donut)
    await db.commit()
    await db.refresh(new_donut)
    return new_donut


async def get_donut(db: AsyncSession, donut_id: int):
    result = await db.execute(select(Donut).filter(Donut.id == donut_id))
    return result.scalars().first()


async def update_donut(db: AsyncSession, donut_id: int, donut_data: DonutUpdate):
    db_donut = await get_donut(db, donut_id)
    if not db_donut:
        return None
    for key, value in donut_data.dict(exclude_unset=True).items():
        setattr(db_donut, key, value)
    await db.commit()
    await db.refresh(db_donut)
    return db_donut


async def delete_donut(db: AsyncSession, donut_id: int):
    db_donut = await get_donut(db, donut_id)
    if db_donut:
        await db.delete(db_donut)
        await db.commit()
