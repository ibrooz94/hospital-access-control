from enum import Enum
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, EmailStr
from src.vital.schemas import VitalOut
from src.note.schemas import NoteRead
from src.appointment.schemas import AppointmentOut
from src.labtest.schemas import LabTestRead
from src.account.schemas import UserRead


class VisitStatus(str, Enum):
    CHECKED_IN = "checked_in"
    CHECKED_OUT = "checked_out"
    DISCHARGED = "discharged"
    ADMITTED = "admitted"

class VisitFilter(BaseModel):
    visit_status: VisitStatus | None = None

class VisitBase(BaseModel):
    id: int
    reason_for_visit: str
    visit_status: VisitStatus
    appointment_id: int | None = None
    created_at: datetime
    updated_at: datetime

class VisitOut(VisitBase):
    vitals: list[VitalOut] | None = []
    notes: list[NoteRead] | None = []
    labtests: list[LabTestRead] | None = []
    appointment: AppointmentOut | None = None
    patient: UserRead | None = None
    discharged_at: datetime | None

class VisitOutList(BaseModel):
    id: int
    reason_for_visit: str
    visit_status: VisitStatus
    appointment: AppointmentOut | None = None
    patient: UserRead | None = None
    discharged_at: datetime | None


class VisitUpdate(BaseModel):
    reason_for_visit: str
    visit_status: VisitStatus = VisitStatus.CHECKED_IN

class VisitCreate(VisitUpdate):
    patient_id: EmailStr = "patient@patient.com"
    appointment_id: int | None = None
