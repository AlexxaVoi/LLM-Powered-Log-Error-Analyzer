from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import List


class LogCreateSchema(BaseModel):
    log_text: str


class LogReadSchema(BaseModel):
    id: int
    user_id: int
    log_text: str
    uploaded_at: datetime

    model_config = ConfigDict(from_attributes=True)


class HistoryLogSchema(BaseModel):
    logs: List[LogReadSchema]
