from typing import Annotated
from fastapi import Depends
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession as Session

from src.account.models import User
from .database import sessionmanager

async def get_db():
    async with sessionmanager.session() as session:
        yield session

SessionDep = Annotated[Session, Depends(get_db)]

async def get_user_db(session: SessionDep):
    yield SQLAlchemyUserDatabase(session, User)
