from pydantic import BaseModel
from typing import Dict, Any
from uuid import UUID
from datetime import datetime

class ExperimentBase(BaseModel):
    name: str
    description: str
    status: str
    groups: Dict[str, Any]
    results: Dict[str, Any]

class ExperimentResponse(ExperimentBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    class Config:
        orm_mode = True
