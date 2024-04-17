from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession as Session

from src.utils.crud import CRUDBase
from src.account.models import User
from src.account.schemas import Role
from src.visit.dependencies import VisitChecker
from src.visit.models import Visit
from .schemas import AppointmentCreate, AppointmentStatus
from .models import Appointment



class AppointmentCRUD(CRUDBase):
    def __init__(self):
        super().__init__(Appointment)

    async def create(self, session:Session, data:AppointmentCreate,  user: User) -> Appointment:

        if user.role_id == Role.PATIENT:
            print("User is a patient")
            data = {
                "on_behalf_of": user.id,
                "status": AppointmentStatus.PENDING,
                **data.model_dump(exclude=["on_behalf_of", "requested_by"])
            }
        else:
            data = {
                "requested_by": user.id,
                "status": AppointmentStatus.PENDING,
                **data.model_dump()
            }

        return await super().create(session, data)
        
    async def get_by_id(self, session: Session, id: int) -> Appointment:
        query = select(self.model).where(self.model.id == id).options(selectinload(Appointment.visit))
        result = (await session.execute(query)).scalar()
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"{self.model.__name__} not found"
            )
        return result 

appointment_crud = AppointmentCRUD()
visit_checker = VisitChecker(Appointment)

