from sqlalchemy.ext.asyncio import AsyncSession

from app.models.schedule import Schedule
from app.schemas.schedule import ScheduleCreate


async def create_schedule(
    session: AsyncSession,
    data: ScheduleCreate,
) -> Schedule:
    schedule = Schedule(
        **data.model_dump(),
    )

    session.add(schedule)

    await session.commit()
    await session.refresh(schedule)

    return schedule
