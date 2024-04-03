import datetime
from uuid import UUID
from typing import Annotated

from sqlalchemy import ForeignKey, event, update, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import DateTime

from src.core.database import Base
from src.utils import TimestampMixin
from .schemas import VisitStatus
from src.vital.models import Vital
from src.note.models import Note
from src.labtest.models import LabTest

user_id = Annotated[UUID, mapped_column(ForeignKey("user.id"))]
visit_id = Annotated[int, mapped_column(ForeignKey("visit.id", ondelete="cascade"))]


class Visit(TimestampMixin, Base):
    __tablename__ = "visit"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    patient_id: Mapped[user_id]
    reason_for_visit: Mapped[str]
    visit_status: Mapped[VisitStatus]
    discharged_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=True)

    vitals: Mapped[list["Vital"]] = relationship(back_populates="visit", cascade="all, delete", passive_deletes=True)
    notes: Mapped[list["Note"]] = relationship(back_populates="visit", cascade="all, delete", passive_deletes=True)
    labtests: Mapped[list["LabTest"]] = relationship(back_populates="visit", cascade="all, delete", passive_deletes=True)



def update_visit_on_related_create(mapper, connection, instance):
    if isinstance(instance, (Vital, Note, LabTest)):
        connection.execute(update(Visit).where(Visit.id == instance.visit_id).values(updated_at = func.current_timestamp()))

event.listen(Vital, 'after_insert', update_visit_on_related_create)
event.listen(Vital, 'after_update', update_visit_on_related_create)
event.listen(Note, 'after_insert', update_visit_on_related_create)
event.listen(Note, 'after_update', update_visit_on_related_create)
event.listen(LabTest, 'after_insert', update_visit_on_related_create)
event.listen(LabTest, 'after_update', update_visit_on_related_create)

# TODO
# class Appointment(Base):
#     __tablename__ = "appointment"
#     id: Mapped[int] = mapped_column(primary_key=True, index=True)
#     patient_id: Mapped[int]
#     # Add fields for date, time, reason, etc.

