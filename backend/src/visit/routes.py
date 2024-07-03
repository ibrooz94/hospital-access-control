from uuid import UUID
from fastapi import APIRouter, status, Depends

from src.core.dependecies import SessionDep
from src.account.services import RoleChecker, current_active_user, get_user_manager, UserManager
from src.account.schemas import Role
from src.vital.routes import router as vital_router
from src.labtest.routes import router as labtest_router
from src.note.routes import router as note_router
from .schemas import VisitBase, VisitCreate, VisitOut, VisitOutList, VisitUpdate, VisitFilter
from . import services


router = APIRouter()
allow_create_resource = RoleChecker([Role.DOCTOR, Role.NURSE, Role.LAB_TECH])


@router.post(
    "/",
    status_code=201,
    dependencies=[Depends(allow_create_resource)],
    response_model=VisitBase,
)
async def create_visit(
    request: VisitCreate, session: SessionDep, user=Depends(current_active_user), user_manager: UserManager = Depends(get_user_manager)
):
    visit = await services.create_visit(session, request, user, user_manager)
    return visit


@router.get(
    "/{id}",
    status_code=201,
    dependencies=[Depends(allow_create_resource)],
    response_model=VisitOut,
)
async def get_visit(id: int, session: SessionDep):
    visit = await services.get_visit_by_id(session, id, with_option=True)
    return visit


@router.get(
    "/",
    status_code=200,
    dependencies=[Depends(allow_create_resource)],
    response_model=list[VisitOutList],
)
async def get_all_visit(
    session: SessionDep,
    skip: int = 0,
    limit: int = 100,
    filter_by: VisitFilter = Depends(),
    sort: str | None = None,
):
    visits = await services.get_all_visits(
        session,
        skip,
        limit,
        sort,
        filter_by.model_dump(exclude_unset=True, exclude_none=True),
    )
    return visits


@router.get(
    "/patient/{patient_id}",
    status_code=200,
    dependencies=[Depends(allow_create_resource)],
    response_model=list[VisitOutList],
)
async def get_all_patient_visit(
    session: SessionDep, patient_id: UUID, skip: int = 0, limit: int = 100
):
    visits = await services.get_all_visits_patient(session, patient_id, skip, limit)
    return visits


@router.patch(
    "/{id}",
    status_code=200,
    dependencies=[Depends(allow_create_resource)],
    response_model=VisitBase,
)
async def update_visit(session: SessionDep, id: int, request: VisitUpdate):
    visit = await services.update_visit(session, id, request)
    return visit


@router.delete("/{id} ", status_code=204, dependencies=[Depends(allow_create_resource)])
async def delete_visit(session: SessionDep, id: int):
    await services.delete_visit(session, id)
    return status.HTTP_204_NO_CONTENT


router.include_router(vital_router, tags=["vital"])
router.include_router(labtest_router, tags=["labtest"])
router.include_router(note_router, tags=["note"])
