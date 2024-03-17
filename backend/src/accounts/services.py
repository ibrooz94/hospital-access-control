from fastapi import HTTPException, status
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession as Session

from src.core.security import hash_password
from .schemas import UserCreate, UserUpdate, UserUpdateMe
from .models import User
from fastapi_users import FastAPIUsers

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

async def update_user_pythonic(session: Session, user_id: int, user_in: UserUpdate):
    user = await get_user_by_id(session, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )

    user_data = user_in.model_dump(exclude_unset=True)
    if not user_data:
        raise HTTPException(
            status_code=400,
            detail="Invalid data",
        )

    for field, value in user_data.items():
        if field == 'password':
            user.hashed_password = hash_password(value)
        setattr(user, field, value)

    await session.commit()
    await session.refresh(user)
    return user

async def update_user(session: Session, user_id: int, user_in: UserUpdate):
    
    user_data = user_in.model_dump(exclude_unset=True)
    if not user_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid data")

    if "password" in user_data:
        password = user_data.pop("password") 
        user_data['hashed_password'] = hash_password(password)

    stmt = update(User).where(User.id == user_id).values(user_data).returning(User)
    updated_user = (await session.execute(stmt)).scalar_one_or_none()

    await session.commit()
    await session.refresh(updated_user)

    return updated_user


