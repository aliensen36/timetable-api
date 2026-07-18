DAY_START = 8 * 60
DAY_END = 22 * 60
DAY_DURATION = DAY_END - DAY_START


def round_to_15_minutes(minutes: int) -> int:
    return ((minutes + 14) // 15) * 15


def format_minutes(minutes: int) -> str:
    hours = minutes // 60
    mins = minutes % 60

    return f"{hours:02d}:{mins:02d}"


def generate_daily_schedule(frequency: int) -> list[str]:
    if frequency == 1:
        return [
            format_minutes(DAY_START),
        ]

    step = DAY_DURATION / (frequency - 1)

    result = []

    for index in range(frequency):
        calculated = DAY_START + round(step * index)
        rounded = round_to_15_minutes(calculated)

        if rounded > DAY_END:
            rounded = DAY_END

        result.append(
            format_minutes(rounded),
        )

    return result
