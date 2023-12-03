from datetime import timedelta


from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db.session import get_db
from app.models.ticket_model import Ticket as TicketModel
from app.models.user_model import User
from app.crud import ticket_crud, user_crud
from app.schemas.ticket_schema import Ticket, TicketCreate


router = APIRouter()


@router.post("", response_model=Ticket)
async def create_ticket(ticket: TicketCreate, db: AsyncSession = Depends(get_db)):
    new_ticket = await ticket_crud.create_ticket(db, ticket)
    return new_ticket


@router.get("")
async def get_tickets(db: AsyncSession = Depends(get_db), skip: int = 0, limit: int = 100):
    return await ticket_crud.get_multi(db=db, skip=skip, limit=limit)



# @router.get("/{ticket_id}")