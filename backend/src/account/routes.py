from uuid import UUID
from typing import Annotated
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from fastapi import APIRouter, Depends, Body

from src.core.dependecies import SessionDep
from .services import fastapi_users, RoleChecker, current_active_user, current_active_superuser
from .schemas import UserRead, UserUpdate, Role, UserUpdatePublic
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
    statement = select(User).where(User.id == id).options(selectinload(User.role))
    result = (await session.execute(statement)).scalar()

    result.role_id = role_id

    await session.commit()
    await session.refresh(result)

    return result

@router.post(
    "/some-resource/",
    status_code=201,
    dependencies=[Depends(allow_create_resource)],
)
async def add_resource(session: SessionDep, user: User = Depends(current_active_user)):
    statement = select(User).where(User.id == user.id).options(selectinload(User.role))
    result = (await session.execute(statement)).scalar()

    return {"hello": result.role }
