from datetime import UTC, datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db.database import Base


class LevelModel(Base):
    __tablename__ = "level"

    levelID: Mapped[int] = mapped_column("levelID", autoincrement=True, nullable=False, unique=True, primary_key=True, init=False)
    level_name: Mapped[str] = mapped_column(String(150))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default_factory=lambda: datetime.now(UTC))

 