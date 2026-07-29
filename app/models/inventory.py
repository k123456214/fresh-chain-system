from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from app.core.database import Base

class Inventory(Base):
    __tablename__ = "inventories"

    id = Column(Integer, primary_key=True, index=True)
    store_id = Column(Integer, nullable=False)
    product_id = Column(Integer, nullable=False)
    quantity = Column(Float, default=0)
    warning_quantity = Column(Float, default=0)
    last_restock_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class InventoryRecord(Base):
    __tablename__ = "inventory_records"

    id = Column(Integer, primary_key=True, index=True)
    store_id = Column(Integer, nullable=False)
    product_id = Column(Integer, nullable=False)
    type = Column(String(20), nullable=False)
    quantity = Column(Float, default=0)
    before_quantity = Column(Float, default=0)
    after_quantity = Column(Float, default=0)
    remark = Column(String(500))
    operator_id = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
