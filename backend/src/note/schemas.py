from datetime import datetime
from pydantic import BaseModel
from uuid import UUID

class NoteCreate(BaseModel):
    text: str

class NoteRead(NoteCreate):
    id: int
    author: UUID
    created_at: datetime
    updated_at: datetime