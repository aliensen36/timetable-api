from app.models.schedule import Schedule


def test_schedule_tablename() -> None:
    assert Schedule.__tablename__ == "schedules"


def test_schedule_columns() -> None:
    columns = Schedule.__table__.columns

    assert "id" in columns
    assert "user_id" in columns
    assert "medicine_name" in columns
    assert "frequency" in columns
    assert "treatment_days" in columns
    assert "created_at" in columns


def test_schedule_has_user_id_index() -> None:
    indexes = Schedule.__table__.indexes

    assert any(
        "user_id" in [column.name for column in index.columns] for index in indexes
    )
