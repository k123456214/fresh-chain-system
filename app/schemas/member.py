from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class MemberBase(BaseModel):
    name: Optional[str] = None
    phone: str
    level: str = "normal"
    store_id: Optional[int] = None

class MemberCreate(MemberBase):
    pass

class MemberUpdate(BaseModel):
    name: Optional[str] = None
    level: Optional[str] = None
    balance: Optional[float] = None
    store_id: Optional[int] = None
    status: Optional[bool] = None

class MemberResponse(MemberBase):
    id: int
    member_no: str
    points: int
    balance: float
    total_spent: float
    status: bool
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class MemberLevelBase(BaseModel):
    name: str
    min_points: int = 0
    discount_rate: float = 1.0
    benefits: Optional[str] = None

class MemberLevelCreate(MemberLevelBase):
    pass

class MemberLevelResponse(MemberLevelBase):
    id: int

    class Config:
        from_attributes = True
