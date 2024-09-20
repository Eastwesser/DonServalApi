from typing import Optional, Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from api.core.models.donut import Donut
from api.donuts.schemas.schemas import (
    DonutCreate,
    DonutUpdate,
)


# Create a new donut entry in the database.
async def create_donut(
        session: AsyncSession,
        donut_create: DonutCreate,
) -> Donut:
    # Create a new Donut ORM object from the provided data.
    new_donut = Donut(**donut_create.model_dump())
    session.add(new_donut)  # Add the donut to the session.
    await session.commit()  # Commit the changes to the database.
    await session.refresh(new_donut)  # Refresh the session to get the new donut's ID.
    # await session.flush()  # instantly fixes all new data info in the database.
    return new_donut  # Return the created donut.


# Get a donut from the database by its ID.
async def get_donut_by_id(
        session: AsyncSession,
        donut_id: int,
) -> Optional[Donut]:
    return await session.get(Donut, donut_id)


# Get all donuts from the database.
async def get_all_donuts(session: AsyncSession) -> Sequence[Donut]:
    stmt = select(Donut)
    result = await session.execute(stmt)
    return result.scalars().all()


# Update an existing donut in the database.
async def update_donut(
        session: AsyncSession,
        donut_id: int,
        donut_update: DonutUpdate,
) -> Optional[Donut]:
    # Fetch the existing donut from the database.
    donut: Optional[Donut] = await session.get(Donut, donut_id)

    if not donut:
        return None  # Return None if the donut is not found.

    # Update the donut's attributes based on the provided data.
    for key, value in donut_update.model_dump(exclude_unset=True).items():
        setattr(donut, key, value)

    await session.commit()  # Commit the changes to the database.
    await session.refresh(donut)  # Refresh the session to reflect the updates.
    return donut  # Return the updated donut.


# Delete a donut from the database by ID.
async def delete_donut(
        session: AsyncSession,
        donut_id: int,
) -> bool:
    # Fetch the existing donut from the database.
    donut: Optional[Donut] = await session.get(Donut, donut_id)

    if not donut:
        return False  # Return False if the donut is not found.

    await session.delete(donut)  # Delete the donut from the session.
    await session.commit()  # Commit the changes to the database.
    return True  # Return True to confirm deletion.
