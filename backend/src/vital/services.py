from sqlalchemy.ext.asyncio import AsyncSession as Session

from src.visit.services import get_visit_by_id
from src.utils.crud import CRUDBase
from src.account.models import User
from src.visit.dependencies import VisitChecker
from .schemas import VitalCreate
from .models import Vital


class VitalCRUD(CRUDBase):
    def __init__(self):
        super().__init__(Vital)

    async def create(self, session:Session, visit_id: int, data:VitalCreate,  user: User) -> Vital:
        visit = await get_visit_by_id(session, visit_id)
        data = {
            "visit_id" : visit.id,
            "taken_by" : user.id,
            **data.model_dump()
        }
        return await super().create(session, data)
    
    ## TODO add patient_id to vital table
    # async def get_all_by_patient(self, session: Session, patient_id: UUID, skip: int = 0, limit: int = 100) -> list[Any]:

    #     query = select(self.model).where(Vital.visit.patient_id == patient_id).offset(skip).limit(limit)
    #     result = await session.execute(query)
    #     return result.scalars().all()
    

vital_crud = VitalCRUD()
visit_checker = VisitChecker(Vital)

