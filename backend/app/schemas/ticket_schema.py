from uuid import UUID
from datetime import datetime
from pydantic import BaseModel


class TicketBase(BaseModel):
    title: str
    description: str
    price: int
    airport_from: str
    airport_in: str
    datetime_from: datetime
    datetime_in: datetime


class TicketCreate(TicketBase):
    pass


class Ticket(TicketBase):
    id: UUID

    class Config:
        orm_mode = True
