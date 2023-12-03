from uuid import UUID
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql import Select

from fastapi import Depends, HTTPException, status

from app.models.ticket_model import Ticket as TicketModel
from app.schemas.ticket_schema import TicketCreate, Ticket


async def create_ticket(db: AsyncSession, ticket: TicketCreate):
    db_ticket = TicketModel(
        title=ticket.title,
        description=ticket.description,
        price=ticket.price,
        airport_from=ticket.airport_from,
        airport_in=ticket.airport_in,
        date_from=ticket.date_from,
        date_in=ticket.date_in
    )

    db.add(db_ticket)
    await db.commit()
    await db.refresh(db_ticket)
    return db_ticket


async def get_multi(db: AsyncSession, query: TicketModel | Select[TicketModel] = None, skip: int = 0, limit: int = 100, ):
    if query is None:
        query = select(TicketModel).offset(skip).limit(limit).order_by(TicketModel.id)
    response = await db.execute(query)
    return response.scalars().all()
