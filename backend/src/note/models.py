from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Text

from src.core.database import Base
from src.utils.types import TimestampMixin, visit_id, user_id

if TYPE_CHECKING:
    from src.visit.models import Visit


class Note(TimestampMixin, Base):
    __tablename__ = "note"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    visit_id: Mapped[visit_id]
    text: Mapped[str] = mapped_column(Text)
    author: Mapped[user_id] 

    visit:Mapped["Visit"] = relationship(back_populates="notes")

