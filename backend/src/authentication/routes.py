
from fastapi import APIRouter
from src.accounts.schemas import UserCreate, UserRead, UserCreatePublic
from src.accounts.services import fastapi_users
from .services import auth_backend

router = APIRouter()

router.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/jwt"
)
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreatePublic)
)
router.include_router(
    fastapi_users.get_reset_password_router()
)
router.include_router(
    fastapi_users.get_verify_router(UserRead)
)
