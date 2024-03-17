from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select, func

from src.core.dependecies import SessionDep
from src.authentication.services import get_current_active_superuser
from . import services
from .schemas import UserCreate, UsersOut, UserOut, UserUpdate, UserBase
from .models import User

router = APIRouter()


@router.post("/register", response_model=UserOut)
async def create_user(request: UserCreate, session:SessionDep):
    user = await services.get_user_by_email(session=session, email=request.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )

    response = await services.create_user(session, request)
    return response

@router.get("/users", dependencies=[Depends(get_current_active_superuser)], response_model=UsersOut)
async def get_all_users(session: SessionDep, skip: int = 0, limit: int = 50 ):

    total_count_query = select(func.count(User.id))
    total_count = (await session.scalar(total_count_query))

    user_query = select(User).limit(limit).offset(skip)
    users = (await session.execute(user_query)).scalars().all()

    users_out = [UserOut(**user.__dict__) for user in users]

    return UsersOut(data=users_out, count=total_count)

@router.patch("/users/{user_id}/update", response_model=UserOut)
async def update_user(session:SessionDep, user_id:int, user_in:UserUpdate):
    updated_user = await services.update_user(session, user_id, user_in)
    if not updated_user:
        raise HTTPException(
            status_code=400,
            detail="The user does not exist.",
        )
    return updated_user