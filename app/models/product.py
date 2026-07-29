from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text
from datetime import datetime
from app.core.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    code = Column(String(50), unique=True, nullable=False)
    barcode = Column(String(50))
    category = Column(String(50))
    unit = Column(String(20), default="kg")
    price = Column(Float, default=0)
    cost_price = Column(Float, default=0)
    stock = Column(Float, default=0)
    min_stock = Column(Float, default=0)
    max_stock = Column(Float, default=0)
    supplier_id = Column(Integer)
    description = Column(Text)
    status = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
