from typing import Optional

from sqlalchemy import Sequence
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from api.core.models.donut import Donut
from api.donuts.schemas.schemas import DonutCreate, DonutUpdate


async def create_donut(
        session: AsyncSession,
        donut_create: DonutCreate,
) -> Donut:
    new_donut = Donut(**donut_create.model_dump())
    session.add(new_donut)
    await session.commit()
    await session.refresh(new_donut)
    return new_donut


async def get_all_donuts(
        session: AsyncSession,
) -> Sequence[Donut]:
    stmt = select(Donut).order_by(Donut.id)
    result = await session.scalars(stmt)
    return result.all()


async def get_donut_by_id(
        session: AsyncSession,
        donut_id: int
) -> Optional[Donut]:
    stmt = select(Donut).filter(Donut.id == donut_id)
    result = await session.scalars(stmt)
    return result.first()


async def update_donut(
        session: AsyncSession,
        donut_id: int,
        donut_update: DonutUpdate
) -> Optional[Donut]:
    stmt = select(Donut).where(Donut.id == donut_id)
    result = await session.execute(stmt)

    try:
        donut = result.scalar_one()
    except NoResultFound:
        return None

    for key, value in donut_update.model_dump(exclude_unset=True).items():
        setattr(donut, key, value)

    await session.commit()
    await session.refresh(donut)
    return donut


async def delete_donut(
        session: AsyncSession,
        donut_id: int
) -> bool:
    stmt = select(Donut).where(Donut.id == donut_id)
    result = await session.execute(stmt)

    try:
        donut = result.scalar_one()
    except NoResultFound:
        return False

    await session.delete(donut)
    await session.commit()
    return True
