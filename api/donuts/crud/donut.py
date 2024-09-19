from typing import Optional, Sequence

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
    # await session.flush()  # instantly fixes all new data info in database
    return new_donut


async def get_donut_by_id(
        session: AsyncSession,
        donut_id: int,
) -> Optional[Donut]:
    return await session.get(Donut, donut_id)


async def get_all_donuts(session: AsyncSession) -> Sequence[Donut]:
    stmt = select(Donut)
    result = await session.execute(stmt)
    return result.scalars().all()


async def update_donut(
        session: AsyncSession,
        donut_id: int,
        donut_update: DonutUpdate,
) -> Optional[Donut]:
    donut: Optional[Donut] = await session.get(Donut, donut_id)

    if not donut:
        return None

    for key, value in donut_update.model_dump(exclude_unset=True).items():
        setattr(donut, key, value)

    await session.commit()
    await session.refresh(donut)
    return donut


async def delete_donut(
        session: AsyncSession,
        donut_id: int,
) -> bool:
    donut: Optional[Donut] = await session.get(Donut, donut_id)

    if not donut:
        return False

    await session.delete(donut)
    await session.commit()
    return True
