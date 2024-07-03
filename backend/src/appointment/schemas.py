from enum import Enum
from typing import Any
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel
from src.account.schemas import UserRead
from pydantic import BaseModel, EmailStr, ConfigDict


class AppointmentStatus(str, Enum):
    PENDING = "pending"
    BOOKED = "booked"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class AppointmentCreate(BaseModel):
    scheduled_date: datetime
    reason: str
    on_behalf_of: EmailStr | None = "patient@patient.com"

class AppointmentBase(BaseModel):
    id: int
    requested_by: UUID | None = None
    assigned_doctor: UUID | None = None
    status: AppointmentStatus
    created_at: datetime
    updated_at: datetime

class AppointmentUpdate(BaseModel):
    status: AppointmentStatus
    assigned_doctor: UUID 

class AppointmentOut(BaseModel):
    id: int
    status: AppointmentStatus
    scheduled_date: datetime
    reason: str
    on_behalf_of: Any
    patient: UserRead | None = None
    # assigned_doctor: UUID

class AppointmentFilter(BaseModel):
    status: AppointmentStatus | None = None

