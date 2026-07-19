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


def test_max_frequency_is_hourly() -> None:
    result = generate_daily_schedule(15)

    assert result == [
        "08:00",
        "09:00",
        "10:00",
        "11:00",
        "12:00",
        "13:00",
        "14:00",
        "15:00",
        "16:00",
        "17:00",
        "18:00",
        "19:00",
        "20:00",
        "21:00",
        "22:00",
    ]


def test_all_times_are_multiple_of_15() -> None:
    result = generate_daily_schedule(5)

    for value in result:
        _, minutes = value.split(":")

        assert int(minutes) % 15 == 0
