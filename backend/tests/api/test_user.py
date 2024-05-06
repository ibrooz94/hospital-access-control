from httpx import AsyncClient
from fastapi import status
from tests.utils.extra import user_data
from tests.utils.user import _create_user

async def test_register_user(async_client: AsyncClient) -> None:
    response = await async_client.post(
        "/api/v1/auth/register", 
        json={"email": "teswt@example.com","password":"pool"})
    
    assert response.status_code == status.HTTP_201_CREATED


async def test_get_users_superuser_me(authenticated_superuser: AsyncClient) -> None:

    r = await authenticated_superuser.get(f"api/v1/user/me")
    assert r.status_code == status.HTTP_200_OK

    current_user = r.json()
    assert current_user
    assert current_user["is_active"] is True
    assert current_user["is_superuser"]
    assert current_user["email"] == "settings@firstsuperuser.com"

async def test_nurse_role(authenticated_user: AsyncClient, user_manager) -> None:

    user_credentials = user_data[3] # nurse 
    await _create_user(user_manager, **user_credentials)
    r: AsyncClient = await authenticated_user(**user_credentials)

    response = await r.get(f"api/v1/user/me")
    assert response.status_code == status.HTTP_200_OK

    current_user = response.json()
    assert current_user
    assert current_user["is_active"] is True
    assert current_user["is_superuser"] is False
    assert current_user["role_id"] == 3

