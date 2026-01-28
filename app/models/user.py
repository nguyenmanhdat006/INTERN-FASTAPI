from sqlalchemy import Column, String, Boolean, Date, DateTime
from datetime import datetime

from tokenize import String
from xmlrpc.client import DateTime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from app.core.database import Base



class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    keycloak_id = Column(String, unique=True, nullable=False)

    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)

    first_name = Column(String)
    last_name = Column(String)
    dob = Column(Date)

    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
