from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class InventoryBase(BaseModel):
    store_id: int
    product_id: int
    quantity: float = 0
    warning_quantity: float = 0

class InventoryCreate(InventoryBase):
    pass

class InventoryUpdate(BaseModel):
    quantity: Optional[float] = None
    warning_quantity: Optional[float] = None

class InventoryResponse(InventoryBase):
    id: int
    last_restock_date: Optional[datetime] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class InventoryRecordBase(BaseModel):
    store_id: int
    product_id: int
    type: str
    quantity: float = 0
    remark: Optional[str] = None

class InventoryRecordCreate(InventoryRecordBase):
    operator_id: Optional[int] = None

class InventoryRecordResponse(InventoryRecordBase):
    id: int
    before_quantity: float
    after_quantity: float
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
