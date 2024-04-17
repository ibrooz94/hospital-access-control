from enum import Enum
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel
from src.vital.schemas import VitalOut
from src.appointment.schemas import AppointmentOut
from src.appointment.models import Appointment


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
    appointment_id: int | None = None
    created_at: datetime
    updated_at: datetime

class VisitOut(VisitBase):
    vitals: list[VitalOut] | None = []
    notes: list | None = []
    labtests: list | None = []
    appointment: AppointmentOut | None = None
    discharged_at: datetime | None

class VisitsOut(BaseModel):
    data: list[VisitOut]

class VisitUpdate(BaseModel):
    reason_for_visit: str
    visit_status: VisitStatus = VisitStatus.CHECKED_IN

class VisitCreate(VisitUpdate):
    patient_id: UUID = UUID("7e738f10-ce39-4c01-bf4a-a5bcdcee2c9a")
    appointment_id: int | None = None
    

class VisitDelete(BaseModel):
    data: list[int]
