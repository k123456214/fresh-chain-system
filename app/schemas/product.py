from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ProductBase(BaseModel):
    name: str
    code: str
    barcode: Optional[str] = None
    category: Optional[str] = None
    unit: str = "kg"
    price: float = 0
    cost_price: float = 0
    stock: float = 0
    min_stock: float = 0
    max_stock: float = 0
    supplier_id: Optional[int] = None
    description: Optional[str] = None

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    barcode: Optional[str] = None
    category: Optional[str] = None
    unit: Optional[str] = None
    price: Optional[float] = None
    cost_price: Optional[float] = None
    stock: Optional[float] = None
    min_stock: Optional[float] = None
    max_stock: Optional[float] = None
    supplier_id: Optional[int] = None
    description: Optional[str] = None
    status: Optional[bool] = None

class ProductResponse(ProductBase):
    id: int
    status: bool
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
