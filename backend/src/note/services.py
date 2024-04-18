from sqlalchemy.ext.asyncio import AsyncSession as Session
from fastapi import Depends, HTTPException, status

from src.core.dependecies import SessionDep
from src.account.services import current_active_user
from src.account.models import User
from src.visit.dependencies import VisitChecker
from src.visit.services import get_visit_by_id
from src.utils.crud import CRUDBase

from .schemas import NoteCreate
from .models import Note


class NoteCRUD(CRUDBase):
    def __init__(self):
        super().__init__(Note)

    async def create(self, session:Session, visit_id: int, data:NoteCreate,  user: User) -> Note:
        visit = await get_visit_by_id(session, visit_id)
        data = {
            "visit_id" : visit.id,
            "author" : user.id,
            **data.model_dump()
        }
        return await super().create(session, data)
    
note_crud = NoteCRUD()
visit_checker = VisitChecker(Note)

async def is_note_author(session: SessionDep, item_id: int, current_user: User = Depends(current_active_user)):
    note: Note = await note_crud.get_by_id(session, item_id)

    if current_user.id != note.author:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden: You are not the author of this note")
