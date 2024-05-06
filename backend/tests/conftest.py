import pytest
import pytest_asyncio
import asyncio
import contextlib
from typing import AsyncGenerator
from httpx import AsyncClient, ASGITransport
from sqlalchemy import insert

from src.main import app as _app
from src.core.dependecies import get_db, get_user_db
from src.core.database import sessionmanager, Base
from src.account.services import get_user_manager
from src.account.models import Role
from src.account.schemas import UserCreate
from tests.utils.user import _create_user, get_superuser_token_headers, user_authentication_headers
from contextlib import ExitStack
from fastapi import FastAPI


get_user_db_context = contextlib.asynccontextmanager(get_user_db)
get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)
connection_str = f"postgresql+psycopg://postgres:root@localhost:5432/test_db"

@pytest.fixture(autouse=True)
def app():
    with ExitStack():
        yield _app

@pytest.fixture()
async def async_client(app) -> AsyncGenerator:
    async with ASGITransport(app=app) as transport:
        async with AsyncClient(transport=transport, base_url="https://test") as c:
            yield c

@pytest_asyncio.fixture(scope="session")
def event_loop_policy() -> asyncio.AbstractEventLoopPolicy:
    return asyncio.WindowsSelectorEventLoopPolicy()

@pytest.fixture(scope="session", autouse=True)
async def connection_test(event_loop_policy):
    sessionmanager.init(connection_str)
    yield
    await sessionmanager.close()


@pytest.fixture(scope="function", autouse=True)
async def session_override(app: FastAPI, connection_test):
    async def get_db_override():
        async with sessionmanager.session() as session:
            yield session

    app.dependency_overrides[get_db] = get_db_override

@pytest.fixture(scope="function", autouse=True)
async def create_tables(connection_test):
    stmt = insert(Role).values([
            dict(name="patient"),
            dict(name="labtech"),
            dict(name="nurse"),
            dict(name="doctor"),
        ])
    async with sessionmanager.connect() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)
        await connection.execute(stmt)
        
@pytest.fixture(scope="function", autouse=True)
async def user_manager(connection_test):
    async with sessionmanager.session() as session:
        async with get_user_db_context(session) as user_db:
            async with get_user_manager_context(user_db) as user_manager:
                yield user_manager

@pytest.fixture(scope="function", autouse=True)
async def create_roles(request, user_manager, create_tables):    
    s_email = "settings@firstsuperuser.com"
    s_password = "settings.FIRST_SUPERUSER_PASSWORD"

    await user_manager.create(
        UserCreate(
            email=s_email, password=s_password, is_superuser=True
        )
    )

@pytest.fixture
async def authenticated_superuser(app: FastAPI, async_client: AsyncClient):
    await get_superuser_token_headers(async_client)
    # async_client.headers["Authorization"] = response['authorization']
    yield async_client

@pytest.fixture
async def authenticated_user(async_client):
    async def _auth(email:str, password:str, *args, **kwargs):
        await user_authentication_headers(async_client, email, password)
        return async_client

    authenticated_client = _auth

    yield authenticated_client