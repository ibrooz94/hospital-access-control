from typing import Optional, TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Text

from src.core.database import Base
from src.utils.types import TimestampMixin, visit_id
from .schemas import LabStatus

if TYPE_CHECKING:
    from src.visit.models import Visit

class LabTest(TimestampMixin, Base):
    __tablename__ = "labtest"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    visit_id: Mapped[Optional[visit_id]]
    lab_type: Mapped[str]
    status: Mapped[LabStatus]
    result: Mapped[str]
    note: Mapped[str] = mapped_column(Text)

    visit:Mapped["Visit"] = relationship(back_populates="labtests")