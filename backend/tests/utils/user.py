from httpx import AsyncClient
from fastapi_users.manager import BaseUserManager

from src.account.schemas import UserCreateRole
from src.account.models import User

async def _create_user(
        user_manager: BaseUserManager, email:str, password:str,
        role_id:int = 1, is_superuser: bool = False) -> User:

    user = await user_manager.create(
        UserCreateRole(
            email= email, password=password, is_superuser=is_superuser, role_id=role_id
        )
    )
    return user

async def user_authentication_headers(
    async_client: AsyncClient, email: str, password: str
) -> dict[str, str]:

    data = {"username": email, "password": password}

    r = await async_client.post(f"/api/v1/auth/jwt/login", data=data)
    assert r.status_code == 204, "Authentication Failed"
    # auth_token = response["access_token"]
    # headers = {"authorization": f"Bearer {auth_token}"}
    # return headers


async def get_superuser_token_headers(async_client: AsyncClient) -> dict[str, str]:
    login_data = {
        "username": "settings@firstsuperuser.com",
        "password": "settings.FIRST_SUPERUSER_PASSWORD"
    }
    r = await async_client.post(f"/api/v1/auth/jwt/login", data=login_data)
    assert r.status_code == 204, "Authentication failed"
