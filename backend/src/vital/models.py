from typing import TYPE_CHECKING
from src.utils.types import TimestampMixin, user_id, visit_id
from src.core.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from src.visit.models import Visit


class Vital(TimestampMixin, Base):
    __tablename__ = "vital"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    visit_id: Mapped[visit_id]
    taken_by: Mapped[user_id]
    temperature: Mapped[str] = mapped_column(nullable=True)
    blood_pressure: Mapped[str] = mapped_column(nullable=True)
    other: Mapped[str] = mapped_column(nullable=True)

    visit:Mapped["Visit"] = relationship(back_populates="vitals")