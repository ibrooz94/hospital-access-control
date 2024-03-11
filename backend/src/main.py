from fastapi import FastAPI, APIRouter
from fastapi.routing import APIRoute
from starlette.middleware.cors import CORSMiddleware
from src.core.config import settings

from src.accounts import routes as user_routes

def custom_generate_unique_id(route: APIRoute):
    return f"{route.tags[0]}-{route.name}"


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    generate_unique_id_function=custom_generate_unique_id,
)

if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            str(origin).strip("/") for origin in settings.BACKEND_CORS_ORIGINS
        ],
        allow_credentials = True,
        allow_methods = ['*'],
        allow_headers=["*"]
    )

# Register all routes here
api_router = APIRouter()
api_router.include_router(user_routes.router, prefix="/users", tags=["users"])


app.include_router(api_router, prefix=settings.API_V1_STR)