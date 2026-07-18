from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.dependencies import get_db
from app.schemas.schedule import (
    ScheduleCreate,
    ScheduleListResponse,
    ScheduleResponse,
)
from app.services.schedule import (
    create_schedule,
    get_schedule_ids,
)

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


@router.get(
    "",
    response_model=ScheduleListResponse,
)
async def get_schedule_ids_endpoint(
    user_id: str = Query(
        min_length=1,
        max_length=255,
    ),
    session: AsyncSession = Depends(get_db),
) -> ScheduleListResponse:
    schedule_ids = await get_schedule_ids(
        session=session,
        user_id=user_id,
    )

    return ScheduleListResponse(
        schedule_ids=schedule_ids,
    )
