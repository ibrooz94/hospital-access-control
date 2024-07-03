from uuid import UUID
from typing import Annotated
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from fastapi import APIRouter, Depends, Body

from src.core.dependecies import SessionDep
from .services import fastapi_users, RoleChecker, current_active_user, current_active_superuser, get_user_manager, UserManager
from .schemas import UserRead, UserUpdate, Role, RoleOut
from .models import User

allow_create_resource = RoleChecker([Role.NURSE, Role.DOCTOR])

router = APIRouter()

router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate)
)


@router.patch(
    "/{id}/role",
    status_code=201,
    dependencies=[Depends(current_active_superuser)],
    response_model = UserRead
)
async def update_user_role(session: SessionDep, id:UUID, role_id: Role):
    statement = select(User).where(User.id == id)
    result = (await session.execute(statement)).scalar()

    result.role_id = role_id

    await session.commit()
    await session.refresh(result)

    return result

@router.post(
    "/some-resource/",
    status_code=200,
    dependencies=[Depends(allow_create_resource)],
    response_model= UserRead
)
async def add_resource(session: SessionDep, user: User = Depends(current_active_user)):
    statement = select(User).where(User.id == user.id)
    result = (await session.execute(statement)).scalar()
    final = UserRead.model_validate(result)
    return final

@router.get(
    "/emsil",
    status_code=200,
    response_model= UserRead
)
async def get_user_by_email(session: SessionDep, user_email, user_manager = Depends(get_user_manager)):
    user = await user_manager.get_by_email(user_email)
    return user
