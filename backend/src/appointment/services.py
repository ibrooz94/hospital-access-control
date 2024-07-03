from typing import Any, Dict
from fastapi import HTTPException, status
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload, aliased
from sqlalchemy.ext.asyncio import AsyncSession as Session
from fastapi_users.exceptions import UserNotExists
from datetime import datetime

from src.utils.crud import CRUDBase
from src.account.models import User
from src.account.schemas import Role
from src.account.services import UserManager

from src.visit.dependencies import VisitChecker
from .schemas import AppointmentCreate, AppointmentStatus
from .models import Appointment


class AppointmentCRUD(CRUDBase):
    def __init__(self):
        super().__init__(Appointment)

    async def find_available_doctor(self, session: Session):
        # Get all doctors with pending appointment
        doctors_pending_appointments =  (
            select(Appointment.assigned_doctor)
            .join(User, User.id == Appointment.assigned_doctor)
            .where(Appointment.status == AppointmentStatus.PENDING, Appointment.assigned_doctor != None)
            .group_by(Appointment.assigned_doctor)
            .order_by(func.count(Appointment.id).desc()) 
        )
        free_doctor_query = (
            select(User.id)
            .where(User.id.not_in(doctors_pending_appointments), User.role_id == 4)
            )
        # get a doctor that's not having a pending appointment
        free_doctors = (await session.execute(free_doctor_query)).scalars().all()
        
        # if no free doctors, get doctor with the least amount of appointments
        if free_doctors:
            free_doctor = free_doctors[0]
        else:
            f_doctor = (await session.execute(doctors_pending_appointments)).scalars().all()
            free_doctor = f_doctor[0]

        return free_doctor
    
    async def create(
        self, session: Session, data: AppointmentCreate, user: User, user_manager: UserManager
    ) -> Appointment:
        if user.role_id == Role.PATIENT:
            available_doctor = await self.find_available_doctor(session)
            data = {
                "on_behalf_of": user.id,
                "status": AppointmentStatus.PENDING,
                "assigned_doctor": available_doctor,
                **data.model_dump(exclude=["on_behalf_of", "requested_by"]),
            }
        elif user.role_id == Role.DOCTOR:
            try:
                patient = await user_manager.get_by_email(data.on_behalf_of)
            except UserNotExists:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail=f"PATIENT not found"
                ) 
            data = {
                "requested_by": user.id,
                "on_behalf_of": patient.id,
                "status": AppointmentStatus.BOOKED,
                "assigned_doctor": user.id,
                **data.model_dump(exclude=["on_behalf_of", "requested_by"]),
            }
        else:
            data = {
                "requested_by": user.id,
                "status": AppointmentStatus.PENDING,
                **data.model_dump(exclude=()),
            }

        return await super().create(session, data)

    async def get_by_id(self, session: Session, id: int) -> Appointment:
        query = (
            select(self.model)
            .where(self.model.id == id)
            .options(selectinload(Appointment.patient))
        )
        result = (await session.execute(query)).scalar()
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{self.model.__name__} not found",
            )
        return result

    async def get_all(
        self,
        session: Session,
        user: User,
        skip: int = 0,
        limit: int = 100,
        sort: str | None = None,
        filter_by: Dict[str, Any] | None = None,
        date_from: datetime | None = None,
        date_to: datetime | None = None,
    ) -> list[Appointment]:
        q = select(Appointment).options(selectinload(Appointment.patient), selectinload(Appointment.doctor))

        if user.is_superuser:
            pass           
        elif user.role.id == Role.PATIENT.value :
            q = q.where(Appointment.on_behalf_of == user.id)
        elif user.role.id == Role.DOCTOR.value:
            q = q.where(Appointment.assigned_doctor == user.id )
        elif user.role.id in (Role.LAB_TECH, Role.NURSE):
            q = q.where(Appointment.requested_by == user.id )


        # Filter by date range (if provided)
        if date_from and date_to:
            q = q.where(Appointment.scheduled_date.between(date_from, date_to))
        elif date_from:
            q = q.where(Appointment.scheduled_date >= date_from)
        elif date_to:
            q = q.where(Appointment.scheduled_date <= date_to)

        query = self.apply_filtering_sorting_pagination(q, skip, limit, sort, filter_by)
        result = await session.execute(query)
        return result.scalars().all()


appointment_crud = AppointmentCRUD()
visit_checker = VisitChecker(Appointment)
