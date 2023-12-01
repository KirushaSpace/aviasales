from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_async_sqlalchemy import SQLAlchemyMiddleware
import uvicorn

from app.models.database import Base, engine
from app.api.api import api_router

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

