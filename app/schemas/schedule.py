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


class ScheduleCreateResponse(BaseModel):
    id: UUID

    model_config = ConfigDict(
        from_attributes=True,
    )
