from uuid import uuid4

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Integer, String

from app.db.session import Base


class User(Base):
    __tablename__ = "user"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    username = Column(String, unique=True)
    hashed_password = Column(String)
    first_name = Column(String)
    last_name = Column(String)
