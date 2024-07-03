from fastapi import APIRouter, Depends
from uuid import UUID
from src.core.dependecies import SessionDep
from src.account.services import RoleChecker, current_active_user, current_active_superuser
from src.account.schemas import Role

from .schemas import LabTestRead, LabTestCreate, LabTestUpdate
from .services import labtest_crud, visit_checker


router = APIRouter(prefix="/{visit_id}")
allow_create_edit_resource = RoleChecker([Role.LAB_TECH])
allow_read_resource = RoleChecker([Role.DOCTOR, Role.NURSE, Role.LAB_TECH])

@router.post(
    "/labtests",
    status_code=201,
    dependencies=[Depends(allow_read_resource)],
    response_model = LabTestRead
)
async def create_visit_labtest(session: SessionDep, visit_id: int, request: LabTestUpdate, user=Depends(current_active_user)):
    labtest = await labtest_crud.create(session, visit_id, request, user)
    return labtest

@router.get(
    "/labtests/{item_id}",
    status_code=201,
    dependencies=[Depends(allow_create_edit_resource), Depends(visit_checker)],
    response_model = LabTestRead
)
async def get_labtest(session: SessionDep, item_id:int):
    labtests = await labtest_crud.get_by_id(session, item_id)
    return labtests

@router.patch(
    "/labtests/{item_id}",
    status_code=201,
    dependencies=[Depends(allow_create_edit_resource), Depends(visit_checker)],
    response_model = LabTestRead
)
async def update_labtest(session: SessionDep, request: LabTestUpdate, item_id:int):
    labtest = await labtest_crud.update(session, item_id, request.model_dump(exclude_unset=True))
    return labtest

@router.delete(
    "/labtests/{item_id}",
    status_code=204,
    dependencies=[Depends(current_active_superuser), Depends(visit_checker)],
)
async def delete_labtest(session: SessionDep, item_id:int):
    labtest = await labtest_crud.delete(session, item_id)
    return labtest

