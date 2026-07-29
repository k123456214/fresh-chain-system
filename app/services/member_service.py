from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.member import Member, MemberLevel
from app.schemas.member import MemberCreate, MemberUpdate, MemberLevelCreate
from datetime import datetime
from typing import Optional, List

def get_member_by_id(db: Session, member_id: int) -> Optional[Member]:
    return db.execute(select(Member).where(Member.id == member_id)).scalar_one_or_none()

def get_member_by_phone(db: Session, phone: str) -> Optional[Member]:
    return db.execute(select(Member).where(Member.phone == phone)).scalar_one_or_none()

def get_member_by_member_no(db: Session, member_no: str) -> Optional[Member]:
    return db.execute(select(Member).where(Member.member_no == member_no)).scalar_one_or_none()

def get_members(db: Session, skip: int = 0, limit: int = 100, keyword: Optional[str] = None, level: Optional[str] = None) -> List[Member]:
    query = select(Member)
    if keyword:
        query = query.where((Member.name.contains(keyword)) | (Member.phone.contains(keyword)) | (Member.member_no.contains(keyword)))
    if level:
        query = query.where(Member.level == level)
    return db.execute(query.offset(skip).limit(limit)).scalars().all()

def generate_member_no() -> str:
    now = datetime.now()
    return f"M{now.strftime('%Y%m%d%H%M%S%f')[:12]}"

def create_member(db: Session, member_data: MemberCreate) -> Member:
    member_no = generate_member_no()
    member = Member(
        member_no=member_no,
        name=member_data.name,
        phone=member_data.phone,
        level=member_data.level,
        store_id=member_data.store_id
    )
    db.add(member)
    db.commit()
    db.refresh(member)
    return member

def update_member(db: Session, member_id: int, member_data: MemberUpdate) -> Optional[Member]:
    member = get_member_by_id(db, member_id)
    if not member:
        return None
    update_data = member_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(member, key, value)
    db.commit()
    db.refresh(member)
    return member

def add_member_points(db: Session, member_id: int, points: int) -> Optional[Member]:
    member = get_member_by_id(db, member_id)
    if not member:
        return None
    member.points += points
    db.commit()
    db.refresh(member)
    return member

def add_member_balance(db: Session, member_id: int, amount: float) -> Optional[Member]:
    member = get_member_by_id(db, member_id)
    if not member:
        return None
    member.balance += amount
    db.commit()
    db.refresh(member)
    return member

def get_member_levels(db: Session) -> List[MemberLevel]:
    return db.execute(select(MemberLevel)).scalars().all()

def create_member_level(db: Session, level_data: MemberLevelCreate) -> MemberLevel:
    level = MemberLevel(**level_data.model_dump())
    db.add(level)
    db.commit()
    db.refresh(level)
    return level

def calculate_member_discount(db: Session, member_id: int) -> float:
    member = get_member_by_id(db, member_id)
    if not member:
        return 1.0
    level = db.execute(select(MemberLevel).where(MemberLevel.name == member.level)).scalar_one_or_none()
    if level:
        return level.discount_rate
    return 1.0
