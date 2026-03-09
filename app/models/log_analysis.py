from sqlalchemy import TIMESTAMP, ForeignKey, Text, func
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base


class LogAnalysis(Base):
    __tablename__ = "log_analysis"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    log_id: Mapped[int] = mapped_column(ForeignKey("log.id"), nullable=False)
    issue: Mapped[str] = mapped_column(Text, nullable=False)
    root_cause: Mapped[str] = mapped_column(Text, nullable=False)
    solution: Mapped[str] = mapped_column(Text, nullable=False)
    analyzed_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, server_default=func.now())
