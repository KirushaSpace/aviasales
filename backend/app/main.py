from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_async_sqlalchemy import SQLAlchemyMiddleware
import uvicorn
from app.config import settings
from app.api.api import api_router
from fastapi_async_sqlalchemy import db
from sqlmodel import text
from contextlib import asynccontextmanager
from app.db.session import sessionmanager

sessionmanager.init(settings.DATABASE_URL)

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    if sessionmanager._engine is not None:
        await sessionmanager.close()

app = FastAPI()
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    SQLAlchemyMiddleware,
    db_url=settings.DATABASE_URL,
    engine_args={
        "echo": False,
        "pool_pre_ping": True,
        "pool_size": 9,
        "max_overflow": 64,
    },
)

async def add_postgresql_extension() -> None:
    async with db():
        query = text("CREATE EXTENSION IF NOT EXISTS pg_trgm")
        return await db.session.execute(query)

@app.on_event("startup")
async def on_startup():
    print("startup fastapi")
    await add_postgresql_extension()