from sqlalchemy.orm import declarative_base
from typing import List, Optional
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from app.db.session import Base
class Ticket(Base):
    __tablename__ = "ticket"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    title = Column(String, index=True)
    description = Column(String, index=True)
    price = Column(Integer)
    airport_from = Column(String)
    airport_in = Column(String)
    date_from = Column(DateTime)
    date_in = Column(DateTime)
