from uuid import UUID
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.core.models import Base
from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from src.utils import TimestampMixin

class User(TimestampMixin, SQLAlchemyBaseUserTableUUID, Base):
    
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), default=1)
    role: Mapped["Role"] = relationship() #,  lazy="selectin")
    
    def __repr__(self):
        return f"<User {self.email}>"
class Role(Base):
    __tablename__ = "roles"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)  

    def __repr__(self):
        return f"<Role {self.name}>"

