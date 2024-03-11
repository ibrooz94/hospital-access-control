from fastapi import APIRouter, HTTPException
from src.core.dependecies import SessionDep
from .schemas import UserBase, UserCreate
from . import services
from .models import User

router = APIRouter()


@router.post("/register", response_model=UserBase)
async def create_user(request: UserCreate, session:SessionDep):
    user = await services.get_user_by_email(session=session, email=request.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )

    response = await services.create_user(session, request)
    return response

@router.get("/users", response_model=list[UserBase])
async def get_all_users(session: SessionDep):
    # Fetch all users using query
    users = await session.query(User).all()
    return users
