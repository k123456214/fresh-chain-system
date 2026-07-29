from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from datetime import datetime
from app.core.database import Base

class Member(Base):
    __tablename__ = "members"

    id = Column(Integer, primary_key=True, index=True)
    member_no = Column(String(50), unique=True, nullable=False)
    name = Column(String(50))
    phone = Column(String(20), unique=True, nullable=False)
    level = Column(String(20), default="normal")
    points = Column(Integer, default=0)
    balance = Column(Float, default=0)
    total_spent = Column(Float, default=0)
    store_id = Column(Integer)
    status = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class MemberLevel(Base):
    __tablename__ = "member_levels"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    min_points = Column(Integer, default=0)
    discount_rate = Column(Float, default=1.0)
    benefits = Column(String(500))
