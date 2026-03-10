from sqlalchemy import TIMESTAMP, ForeignKey, Text, func
from sqlalchemy.orm import Mapped, mapped_column
from .base import BaseModel


class LogModel(BaseModel):
    __tablename__ = "log"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    log_text: Mapped[str] = mapped_column(Text, nullable=False)
    uploaded_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, server_default=func.now())
