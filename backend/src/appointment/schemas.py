from enum import Enum
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel


class AppointmentStatus(str, Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    CANCELLED = "cancelled"

class AppointmentCreate(BaseModel):
    scheduled_date: datetime
    reason: str
    on_behalf_of: UUID | None = "7e738f10-ce39-4c01-bf4a-a5bcdcee2c9a"

class AppointmentUpdate(AppointmentCreate):
    status: AppointmentStatus

class AppointmentOut(AppointmentCreate):
    id: int
    requested_by: UUID | None = None
    assigned_doctor: UUID | None = None
    status: AppointmentStatus