from datetime import UTC, datetime
from uuid import uuid4

import pytest
from pydantic import ValidationError

from app.schemas.schedule import (
    ScheduleCreate,
    ScheduleListResponse,
    ScheduleResponse,
)


def test_schedule_create_valid() -> None:
    schema = ScheduleCreate(
        user_id="user-1",
        medicine_name="Ibuprofen",
        frequency=3,
        treatment_days=14,
    )

    assert schema.user_id == "user-1"
    assert schema.medicine_name == "Ibuprofen"
    assert schema.frequency == 3
    assert schema.treatment_days == 14


def test_schedule_create_accepts_none_treatment_days() -> None:
    schema = ScheduleCreate(
        user_id="user-1",
        medicine_name="Vitamin C",
        frequency=1,
        treatment_days=None,
    )

    assert schema.treatment_days is None


@pytest.mark.parametrize(
    "frequency",
    [
        0,
        16,
    ],
)
def test_schedule_create_invalid_frequency(
    frequency: int,
) -> None:
    with pytest.raises(ValidationError):
        ScheduleCreate(
            user_id="user-1",
            medicine_name="Ibuprofen",
            frequency=frequency,
            treatment_days=10,
        )


def test_schedule_response() -> None:
    schedule_id = uuid4()

    response = ScheduleResponse(
        id=schedule_id,
        user_id="user-1",
        medicine_name="Ibuprofen",
        frequency=3,
        treatment_days=10,
        created_at=datetime.now(UTC),
    )

    assert response.id == schedule_id
    assert response.medicine_name == "Ibuprofen"


def test_schedule_list_response() -> None:
    schedule_ids = [
        uuid4(),
        uuid4(),
    ]

    response = ScheduleListResponse(
        schedule_ids=schedule_ids,
    )

    assert response.schedule_ids == schedule_ids
