from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.dependencies import get_db
from app.schemas.schedule import (
    ScheduleCreate,
    ScheduleDetailsResponse,
    ScheduleListResponse,
    ScheduleResponse,
)
from app.services.schedule import (
    create_schedule,
    get_schedule,
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


@router.get(
    "/detail",
    response_model=ScheduleDetailsResponse,
)
async def get_schedule_endpoint(
    user_id: str = Query(
        min_length=1,
        max_length=255,
    ),
    schedule_id: UUID = Query(),
    session: AsyncSession = Depends(get_db),
) -> ScheduleDetailsResponse:
    schedule = await get_schedule(
        session=session,
        user_id=user_id,
        schedule_id=schedule_id,
    )

    if schedule is None:
        from fastapi import HTTPException

        raise HTTPException(
            status_code=404,
            detail="Schedule not found",
        )

    from app.services.schedule_calculator import (
        generate_daily_schedule,
    )

    return ScheduleDetailsResponse(
        id=schedule.id,
        user_id=schedule.user_id,
        medicine_name=schedule.medicine_name,
        frequency=schedule.frequency,
        treatment_days=schedule.treatment_days,
        created_at=schedule.created_at,
        daily_schedule=generate_daily_schedule(
            schedule.frequency,
        ),
    )
