from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.schemas.member import MemberCreate, MemberUpdate, MemberResponse, MemberLevelCreate, MemberLevelResponse
from app.services.member_service import get_member_by_id, get_member_by_phone, get_members, create_member, update_member, add_member_points, add_member_balance, get_member_levels, create_member_level, calculate_member_discount
from app.api.deps import get_current_active_user

router = APIRouter(prefix="/members", tags=["会员管理"])

@router.get("/", response_model=List[MemberResponse])
def list_members(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    keyword: Optional[str] = None,
    level: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    members = get_members(db, skip=skip, limit=limit, keyword=keyword, level=level)
    return members

@router.get("/{member_id}", response_model=MemberResponse)
def get_member(member_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_active_user)):
    member = get_member_by_id(db, member_id)
    if not member:
        raise HTTPException(status_code=404, detail="会员不存在")
    return member

@router.get("/phone/{phone}", response_model=MemberResponse)
def get_member_by_phone_number(phone: str, db: Session = Depends(get_db), current_user = Depends(get_current_active_user)):
    member = get_member_by_phone(db, phone)
    if not member:
        raise HTTPException(status_code=404, detail="会员不存在")
    return member

@router.post("/", response_model=MemberResponse)
def create_new_member(member_data: MemberCreate, db: Session = Depends(get_db), current_user = Depends(get_current_active_user)):
    existing = get_member_by_phone(db, member_data.phone)
    if existing:
        raise HTTPException(status_code=400, detail="手机号已注册")
    member = create_member(db, member_data)
    return member

@router.put("/{member_id}", response_model=MemberResponse)
def update_existing_member(member_id: int, member_data: MemberUpdate, db: Session = Depends(get_db), current_user = Depends(get_current_active_user)):
    member = update_member(db, member_id, member_data)
    if not member:
        raise HTTPException(status_code=404, detail="会员不存在")
    return member

@router.post("/{member_id}/points")
def add_points(member_id: int, points: int = 0, db: Session = Depends(get_db), current_user = Depends(get_current_active_user)):
    member = add_member_points(db, member_id, points)
    if not member:
        raise HTTPException(status_code=404, detail="会员不存在")
    return {"message": "积分已添加", "current_points": member.points}

@router.post("/{member_id}/balance")
def add_balance(member_id: int, amount: float = 0, db: Session = Depends(get_db), current_user = Depends(get_current_active_user)):
    member = add_member_balance(db, member_id, amount)
    if not member:
        raise HTTPException(status_code=404, detail="会员不存在")
    return {"message": "余额已更新", "current_balance": member.balance}

@router.get("/{member_id}/discount")
def get_discount(member_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_active_user)):
    discount = calculate_member_discount(db, member_id)
    return {"discount_rate": discount}

@router.get("/levels", response_model=List[MemberLevelResponse])
def list_levels(db: Session = Depends(get_db), current_user = Depends(get_current_active_user)):
    levels = get_member_levels(db)
    return levels

@router.post("/levels", response_model=MemberLevelResponse)
def create_new_level(level_data: MemberLevelCreate, db: Session = Depends(get_db), current_user = Depends(get_current_active_user)):
    level = create_member_level(db, level_data)
    return level
