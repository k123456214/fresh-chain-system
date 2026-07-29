from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class PromotionBase(BaseModel):
    name: str
    type: str = "discount"
    discount_rate: float = 1.0
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    scope: str = "all"
    product_ids: Optional[str] = None

class PromotionCreate(PromotionBase):
    pass

class PromotionUpdate(BaseModel):
    name: Optional[str] = None
    discount_rate: Optional[float] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    status: Optional[bool] = None

class PromotionResponse(PromotionBase):
    id: int
    status: bool
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class CouponBase(BaseModel):
    name: str
    type: str = "cash"
    value: float = 0
    min_amount: float = 0
    total_count: int = 0
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

class CouponCreate(CouponBase):
    pass

class CouponUpdate(BaseModel):
    name: Optional[str] = None
    value: Optional[float] = None
    min_amount: Optional[float] = None
    total_count: Optional[int] = None
    status: Optional[bool] = None

class CouponResponse(CouponBase):
    id: int
    used_count: int
    status: bool
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class MemberCouponResponse(BaseModel):
    id: int
    member_id: int
    coupon_id: int
    status: str
    used_at: Optional[datetime] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
