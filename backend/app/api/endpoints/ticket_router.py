from datetime import date, time, datetime
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

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
    price_r: int = 1000000, 
    airport_from: str = None,
    airport_in: str = None,
    date_from: date = None,
    time_from: time = None,
    date_in: date = None,
    time_in: time = None,
    skip: int = 0, 
    limit: int = 100
):
    query = select(TicketModel).filter(and_(TicketModel.price >=  price_l, TicketModel.price <= price_r))

    if airport_from:
        query = query.filter(TicketModel.airport_from == airport_from)

    if airport_in:
        query = query.filter(TicketModel.airport_in == airport_in)

    date_now = datetime.now()
    query = query.filter(
        TicketModel.datetime_from >= TicketModel.create_datetime(
            date_from if date_from else date_now.date(), 
            time_from if time_from else time(0, 0)
        )
    )

    if date_in:
        query = query.filter(
            TicketModel.datetime_in <= TicketModel.create_datetime(
                date_in, 
                time_in if time_in else time(23, 59)
            )
        )

    return await ticket_crud.get_multi(db=db, skip=skip, limit=limit, query=query)


@router.get("/{ticket_id}")
async def get_ticket(ticket_id: UUID, db: AsyncSession = Depends(get_db())):
    current_ticket = await ticket_crud.get_by_id(db, id)

    if not current_ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    return current_ticket


@router.delete("/{ticket_id}")
async def delete_ticket(ticket_id: UUID, db: AsyncSession = Depends(get_db())):
    current_ticket = await ticket_crud.get_by_id(db, id)

    if not current_ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    ticket = await ticket_crud.delete(db, id)
    return {"ticket": ticket, "delete": "done"}
