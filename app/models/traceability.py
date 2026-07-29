from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from datetime import datetime
from app.core.database import Base

class Traceability(Base):
    __tablename__ = "traceabilities"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, nullable=False)
    product_name = Column(String(200))
    batch_no = Column(String(50))
    origin = Column(String(200))
    supplier = Column(String(200))
    harvest_date = Column(DateTime)
    arrival_date = Column(DateTime)
    storage_condition = Column(String(100))
    quality_report = Column(Text)
    status = Column(String(20), default="normal")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class TraceabilityStep(Base):
    __tablename__ = "traceability_steps"

    id = Column(Integer, primary_key=True, index=True)
    traceability_id = Column(Integer, nullable=False)
    step_no = Column(Integer, default=1)
    step_name = Column(String(100))
    description = Column(Text)
    operator = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)
