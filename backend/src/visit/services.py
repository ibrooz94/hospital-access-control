from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession as Session
from sqlalchemy.orm import selectinload
from sqlalchemy import select, func, update

from src.account.models import User
from src.account.schemas import Role
from src.appointment.services import appointment_crud
from .schemas import VisitCreate, VisitBase, VisitUpdate, VisitStatus
from .models import Visit




async def create_visit(session:Session, request:VisitCreate, user:User) -> Visit:

    if user.role_id == Role.PATIENT:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Operation not permitted for base user")
    
    data = request.model_dump()
    if data["appointment_id"] is not None:
        await appointment_crud.get_by_id(session, data["appointment_id"])

    visit = Visit(**data)

    session.add(visit)
    await session.commit()
    await session.refresh(visit)

    return visit

async def get_visit_by_id(session:Session, visit_id: int, with_option: bool = False) -> Visit:
    
    if with_option:
        statement = select(Visit).where(Visit.id == visit_id).options(
            selectinload(Visit.vitals),
            selectinload(Visit.notes),
            selectinload(Visit.labtests),
            selectinload(Visit.appointment))
    else:
        statement = select(Visit).where(Visit.id == visit_id)

    visit = (await session.execute(statement)).scalar()

    if not visit:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Visit not found")
    
    return visit

async def get_all_visits_patient(session: Session, patient_id: UUID, skip: int, limit: int):

    stmt = select(Visit).where(Visit.patient_id == patient_id).limit(limit).offset(skip)
    visits = (await session.execute(stmt)).scalars().all()

    visits_out = [VisitBase(**visit.__dict__) for visit in visits]

    return visits_out

async def update_visit(session: Session, visit_id: int, request:VisitUpdate):

    visit: Visit = await get_visit_by_id(session, visit_id)

    if visit.discharged_at is not None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cannot update 'discharged' visit")

    visit_data = request.model_dump()
    if visit_data["visit_status"] == VisitStatus.DISCHARGED:
        visit_data["discharged_at"] = func.now()

    stmt = update(Visit).where(Visit.id == visit_id).values(visit_data).returning(Visit)
    visit = (await session.execute(stmt)).scalar()

    await session.commit()
    await session.refresh(visit)

    return visit

async def delete_visit(session: Session, visit_id: int):

    visit = await get_visit_by_id(session, visit_id)

    try:
        await session.delete(visit)
        await session.commit()
        return True
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Error deleting object: {str(e)}",
        )



