from typing import Annotated
from fastapi import Depends
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession as Session

from src.account.models import User
from .database import sessionmanager
from .config import settings

session_manager = sessionmanager.init(host = str(settings.SQLALCHEMY_DATABASE_URI) )

async def get_db():
    async with sessionmanager.session() as session:
        yield session

SessionDep = Annotated[Session, Depends(get_db)]

async def get_user_db(session: SessionDep):
    yield SQLAlchemyUserDatabase(session, User)
