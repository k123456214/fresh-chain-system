from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class LossRecordBase(BaseModel):
    store_id: int
    product_id: int
    product_name: Optional[str] = None
    quantity: float = 0
    reason: str
    amount: float = 0
    handler_id: Optional[int] = None
    remark: Optional[str] = None

class LossRecordCreate(LossRecordBase):
    pass

class LossRecordUpdate(BaseModel):
    quantity: Optional[float] = None
    reason: Optional[str] = None
    amount: Optional[float] = None
    remark: Optional[str] = None

class LossRecordResponse(LossRecordBase):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
