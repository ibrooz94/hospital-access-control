from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import Base
from src.utils.types import user_id, TimestampMixin

if TYPE_CHECKING:
    from src.account.models import User


class MedicalRecord(TimestampMixin, Base):
    __tablename__ = "medical_record"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    patient_id: Mapped[user_id]

    patient: Mapped["User"] = relationship(lazy="selectin")


class UserPermission(Base):
    __tablename__ = "permission"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[user_id]
    record_id: Mapped[int] = mapped_column(ForeignKey("medical_record.id"))
    can_view: Mapped[bool]
    can_edit: Mapped[bool]
