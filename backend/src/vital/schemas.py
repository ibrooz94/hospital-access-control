from datetime import datetime
from pydantic import BaseModel

class VitalCreate(BaseModel):
    temperature: str | None = None
    blood_pressure: str | None = None
    other: str | None = None

class VitalOut(VitalCreate):
    id: int
    created_at: datetime
    updated_at: datetime