from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from datetime import datetime
from app.core.database import Base

class Store(Base):
    __tablename__ = "stores"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    code = Column(String(50), unique=True, nullable=False)
    address = Column(String(255))
    phone = Column(String(20))
    manager = Column(String(50))
    area = Column(Float, default=0)
    status = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
