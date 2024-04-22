from httpx import AsyncClient
from fastapi import status
from tests.utils.extra import user_data
from tests.utils.user import _create_user
from fastapi_users.manager import BaseUserManager
import pytest

@pytest.mark.asyncio
async def test_create_visit(authenticated_user: AsyncClient, user_manager: BaseUserManager) -> None:

    admin_as_patient = await user_manager.get_by_email("settings@firstsuperuser.com")
    data = {
        "reason_for_visit": "string",
        "visit_status": "checked_in",
        "patient_id": str(admin_as_patient.id)
    }
    user_credentials = user_data[4]
    await _create_user(user_manager, **user_credentials)
    r = await authenticated_user(**user_credentials)
    response = await r.post("/api/v1/visits/",json=data)
    
    assert response.status_code == status.HTTP_201_CREATED
