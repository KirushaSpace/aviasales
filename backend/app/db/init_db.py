import json

from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import Depends

from app.crud import ticket_crud
from app.db.session import get_db
from app.models.ticket_model import Ticket as TicketModel
from app.schemas.ticket_schema import TicketCreate


async def init_db(db: AsyncSession = Depends(get_db)):
    with open('app/db/data.json') as f:
        data = json.load(f)
    
    tickets = [TicketCreate(**ticket) for ticket in data]

    for ticket in tickets:
        await ticket_crud.create_ticket(db, ticket)
        