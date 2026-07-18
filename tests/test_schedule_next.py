from app.core.config import Settings


def test_next_takings_period_default() -> None:
    settings = Settings(
        database_url="postgresql+asyncpg://test",
    )

    assert settings.next_takings_period_minutes == 60
