from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class StoreBase(BaseModel):
    name: str
    code: str
    address: Optional[str] = None
    phone: Optional[str] = None
    manager: Optional[str] = None
    area: Optional[float] = 0

class StoreCreate(StoreBase):
    pass

class StoreUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    manager: Optional[str] = None
    area: Optional[float] = None
    status: Optional[bool] = None

class StoreResponse(StoreBase):
    id: int
    status: bool
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
