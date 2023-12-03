from fastapi import APIRouter, Depends

from app.api.endpoints import user_router, ticket_router
from app.crud.user_crud import get_current_active_user


api_router = APIRouter()
api_router.include_router(user_router.router, prefix='/user', tags=['user'])
api_router.include_router(ticket_router.router, prefix='/tickets', tags=['ticket'], dependencies=[Depends(get_current_active_user)])
