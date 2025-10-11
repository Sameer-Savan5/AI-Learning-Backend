from sqlalchemy import Column, String, Integer, TIMESTAMP
from sqlalchemy.sql import func
from database import Base   # ✅ now database.py exists

class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, index=True)
    username = Column(String(255), nullable=False, unique=True)
    email = Column(String(255), nullable=False, unique=True)
    age = Column(Integer)
    created_at = Column(TIMESTAMP, server_default=func.now())