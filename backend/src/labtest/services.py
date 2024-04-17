
from sqlalchemy.ext.asyncio import AsyncSession as Session

from src.visit.services import get_visit_by_id

from src.utils.crud import CRUDBase
from src.account.models import User
from src.visit.dependencies import VisitChecker
from .schemas import LabTestCreate
from .models import LabTest


class LabTestCRUD(CRUDBase):
    def __init__(self):
        super().__init__(LabTest)

    async def create(self, session:Session, visit_id: int, data:LabTestCreate) -> LabTest:
        visit = await get_visit_by_id(session, visit_id)
        data = {
            "visit_id" : visit.id,
            **data.model_dump()
        }
        return await super().create(session, data)
        
labtest_crud = LabTestCRUD()
visit_checker = VisitChecker(LabTest)

