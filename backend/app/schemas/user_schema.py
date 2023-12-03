from uuid import uuid4, UUID
from typing import Union, List, Optional
from pydantic import BaseModel, Field


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class UserBase(BaseModel):
    username: str
    first_name: str
    last_name: str


class UserCreate(UserBase):
    password: str


class LoginSchema(BaseModel):
    username: str
    password: str


class UserUpdate(BaseModel):
    first_name: str
    last_name: str


class User(UserBase):
    id: UUID = Field(default_factory=uuid4)
    hashed_password: str

    class Config:
        orm_mode = True