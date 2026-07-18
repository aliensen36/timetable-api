from app.services.schedule_calculator import (
    generate_daily_schedule,
)


def test_one_intake_per_day() -> None:
    result = generate_daily_schedule(1)

    assert result == [
        "08:00",
    ]


def test_two_intakes_per_day() -> None:
    result = generate_daily_schedule(2)

    assert result == [
        "08:00",
        "22:00",
    ]


def test_all_times_are_multiple_of_15() -> None:
    result = generate_daily_schedule(5)

    for value in result:
        hours, minutes = value.split(":")

        assert int(minutes) % 15 == 0
