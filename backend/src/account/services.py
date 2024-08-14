import uuid
from typing import Optional
from fastapi import Depends, Request, HTTPException, Response, status
from fastapi_users import BaseUserManager, FastAPIUsers, UUIDIDMixin
from fastapi_users.jwt import generate_jwt
from fastapi_users.db import SQLAlchemyUserDatabase

from src.core.config import settings
from src.core.dependecies import get_user_db
from src.authentication.services import auth_backend
from src.utils.email import send_new_account_email
from .models import User
from .schemas import Role

class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = settings.SECRET_KEY
    verification_token_secret = settings.SECRET_KEY
    verification_token_lifetime_seconds = settings.ACCESS_TOKEN_EXPIRE_MINUTES
    
    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

        token_data = {
            "sub": str(user.id),
            "email": user.email,
            "aud": self.verification_token_audience,
        }
        token = generate_jwt(
            token_data,
            self.verification_token_secret,
            self.verification_token_lifetime_seconds,
        )

        data = request._json
        await self._update(user, {"patient.first_name": data.get("first_name")})         
        send_new_account_email(user.email, token)

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"Verification requested for user {user.id}. Verification token: {token}")
        
        send_new_account_email(user.email, token)
        
    async def on_after_login(self, user: User, request: Request | None = None, response: Response | None = None) -> None:
        user_is_allowed = False
        if user.role.id in (Role.PATIENT,) or user.is_superuser:
            user_is_allowed = True
        else:
            if request.client.host in settings.ALLOWED_IPS.split(','):
                user_is_allowed = True
        await self._update(user, {"is_allowed": user_is_allowed})



async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)

fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager, [auth_backend])

current_active_user = fastapi_users.current_user(active=True)
current_active_superuser = fastapi_users.current_user(active=True, superuser=True)

class RoleChecker:
    def __init__(self, allowed_roles: list):
        self.allowed_roles = allowed_roles

    def __call__(self, user: User = Depends(current_active_user)):
        if (user.role.id not in self.allowed_roles) and not user.is_superuser:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Operation not permitted")
    