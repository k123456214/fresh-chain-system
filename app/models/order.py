from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from datetime import datetime
from app.core.database import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    order_no = Column(String(50), unique=True, nullable=False, index=True)
    store_id = Column(Integer, nullable=False)
    cashier_id = Column(Integer)
    member_id = Column(Integer)
    total_amount = Column(Float, default=0)
    discount_amount = Column(Float, default=0)
    final_amount = Column(Float, default=0)
    pay_method = Column(String(20), default="cash")
    status = Column(String(20), default="pending")
    remark = Column(String(500))
    items = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, nullable=False)
    product_id = Column(Integer, nullable=False)
    product_name = Column(String(200))
    quantity = Column(Float, default=0)
    unit_price = Column(Float, default=0)
    subtotal = Column(Float, default=0)
    weight = Column(Float, default=0)
