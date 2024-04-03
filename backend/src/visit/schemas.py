from enum import Enum
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel
from src.vital.schemas import VitalOut


class VisitStatus(str, Enum):
    CHECKED_IN = "checked_in"
    CHECKED_OUT = "checked_out"
    DISCHARGED = "discharged"
    ADMITTED = "admitted"

class VisitBase(BaseModel):
    id: int
    patient_id: UUID 
    reason_for_visit: str
    visit_status: VisitStatus
    created_at: datetime
    updated_at: datetime

class VisitOut(VisitBase):
    vitals: list[VitalOut] | None = []
    notes: list | None = []
    labtests: list | None = []
    discharged_at: datetime | None

class VisitsOut(BaseModel):
    data: list[VisitOut]

class VisitUpdate(BaseModel):
    reason_for_visit: str
    visit_status: VisitStatus = VisitStatus.CHECKED_IN

class VisitCreate(VisitUpdate):
    patient_id: UUID = UUID("3d765a74-45d8-48c0-b9aa-247b304bb487")

class VisitDelete(BaseModel):
    data: list[int]
