from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ScheduleCreate(BaseModel):
    user_id: str = Field(
        min_length=1,
        max_length=255,
    )

    medicine_name: str = Field(
        min_length=1,
        max_length=255,
    )

    frequency: int = Field(
        ge=1,
        le=24,
    )

    treatment_days: int | None = Field(
        default=None,
        ge=1,
    )


class ScheduleResponse(BaseModel):
    id: UUID
    user_id: str
    medicine_name: str
    frequency: int
    treatment_days: int | None
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )


class ScheduleListResponse(BaseModel):
    schedule_ids: list[UUID]


class ScheduleDetailsResponse(BaseModel):
    id: UUID
    user_id: str
    medicine_name: str
    frequency: int
    treatment_days: int | None
    created_at: datetime
    daily_schedule: list[str]

    model_config = ConfigDict(
        from_attributes=True,
    )


class NextTakingResponse(BaseModel):
    schedule_id: UUID
    medicine_name: str
    taking_time: str


class ScheduleCreatedResponse(BaseModel):
    id: UUID
