from sqlalchemy.ext.asyncio import AsyncSession as Session
from sqlalchemy import select, update

from src.core.security import hash_password, verify_password
from .schemas import UserCreate, UserUpdate
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
    session_user = result.scalar()
    return session_user

async def get_user_by_id(session: Session, user_id:int) -> User | None:
    statement = select(User).where(User.id == user_id)
    user = await session.scalar(statement)
    return user


async def update_user(session: Session, user_id: int, user_in: UserUpdate):

    # user = await get_user_by_id(session, user_id)
    # if not user:
    #     return None
    # for field, value in user_data.items():
    #     setattr(user, field, value)
    # await session.commit()
    # await session.refresh(user)

    user_data = user_in.model_dump(exclude_unset=True)

    if "password" in user_data:
        password = user_data.pop("password") 
        user_data['hashed_password'] = hash_password(password)


    stmt = update(User).where(User.id == user_id).values(user_data).returning(User)
    updated_user = (await session.execute(stmt)).scalar()
    
    return updated_user

# TODO: move to login module
async def authenticate(session: Session, email: str, password: str) -> User | None:
    db_user = await get_user_by_email(session=session, email=email)
    if not db_user:
        return None
    if not verify_password(password, db_user.hashed_password):
        return None
    return db_user

