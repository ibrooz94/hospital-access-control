from uuid import UUID
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.core.models import Base
from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from src.utils import created_at, updated_at

class Role(Base):
    __tablename__ = "roles"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)  

    user: Mapped["User"] = relationship(back_populates="role") 

    def __repr__(self):
        return f"<Role {self.name}>"

class User(SQLAlchemyBaseUserTableUUID, Base):
    
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), default=1)
    role: Mapped["Role"] = relationship(back_populates="user") #,  lazy="selectin")
    created_at: Mapped[created_at] 
    updated_at: Mapped[updated_at] 
    def __repr__(self):
        return f"<User {self.email}>"
