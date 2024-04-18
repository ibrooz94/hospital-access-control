from fastapi import APIRouter, Depends
from src.core.dependecies import SessionDep
from src.account.services import RoleChecker, current_active_user, current_active_superuser
from src.account.schemas import Role

from .schemas import NoteCreate, NoteRead
from .services import note_crud, is_note_author


router = APIRouter(prefix="/{visit_id}")

allow_create_edit_resource = RoleChecker([Role.DOCTOR, Role.NURSE])
allow_read_resource = RoleChecker([Role.DOCTOR, Role.NURSE, Role.LAB_TECH])

@router.post(
    "/note",
    status_code=201,
    dependencies=[Depends(allow_create_edit_resource)],
    response_model = NoteRead
)
async def create_visit_note(session: SessionDep, visit_id: int, request: NoteCreate, user = Depends(current_active_user)):
    note = await note_crud.create(session, visit_id, request, user)
    return note

@router.get(
    "/note/{item_id}",
    status_code=201,
    dependencies=[Depends(allow_read_resource)],
    response_model = NoteRead
)
async def get_note(session: SessionDep, item_id:int):
    notes = await note_crud.get_by_id(session, item_id)
    return notes

@router.patch(
    "/note/{item_id}",
    status_code=201,
    dependencies=[Depends(allow_create_edit_resource), Depends(is_note_author)],
    response_model = NoteRead
)
async def update_note(session: SessionDep, request: NoteCreate, item_id:int):
    note = await note_crud.update(session, item_id, request.model_dump(exclude_unset=True))
    return note

@router.delete(
    "/note/{item_id}",
    status_code=204,
    dependencies=[Depends(current_active_superuser)],
)
async def delete_note(session: SessionDep, item_id:int):
    note = await note_crud.delete(session, item_id)
    return note

