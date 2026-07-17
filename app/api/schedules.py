from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.dependencies import get_db
from app.schemas.schedule import (
    ScheduleCreate,
    ScheduleResponse,
)
from app.services.schedule import create_schedule

router = APIRouter(
    prefix="/schedules",
    tags=["Schedules"],
)


@router.post(
    "",
    response_model=ScheduleResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_schedule_endpoint(
    data: ScheduleCreate,
    session: AsyncSession = Depends(get_db),
) -> ScheduleResponse:
    schedule = await create_schedule(
        session,
        data,
    )

    return ScheduleResponse.model_validate(schedule)
