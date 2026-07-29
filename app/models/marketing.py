from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text
from datetime import datetime
from app.core.database import Base

class Promotion(Base):
    __tablename__ = "promotions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    type = Column(String(20), default="discount")
    discount_rate = Column(Float, default=1.0)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    scope = Column(String(20), default="all")
    product_ids = Column(Text)
    status = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Coupon(Base):
    __tablename__ = "coupons"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    type = Column(String(20), default="cash")
    value = Column(Float, default=0)
    min_amount = Column(Float, default=0)
    total_count = Column(Integer, default=0)
    used_count = Column(Integer, default=0)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    status = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class MemberCoupon(Base):
    __tablename__ = "member_coupons"

    id = Column(Integer, primary_key=True, index=True)
    member_id = Column(Integer, nullable=False)
    coupon_id = Column(Integer, nullable=False)
    status = Column(String(20), default="unused")
    used_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
