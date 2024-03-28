from fastapi import APIRouter, Depends
from .services import fastapi_users, RoleChecker, current_active_user
from .schemas import UserRead, UserUpdate, Role, UserUpdatePublic
from src.core.dependecies import SessionDep
from .models import User
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy import select



router = APIRouter()

router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdatePublic)
)

allow_create_resource = RoleChecker([Role.PATIENT])

@router.post(
    "/some-resource/",
    status_code=201,
    dependencies=[Depends(allow_create_resource)],
)
async def add_resource(session: SessionDep):
    statement = select(User).where(User.email == "user@example.com").options(joinedload(User.role))
    result = (await session.execute(statement)).scalar()

    return {"hello": result.role }
