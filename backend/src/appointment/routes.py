from fastapi import APIRouter, Depends
from datetime import datetime
from src.core.dependecies import SessionDep
from src.account.services import (
    RoleChecker,
    current_active_user,
    current_active_superuser,
)
from src.account.schemas import Role

from .schemas import (
    AppointmentBase,
    AppointmentCreate,
    AppointmentOut,
    AppointmentUpdate,
    AppointmentFilter,
)
from .services import appointment_crud
from src.account.services import get_user_manager, UserManager



router = APIRouter()

allow_create_edit_resource = RoleChecker([Role.DOCTOR, Role.NURSE])
allow_read_resource = RoleChecker([Role.DOCTOR, Role.NURSE, Role.LAB_TECH])
doctor_read = RoleChecker([Role.DOCTOR])


@router.post("", status_code=201, response_model=AppointmentBase)
async def create_appointment(
    session: SessionDep, request: AppointmentCreate, user=Depends(current_active_user), user_manager=Depends(get_user_manager)
):
    appointment = await appointment_crud.create(session, request, user, user_manager)

    return appointment


@router.get(
    "",
    status_code=200,
    dependencies=[Depends(current_active_user)],
    response_model=list[AppointmentOut],
)
async def get_all_appointments(
    session: SessionDep,
    user=Depends(current_active_user),
    skip: int = 0,
    limit: int = 100,
    filter_by: AppointmentFilter = Depends(),
    sort: str | None = None,
    date_from: datetime | None = None,
    date_to: datetime | None = None,
):
    appointments = await appointment_crud.get_all(
        session,
        user,
        skip,
        limit,
        sort,
        filter_by.model_dump(exclude_unset=True, exclude_none=True),
        date_from,
        date_to,
    )
    appointments_out = [
        AppointmentOut(**appointment.__dict__) for appointment in appointments
    ]

    return appointments_out


@router.get(
    "/{item_id}",
    status_code=200,
    dependencies=[Depends(current_active_user)],
    response_model=AppointmentOut,
)
async def get_appointment(session: SessionDep, item_id: int):
    appointment = await appointment_crud.get_by_id(session, item_id)
    return appointment


@router.patch(
    "/{item_id}",
    status_code=200,
    dependencies=[Depends(allow_create_edit_resource)],
    response_model=AppointmentOut,
)
async def update_appointment(
    session: SessionDep, request: AppointmentUpdate, item_id: int
):
    appointment = await appointment_crud.update(
        session, item_id, request.model_dump(exclude_unset=True)
    )
    return appointment


@router.delete(
    "/{item_id}",
    status_code=204,
    dependencies=[Depends(current_active_superuser)],
)
async def delete_appointment(session: SessionDep, item_id: int):
    appointment = await appointment_crud.delete(session, item_id)
    return appointment
