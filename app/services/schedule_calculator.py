DAY_START = 8 * 60
DAY_END = 22 * 60

MINUTES_IN_HOUR = 60
ROUND_STEP = 15


def round_to_15_minutes(minutes: int) -> int:
    return ((minutes + ROUND_STEP - 1) // ROUND_STEP) * ROUND_STEP


def format_minutes(minutes: int) -> str:
    hours = minutes // MINUTES_IN_HOUR
    mins = minutes % MINUTES_IN_HOUR

    return f"{hours:02d}:{mins:02d}"


def generate_daily_schedule(frequency: int) -> list[str]:
    """
    Расчет времени приема в дневном интервале 08:00-22:00.

    frequency:
    1 - один прием
    15 - ежечасный прием
    """

    if frequency == 1:
        return [
            format_minutes(DAY_START),
        ]

    interval = (DAY_END - DAY_START) / (frequency - 1)

    result: list[str] = []

    for index in range(frequency):
        calculated = DAY_START + round(
            interval * index,
        )

        rounded = round_to_15_minutes(
            calculated,
        )

        if rounded > DAY_END:
            rounded = DAY_END

        result.append(
            format_minutes(rounded),
        )

    return result
