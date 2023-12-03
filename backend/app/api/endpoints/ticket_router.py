from datetime import timedelta


from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import and_
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


@router.get("", response_model=list[Ticket])
async def get_tickets(
    db: AsyncSession = Depends(get_db), 
    price_l: int = 0, 
    price_r: int = 999999, 
    airport_from: str = None,
    airport_in: str = None, 
    skip: int = 0, 
    limit: int = 100
):
    query = select(TicketModel).filter(and_(TicketModel.price >=  price_l, TicketModel.price <= price_r))
    if airport_from:
        query = query.filter(TicketModel.airport_from == airport_from)
    if airport_in:
        query = query.filter(TicketModel.airport_in == airport_in)
    return await ticket_crud.get_multi(db=db, skip=skip, limit=limit, query=query)



# @router.get("/{ticket_id}")