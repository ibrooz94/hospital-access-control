import datetime
from typing import TYPE_CHECKING, Annotated

from sqlalchemy import ForeignKey, event, update, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import DateTime

from src.core.database import Base
from src.utils.types import user_id
from src.utils.types import TimestampMixin
from src.vital.models import Vital
from src.note.models import Note
from src.labtest.models import LabTest
from src.appointment.models import Appointment
from .schemas import VisitStatus
if TYPE_CHECKING:
    from src.account.models import User


class Visit(TimestampMixin, Base):
    __tablename__ = "visit"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    patient_id: Mapped[user_id]
    reason_for_visit: Mapped[str]
    visit_status: Mapped[VisitStatus]
    discharged_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    appointment_id: Mapped[int] = mapped_column(ForeignKey("appointment.id", ondelete="cascade"), nullable=True)

    vitals: Mapped[list["Vital"]] = relationship(back_populates="visit", cascade="all, delete", passive_deletes=True)
    notes: Mapped[list["Note"]] = relationship(back_populates="visit", cascade="all, delete", passive_deletes=True)
    labtests: Mapped[list["LabTest"]] = relationship(back_populates="visit", cascade="all, delete", passive_deletes=True)
    appointment: Mapped["Appointment"] = relationship(back_populates="visit", cascade="all, delete", passive_deletes=True)
    patient:Mapped["User"] = relationship(foreign_keys="visit.c.patient_id")


def update_visit_on_related_create(mapper, connection, instance):
    if isinstance(instance, (Vital, Note, LabTest)):
        if instance.visit_id:
            connection.execute(update(Visit).where(Visit.id == instance.visit_id).values(updated_at = func.current_timestamp()))

event.listen(Vital, 'after_insert', update_visit_on_related_create)
event.listen(Vital, 'after_update', update_visit_on_related_create)
event.listen(Note, 'after_insert', update_visit_on_related_create)
event.listen(Note, 'after_update', update_visit_on_related_create)
event.listen(LabTest, 'after_insert', update_visit_on_related_create)
event.listen(LabTest, 'after_update', update_visit_on_related_create)
