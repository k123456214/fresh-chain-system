from sqlalchemy.orm import Session
from sqlalchemy import select, desc
from app.models.marketing import Promotion, Coupon, MemberCoupon
from app.models.member import Member
from app.schemas.marketing import PromotionCreate, PromotionUpdate, CouponCreate, CouponUpdate
from datetime import datetime
from typing import Optional, List

def get_promotion_by_id(db: Session, promotion_id: int) -> Optional[Promotion]:
    return db.execute(select(Promotion).where(Promotion.id == promotion_id)).scalar_one_or_none()

def get_promotions(db: Session, skip: int = 0, limit: int = 100, status: Optional[bool] = None) -> List[Promotion]:
    query = select(Promotion).order_by(desc(Promotion.created_at))
    if status is not None:
        query = query.where(Promotion.status == status)
    return db.execute(query.offset(skip).limit(limit)).scalars().all()

def create_promotion(db: Session, promotion_data: PromotionCreate) -> Promotion:
    promotion = Promotion(**promotion_data.model_dump())
    db.add(promotion)
    db.commit()
    db.refresh(promotion)
    return promotion

def update_promotion(db: Session, promotion_id: int, promotion_data: PromotionUpdate) -> Optional[Promotion]:
    promotion = get_promotion_by_id(db, promotion_id)
    if not promotion:
        return None
    update_data = promotion_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(promotion, key, value)
    db.commit()
    db.refresh(promotion)
    return promotion

def get_active_promotions(db: Session) -> List[Promotion]:
    now = datetime.now()
    return db.execute(
        select(Promotion).where(
            Promotion.status == True,
            Promotion.start_date <= now,
            Promotion.end_date >= now
        )
    ).scalars().all()

def get_coupons(db: Session, skip: int = 0, limit: int = 100, status: Optional[bool] = None) -> List[Coupon]:
    query = select(Coupon).order_by(desc(Coupon.created_at))
    if status is not None:
        query = query.where(Coupon.status == status)
    return db.execute(query.offset(skip).limit(limit)).scalars().all()

def create_coupon(db: Session, coupon_data: CouponCreate) -> Coupon:
    coupon = Coupon(**coupon_data.model_dump())
    db.add(coupon)
    db.commit()
    db.refresh(coupon)
    return coupon

def update_coupon(db: Session, coupon_id: int, coupon_data: CouponUpdate) -> Optional[Coupon]:
    coupon = db.execute(select(Coupon).where(Coupon.id == coupon_id)).scalar_one_or_none()
    if not coupon:
        return None
    update_data = coupon_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(coupon, key, value)
    db.commit()
    db.refresh(coupon)
    return coupon

def issue_coupon_to_member(db: Session, coupon_id: int, member_id: int) -> Optional[MemberCoupon]:
    coupon = db.execute(select(Coupon).where(Coupon.id == coupon_id)).scalar_one_or_none()
    member = db.execute(select(Member).where(Member.id == member_id)).scalar_one_or_none()
    if not coupon or not member:
        return None
    if coupon.used_count >= coupon.total_count:
        return None
    
    member_coupon = MemberCoupon(
        member_id=member_id,
        coupon_id=coupon_id
    )
    coupon.used_count += 1
    db.add(member_coupon)
    db.commit()
    db.refresh(member_coupon)
    return member_coupon

def get_member_coupons(db: Session, member_id: int) -> List[MemberCoupon]:
    return db.execute(select(MemberCoupon).where(MemberCoupon.member_id == member_id)).scalars().all()

def use_member_coupon(db: Session, member_coupon_id: int) -> bool:
    member_coupon = db.execute(select(MemberCoupon).where(MemberCoupon.id == member_coupon_id)).scalar_one_or_none()
    if not member_coupon or member_coupon.status != "unused":
        return False
    member_coupon.status = "used"
    member_coupon.used_at = datetime.now()
    db.commit()
    return True
