from sqlalchemy.ext.asyncio import AsyncSession as Session
from sqlalchemy import select

from src.core.security import hash_password, verify_password
from .schemas import UserCreate
from .models import User

async def create_user(session:Session, request:UserCreate) -> User:
    new_user = User(**request.model_dump(exclude="password"), hashed_password=hash_password(request.password) ) 
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    return new_user

async def get_user_by_email(session: Session, email: str) -> User | None:
    statement = select(User).where(User.email == email)
    result = await session.execute(statement)
    session_user = result.scalars().first()
    return session_user

# TODO: move to login module
async def authenticate(session: Session, email: str, password: str) -> User | None:
    db_user = await get_user_by_email(session=session, email=email)
    if not db_user:
        return None
    if not verify_password(password, db_user.hashed_password):
        return None
    return db_user

