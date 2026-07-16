from pathlib import Path

from alembic.config import Config

ROOT_DIR = Path(__file__).resolve().parent.parent


def test_alembic_config_exists() -> None:
    alembic_ini = ROOT_DIR / "alembic.ini"

    assert alembic_ini.exists(), (
        "alembic.ini не найден. Сначала нужно инициализировать Alembic."
    )


def test_alembic_config_loads() -> None:
    alembic_ini = ROOT_DIR / "alembic.ini"

    config = Config(str(alembic_ini))

    assert config.config_file_name == str(alembic_ini)
