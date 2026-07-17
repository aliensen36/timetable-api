from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Schedule(Base):
    __tablename__ = "schedules"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
    )

    user_id: Mapped[str] = mapped_column(
        String(255),
        index=True,
    )

    medicine_name: Mapped[str] = mapped_column(
        String(255),
    )

    frequency: Mapped[int] = mapped_column(
        Integer,
        comment="Количество приемов в день",
    )

    treatment_days: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
        comment="None - постоянный прием",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )
