from fastapi import APIRouter, Depends
from src.core.dependecies import SessionDep
from src.account.services import ( current_active_user )

from .services import medicalrecord_crud, userpermission_crud
from .schemas import PermissionCreate

router = APIRouter()

@router.get("/{record_id}", status_code=200)
async def get_record(session: SessionDep, record_id:int, user=Depends(current_active_user)):
    medical_record = await medicalrecord_crud.get(session, record_id, user)
    return medical_record

@router.get("/", status_code=200)
async def get_all_available_records(session: SessionDep, user=Depends(current_active_user)):
    medical_record = await medicalrecord_crud.get_available(session, user)
    return medical_record

@router.post("permissions/", status_code=201)
async def create_permission(session: SessionDep, request:PermissionCreate):
    medical_record = await userpermission_crud.create(session, request)
    return medical_record