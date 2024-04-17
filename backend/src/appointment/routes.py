from fastapi import APIRouter, Depends
from uuid import UUID
from src.core.dependecies import SessionDep
from src.account.services import RoleChecker, current_active_user, current_active_superuser
from src.account.schemas import Role

from .schemas import AppointmentCreate, AppointmentOut, AppointmentUpdate
from .services import appointment_crud


router = APIRouter()

allow_create_edit_resource = RoleChecker([Role.DOCTOR, Role.NURSE])
allow_read_resource = RoleChecker([Role.DOCTOR, Role.NURSE, Role.LAB_TECH])

@router.post(
    "/",
    status_code=201,
    response_model = AppointmentOut
)
async def create_appointment(session: SessionDep, request: AppointmentCreate, user = Depends(current_active_user)):
    appointment = await appointment_crud.create(session, request, user)
    return appointment

@router.get(
    "/{item_id}",
    status_code=201,
    dependencies=[Depends(current_active_user)],
    response_model = AppointmentOut
)
async def get_appointment(session: SessionDep, item_id:int):
    vitals = await appointment_crud.get_by_id(session, item_id)
    return vitals

@router.patch(
    "/{item_id}",
    status_code=201,
    dependencies=[Depends(allow_create_edit_resource)],
    response_model = AppointmentOut
)
async def update_appointment(session: SessionDep, request: AppointmentUpdate, item_id:int):
    appointment = await appointment_crud.update(session, item_id, request.model_dump(exclude_unset=True))
    return appointment

@router.delete(
    "/{item_id}",
    status_code=204,
    dependencies=[Depends(current_active_superuser)],
)
async def delete_appointment(session: SessionDep, item_id:int):
    appointment = await appointment_crud.delete(session, item_id)
    return appointment

