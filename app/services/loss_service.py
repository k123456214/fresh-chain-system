from sqlalchemy.orm import Session
from sqlalchemy import select, desc
from app.models.loss import LossRecord
from app.schemas.loss import LossRecordCreate, LossRecordUpdate
from typing import Optional, List

def get_loss_record_by_id(db: Session, record_id: int) -> Optional[LossRecord]:
    return db.execute(select(LossRecord).where(LossRecord.id == record_id)).scalar_one_or_none()

def get_loss_records(db: Session, skip: int = 0, limit: int = 100, store_id: Optional[int] = None, product_id: Optional[int] = None, start_date: Optional[str] = None, end_date: Optional[str] = None) -> List[LossRecord]:
    query = select(LossRecord).order_by(desc(LossRecord.created_at))
    if store_id:
        query = query.where(LossRecord.store_id == store_id)
    if product_id:
        query = query.where(LossRecord.product_id == product_id)
    if start_date:
        query = query.where(LossRecord.created_at >= start_date)
    if end_date:
        query = query.where(LossRecord.created_at <= end_date)
    return db.execute(query.offset(skip).limit(limit)).scalars().all()

def create_loss_record(db: Session, record_data: LossRecordCreate) -> LossRecord:
    record = LossRecord(**record_data.model_dump())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

def update_loss_record(db: Session, record_id: int, record_data: LossRecordUpdate) -> Optional[LossRecord]:
    record = get_loss_record_by_id(db, record_id)
    if not record:
        return None
    update_data = record_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(record, key, value)
    db.commit()
    db.refresh(record)
    return record

def delete_loss_record(db: Session, record_id: int) -> bool:
    record = get_loss_record_by_id(db, record_id)
    if not record:
        return False
    db.delete(record)
    db.commit()
    return True

def get_loss_statistics(db: Session, store_id: Optional[int] = None) -> dict:
    query = select(LossRecord)
    if store_id:
        query = query.where(LossRecord.store_id == store_id)
    records = db.execute(query).scalars().all()
    
    total_quantity = sum(r.quantity for r in records)
    total_amount = sum(r.amount for r in records)
    
    reason_stats = {}
    for record in records:
        reason = record.reason or "unknown"
        if reason not in reason_stats:
            reason_stats[reason] = {"count": 0, "quantity": 0, "amount": 0}
        reason_stats[reason]["count"] += 1
        reason_stats[reason]["quantity"] += record.quantity
        reason_stats[reason]["amount"] += record.amount
    
    return {
        "total_records": len(records),
        "total_quantity": total_quantity,
        "total_amount": total_amount,
        "reason_stats": reason_stats
    }
