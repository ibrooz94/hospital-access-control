from fastapi import HTTPException, status
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession as Session

from src.utils.crud import CRUDBase
from src.account.models import User
from .models import UserPermission, MedicalRecord


async def has_edit_permission(session: Session, user_id: int, record_id: int) -> bool:

    permission_query = (
        select(UserPermission)
        .where(UserPermission.user_id == user_id, UserPermission.record_id == record_id)
        .where(UserPermission.can_edit == True)
    )
    permission = (await session.execute(permission_query)).scalar()

    return permission is not None


async def has_view_permission(session: Session, user_id: int, record_id: int) -> bool:

    permission_query = (
        select(UserPermission)
        .where(UserPermission.user_id == user_id, UserPermission.record_id == record_id)
        .where(UserPermission.can_view == True)
    )
    permission = (await session.execute(permission_query)).scalar()

    return permission is not None


class MedicalRecordCRUD(CRUDBase):
    def __init__(self):
        super().__init__(MedicalRecord)

    async def get(self, session: Session, record_id: int, user: User):

        record = await self.get_by_id(session, record_id)
        if await has_view_permission(session, user.id, record.id):
            return record
        else:
            raise HTTPException(403, "Insufficient permissions to view record")

    async def get_available(self, session: Session, user: User):
        records_query = (
            select(MedicalRecord)
            .join(UserPermission, UserPermission.record_id == MedicalRecord.id)
            .where(UserPermission.user_id == user.id, UserPermission.can_edit == True)
        )
        print(records_query)
        records = (await session.execute(records_query)).scalars().all()
        return records


class UserPermissionCRUD(CRUDBase):
    def __init__(self):
        super().__init__(UserPermission)


medicalrecord_crud = MedicalRecordCRUD()
userpermission_crud = UserPermissionCRUD()
