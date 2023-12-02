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


@app.on_event("startup")
async def on_startup():
    print("startup fastapi")
