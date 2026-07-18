from datetime import datetime, timedelta
from typing import TypedDict
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.schedule import Schedule
from app.schemas.schedule import ScheduleCreate
from app.services.schedule_calculator import generate_daily_schedule


class NextTakingDict(TypedDict):
    schedule_id: UUID
    medicine_name: str
    taking_time: str


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


async def get_next_takings(
    session: AsyncSession,
    user_id: str,
    period_minutes: int,
) -> list[NextTakingDict]:
    schedules = await session.scalars(
        select(Schedule).where(
            Schedule.user_id == user_id,
        )
    )

    now = datetime.now()

    end_time = now + timedelta(
        minutes=period_minutes,
    )

    result: list[NextTakingDict] = []

    for schedule in schedules:
        times = generate_daily_schedule(
            schedule.frequency,
        )

        for time_value in times:
            hour, minute = map(
                int,
                time_value.split(":"),
            )

            taking = now.replace(
                hour=hour,
                minute=minute,
                second=0,
                microsecond=0,
            )

            if now <= taking <= end_time:
                result.append(
                    {
                        "schedule_id": schedule.id,
                        "medicine_name": schedule.medicine_name,
                        "taking_time": time_value,
                    }
                )

    return result
