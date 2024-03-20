from sqlalchemy.orm import Mapped, mapped_column
from src.core.models import Base
from fastapi_users.db import SQLAlchemyBaseUserTableUUID


class User(SQLAlchemyBaseUserTableUUID, Base):
    # TODO add role
    pass 
