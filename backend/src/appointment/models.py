import datetime
from typing import TYPE_CHECKING, Optional
from sqlalchemy.types import DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.utils.types import TimestampMixin, user_id
from src.core.database import Base
from .schemas import AppointmentStatus

if TYPE_CHECKING:
    from src.visit.models import Visit
    from src.account.models import User

class Appointment(TimestampMixin, Base):
    __tablename__ = "appointment"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    requested_by: Mapped[user_id] = mapped_column(nullable=True)
    on_behalf_of: Mapped[user_id] 
    scheduled_date: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True))
    status: Mapped[AppointmentStatus] = mapped_column(default=AppointmentStatus.PENDING)
    reason: Mapped[str]
    assigned_doctor: Mapped[user_id] = mapped_column(nullable=True)

    visit:Mapped["Visit"] = relationship(back_populates="appointment", single_parent=True)
    patient:Mapped["User"] = relationship(foreign_keys="appointment.c.on_behalf_of")
    doctor:Mapped["User"] = relationship(foreign_keys="appointment.c.assigned_doctor")