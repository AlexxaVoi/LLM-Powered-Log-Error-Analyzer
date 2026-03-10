from pydantic import BaseModel, ConfigDict
from datetime import datetime


class AnalysisReadSchema(BaseModel):
    id: int
    log_id: int
    issue: str
    root_cause: str
    solution: str
    analyzed_at: datetime

    model_config = ConfigDict(from_attributes=True)
