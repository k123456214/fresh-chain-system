from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from datetime import datetime
from app.core.database import Base

class LossRecord(Base):
    __tablename__ = "loss_records"

    id = Column(Integer, primary_key=True, index=True)
    store_id = Column(Integer, nullable=False)
    product_id = Column(Integer, nullable=False)
    product_name = Column(String(200))
    quantity = Column(Float, default=0)
    reason = Column(String(50))
    amount = Column(Float, default=0)
    handler_id = Column(Integer)
    remark = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
