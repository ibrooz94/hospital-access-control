from fastapi import APIRouter, Depends
from uuid import UUID
from src.core.dependecies import SessionDep
from src.account.services import RoleChecker, current_active_user, current_active_superuser
from src.account.schemas import Role

from .schemas import VitalOut, VitalCreate
from .services import vital_crud, visit_checker


router = APIRouter(prefix="/{visit_id}")
allow_create_edit_resource = RoleChecker([Role.DOCTOR, Role.NURSE])
allow_read_resource = RoleChecker([Role.DOCTOR, Role.NURSE, Role.LAB_TECH])

@router.post(
    "/vital",
    status_code=201,
    dependencies=[Depends(allow_read_resource)],
    response_model = VitalOut
)
async def create_visit_vital(session: SessionDep, visit_id: int, request: VitalCreate, user = Depends(current_active_user)):
    vital = await vital_crud.create(session, visit_id, request, user)
    return vital

@router.get(
    "/vitals/",
    status_code=201,
    dependencies=[Depends(allow_create_edit_resource)],
    response_model = list[VitalOut]
)
async def get_all_vital(session: SessionDep, visit_id:int, skip: int = 0, limit: int = 100):
    vitals = await vital_crud.get_all_by_visit(session, visit_id, skip, limit)
    return vitals

@router.get(
    "/vital/{item_id}",
    status_code=201,
    dependencies=[Depends(allow_create_edit_resource), Depends(visit_checker)],
    response_model = VitalOut
)
async def get_vital(session: SessionDep, item_id:int):
    vitals = await vital_crud.get_by_id(session, item_id)
    return vitals

@router.patch(
    "/vital/{item_id}",
    status_code=201,
    dependencies=[Depends(allow_create_edit_resource), Depends(visit_checker)],
    response_model = VitalOut
)
async def update_vital(session: SessionDep, request: VitalCreate, item_id:int):
    vital = await vital_crud.update(session, item_id, request.model_dump(exclude_unset=True))
    return vital

@router.delete(
    "/vital/{item_id}",
    status_code=204,
    dependencies=[Depends(current_active_superuser), Depends(visit_checker)],
)
async def delete_vital(session: SessionDep, item_id:int):
    vital = await vital_crud.delete(session, item_id)
    return vital

