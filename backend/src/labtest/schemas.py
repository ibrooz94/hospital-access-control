from enum import Enum
from datetime import datetime
from pydantic import BaseModel

class LabStatus(str, Enum):
    REQUESTED = "requested"
    PENDING = "pending"
    COMPLETED = "completed"

class LabTestCreate(BaseModel):
    lab_type: str

class LabTestUpdate(LabTestCreate):
    result: str | None = None
    note: str | None = None
    status: LabStatus = LabStatus.REQUESTED

class LabTestRead(LabTestUpdate):
    id: int
    created_at: datetime
    updated_at: datetime