import datetime
from uuid import UUID
from typing import Annotated, TypeVar
from sqlalchemy import func, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.types import DateTime
from src.core.database import Base


ModelT = TypeVar("ModelT", bound=Base)

user_id = Annotated[UUID, mapped_column(ForeignKey("user.id"))]
visit_id = Annotated[int, mapped_column(ForeignKey("visit.id", ondelete="cascade"))]

class TimestampMixin(object):
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), 
        server_default=func.now(),
        onupdate=func.current_timestamp())
