from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float
from datetime import datetime
from app.core.database import Base

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    phone = Column(String(20))
    position = Column(String(50))
    department = Column(String(50))
    store_id = Column(Integer)
    entry_date = Column(DateTime)
    status = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Schedule(Base):
    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, nullable=False)
    store_id = Column(Integer)
    shift_date = Column(DateTime, nullable=False)
    shift_type = Column(String(20))
    start_time = Column(String(10))
    end_time = Column(String(10))
