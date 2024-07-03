
from sqlalchemy.ext.asyncio import AsyncSession as Session

from src.visit.services import get_visit_by_id

from src.utils.crud import CRUDBase
from src.account.models import User
from src.account.schemas import Role
from src.visit.dependencies import VisitChecker
from .schemas import LabTestCreate, LabStatus
from .models import LabTest


class LabTestCRUD(CRUDBase):
    def __init__(self):
        super().__init__(LabTest)

    async def create(self, session:Session, visit_id: int, data:LabTestCreate, user:User) -> LabTest:
        visit = await get_visit_by_id(session, visit_id)

        input = data.model_dump()

        if user.role_id == Role.LAB_TECH.value:
            data = {
                "visit_id" : visit.id,
                "status": LabStatus.COMPLETED,
                **data.model_dump(exclude=["status"])
            }
        else:
            data = {
                "visit_id": visit_id,
                "lab_type": input["lab_type"],
                "status": LabStatus.REQUESTED,
                **data.model_dump(exclude=["status"])
            }

        return await super().create(session, data)
        
labtest_crud = LabTestCRUD()
visit_checker = VisitChecker(LabTest)

