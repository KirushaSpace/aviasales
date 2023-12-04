from uuid import UUID
from datetime import timedelta

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql import Select, and_

from app.models.ticket_model import Ticket as TicketModel
from app.schemas.ticket_schema import TicketCreate, Ticket


async def create_ticket(db: AsyncSession, ticket: TicketCreate):
    db_ticket = TicketModel(
        company=ticket.company,
        description=ticket.description,
        price=ticket.price,
        airport_from=ticket.airport_from,
        airport_in=ticket.airport_in,
        datetime_from=ticket.datetime_from,
        datetime_in=ticket.datetime_in
    )

    db.add(db_ticket)
    await db.commit()
    await db.refresh(db_ticket)
    return db_ticket


async def get_multi(db: AsyncSession, query: TicketModel | Select[TicketModel] = None, skip: int = 0, limit: int = 100):
    if query is None:
        query = select(TicketModel).offset(skip).limit(limit).order_by(TicketModel.id)
    response = await db.execute(query)
    return response.scalars().all()


async def get_by_id(db: AsyncSession, id: UUID):
    query = select(TicketModel).where(TicketModel.id == id)
    response = await db.execute(query)
    return response.scalar_one_or_none()


async def delete(db: AsyncSession, id: UUID):
    query = select(TicketModel).where(TicketModel.id == id)
    response = await db.execute(query)
    ticket = response.scalar_one()
    await db.delete(ticket)
    await db.commit()
    return ticket


async def get_alternative(db: AsyncSession, params: dict):
    query = select(TicketModel).filter(TicketModel.airport_from == params['airport_from'])
    tickets = await get_multi(db=db, query=query)
    alternative_flights = []
    for ticket in tickets:
        visited = set()
        async for way in dfs_paths(ticket, params['airport_in'], db, visited):
            if len(way) > 1:
                alternative_flights += [way]
        
    return alternative_flights


async def dfs_paths(ticket_start: TicketModel,  airport_in: str, db: AsyncSession, visited: set, path=None):
    visited.add(ticket_start.airport_from)
    if path is None:
        path = [ticket_start]
    if ticket_start.airport_in == airport_in:
        yield path
    query = select(TicketModel).filter(and_(TicketModel.airport_from == ticket_start.airport_in, 
                                            TicketModel.datetime_from - ticket_start.datetime_in <= timedelta(days=2), 
                                            TicketModel.datetime_from - ticket_start.datetime_in >= timedelta(minutes=10)
                                            )
                                        )
    tickets_airport_in = await get_multi(db=db, query=query)
    for next in list(tickets_airport_in):
        if next.airport_in not in visited:
            async for way in dfs_paths(next, airport_in, db, visited, path + [next]):
                yield way
