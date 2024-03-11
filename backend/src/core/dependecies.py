from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession as Session
from fastapi import Depends
from .database import sessionmanager


async def get_db():
    async with sessionmanager.session() as session:
        yield session

SessionDep = Annotated[Session, Depends(get_db)]