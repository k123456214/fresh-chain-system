from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class OrderItemBase(BaseModel):
    product_id: int
    product_name: str
    quantity: float = 0
    unit_price: float = 0
    weight: float = 0

class OrderItemCreate(OrderItemBase):
    pass

class OrderBase(BaseModel):
    store_id: int
    member_id: Optional[int] = None
    pay_method: str = "cash"
    remark: Optional[str] = None

class OrderCreate(OrderBase):
    items: List[OrderItemCreate]

class OrderUpdate(BaseModel):
    status: Optional[str] = None
    remark: Optional[str] = None

class OrderResponse(OrderBase):
    id: int
    order_no: str
    cashier_id: Optional[int] = None
    total_amount: float
    discount_amount: float
    final_amount: float
    status: str
    items: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class OrderItemResponse(OrderItemBase):
    id: int
    order_id: int
    subtotal: float

    class Config:
        from_attributes = True
