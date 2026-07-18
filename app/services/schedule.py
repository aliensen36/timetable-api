from uuid import UUID

from sqlalchemy import select
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


async def get_schedule_ids(
    session: AsyncSession,
    user_id: str,
) -> list[UUID]:
    result = await session.scalars(
        select(Schedule.id).where(
            Schedule.user_id == user_id,
        )
    )

    return list(result)


async def get_schedule(
    session: AsyncSession,
    user_id: str,
    schedule_id: UUID,
) -> Schedule | None:
    result = await session.scalar(
        select(Schedule).where(
            Schedule.id == schedule_id,
            Schedule.user_id == user_id,
        )
    )

    return result
