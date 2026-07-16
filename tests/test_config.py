from app.core.config import Settings


def test_settings_load_database_url() -> None:
    settings = Settings(
        database_url="postgresql+asyncpg://user:password@localhost:5432/test"
    )

    assert settings.database_url == (
        "postgresql+asyncpg://user:password@localhost:5432/test"
    )


def test_settings_default_app_name() -> None:
    settings = Settings(
        database_url="postgresql+asyncpg://user:password@localhost:5432/test"
    )

    assert settings.app_name == "Timetable API"
