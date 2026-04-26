from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

# Infrastructure
from app.configs.environment import get_environment_settings
#from app.configs.database import Engine, AssyncSessionLocal
from app.models.base_sqlalchemy import init_db
from app.core.exceptions import AppException

# Seed

# Routers
from app.routers.v1 import (
    user_routers,
    address_routers,
    order_routers,
    tracking_routers
)


env = get_environment_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up database...")
    await init_db()
    print("Database initialized.")
    yield
    print("Shutting down database...")

app = FastAPI(
    title=env.APP_NAME,
    version=env.API_VERSION,
    lifespan=lifespan
)

app.add_middleware(
    SessionMiddleware,
    secret_key=env.SECRET_KEY,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(user_routers.router)
app.include_router(address_routers.router)
app.include_router(order_routers.router)
app.include_router(tracking_routers.router)

@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )