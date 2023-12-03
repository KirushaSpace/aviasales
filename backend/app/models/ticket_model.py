from datetime import datetime
from uuid import uuid4

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Integer, String, DateTime

from app.db.session import Base


class Ticket(Base):
    __tablename__ = "ticket"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    company = Column(String, index=True)
    description = Column(String, index=True)
    price = Column(Integer)
    airport_from = Column(String)
    airport_in = Column(String)
    datetime_from = Column(DateTime(timezone=True))
    datetime_in = Column(DateTime(timezone=True))

    @staticmethod
    def create_datetime(date, time):
        return datetime.combine(date, time)

    @staticmethod
    def split_datetime(datetime_value):
        return datetime_value.date(), datetime_value.time()
