from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class SupplierBase(BaseModel):
    name: str
    contact_person: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    supply_category: Optional[str] = None

class SupplierCreate(SupplierBase):
    pass

class SupplierUpdate(BaseModel):
    name: Optional[str] = None
    contact_person: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    supply_category: Optional[str] = None
    status: Optional[bool] = None

class SupplierResponse(SupplierBase):
    id: int
    cooperation_start: Optional[datetime] = None
    status: bool
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class PurchaseOrderBase(BaseModel):
    supplier_id: int
    store_id: int
    total_amount: float = 0
    remark: Optional[str] = None

class PurchaseOrderCreate(PurchaseOrderBase):
    items: Optional[str] = None

class PurchaseOrderUpdate(BaseModel):
    status: Optional[str] = None
    total_amount: Optional[float] = None
    remark: Optional[str] = None

class PurchaseOrderResponse(PurchaseOrderBase):
    id: int
    order_no: str
    status: str
    items: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
