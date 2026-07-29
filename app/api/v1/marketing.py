from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.schemas.marketing import PromotionCreate, PromotionUpdate, PromotionResponse, CouponCreate, CouponUpdate, CouponResponse, MemberCouponResponse
from app.services.marketing_service import get_promotion_by_id, get_promotions, create_promotion, update_promotion, get_active_promotions, get_coupons, create_coupon, update_coupon, issue_coupon_to_member, get_member_coupons, use_member_coupon
from app.api.deps import get_current_active_user

router = APIRouter(prefix="/marketing", tags=["营销管理"])

@router.get("/promotions", response_model=List[PromotionResponse])
def list_promotions(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    status: Optional[bool] = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    promotions = get_promotions(db, skip=skip, limit=limit, status=status)
    return promotions

@router.get("/promotions/active", response_model=List[PromotionResponse])
def list_active_promotions(db: Session = Depends(get_db), current_user = Depends(get_current_active_user)):
    promotions = get_active_promotions(db)
    return promotions

@router.post("/promotions", response_model=PromotionResponse)
def create_new_promotion(promotion_data: PromotionCreate, db: Session = Depends(get_db), current_user = Depends(get_current_active_user)):
    promotion = create_promotion(db, promotion_data)
    return promotion

@router.put("/promotions/{promotion_id}", response_model=PromotionResponse)
def update_existing_promotion(promotion_id: int, promotion_data: PromotionUpdate, db: Session = Depends(get_db), current_user = Depends(get_current_active_user)):
    promotion = update_promotion(db, promotion_id, promotion_data)
    if not promotion:
        raise HTTPException(status_code=404, detail="促销活动不存在")
    return promotion

@router.get("/coupons", response_model=List[CouponResponse])
def list_coupons(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    status: Optional[bool] = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    coupons = get_coupons(db, skip=skip, limit=limit, status=status)
    return coupons

@router.post("/coupons", response_model=CouponResponse)
def create_new_coupon(coupon_data: CouponCreate, db: Session = Depends(get_db), current_user = Depends(get_current_active_user)):
    coupon = create_coupon(db, coupon_data)
    return coupon

@router.put("/coupons/{coupon_id}", response_model=CouponResponse)
def update_existing_coupon(coupon_id: int, coupon_data: CouponUpdate, db: Session = Depends(get_db), current_user = Depends(get_current_active_user)):
    coupon = update_coupon(db, coupon_id, coupon_data)
    if not coupon:
        raise HTTPException(status_code=404, detail="优惠券不存在")
    return coupon

@router.post("/coupons/{coupon_id}/issue/{member_id}", response_model=MemberCouponResponse)
def issue_coupon(coupon_id: int, member_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_active_user)):
    member_coupon = issue_coupon_to_member(db, coupon_id, member_id)
    if not member_coupon:
        raise HTTPException(status_code=400, detail="发放失败")
    return member_coupon

@router.get("/members/{member_id}/coupons", response_model=List[MemberCouponResponse])
def list_member_coupons(member_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_active_user)):
    coupons = get_member_coupons(db, member_id)
    return coupons

@router.post("/member-coupons/{coupon_id}/use")
def use_coupon(coupon_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_active_user)):
    success = use_member_coupon(db, coupon_id)
    if not success:
        raise HTTPException(status_code=400, detail="使用失败")
    return {"message": "优惠券已使用"}
