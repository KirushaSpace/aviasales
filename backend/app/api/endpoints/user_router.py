from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.db.session import get_db

from app.models.user_model import User
from app.schemas import user_schema
from app.crud import user_crud

ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter()


@router.post("/registration", response_model=user_schema.Token)
async def user_registration(user: user_schema.UserCreate, db: AsyncSession = Depends(get_db)):
    exist_user = await user_crud.get_user(db=db, username=user.username)
    if exist_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This username already exist"
        )

    user = await user_crud.create_user(db=db, user=user)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = user_crud.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/token", response_model=user_schema.Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: AsyncSession = Depends(get_db)
):
    user = await user_crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = user_crud.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=user_schema.User)
async def read_users_me(current_user: Annotated[User, Depends(user_crud.get_current_active_user)]):
    return current_user


# @router.put("/update", response_model=user_schema.User)
# def update_user(new_user_data: user_schema.UserUpdate, current_user: User = Depends(crud.get_current_user), db: AsyncSession = Depends(get_db)):
#     return user_crud.update_user(new_user_data=new_user_data, current_user=current_user, db=db)