from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.schemas.loss import LossRecordCreate, LossRecordUpdate, LossRecordResponse
from app.services.loss_service import get_loss_record_by_id, get_loss_records, create_loss_record, update_loss_record, delete_loss_record, get_loss_statistics
from app.api.deps import get_current_active_user

router = APIRouter(prefix="/loss", tags=["损耗管理"])

@router.get("/", response_model=List[LossRecordResponse])
def list_loss_records(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    store_id: Optional[int] = None,
    product_id: Optional[int] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    records = get_loss_records(db, skip=skip, limit=limit, store_id=store_id, product_id=product_id, start_date=start_date, end_date=end_date)
    return records

@router.get("/stats")
def get_loss_stats(
    store_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    stats = get_loss_statistics(db, store_id=store_id)
    return stats

@router.get("/{record_id}", response_model=LossRecordResponse)
def get_loss_record(record_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_active_user)):
    record = get_loss_record_by_id(db, record_id)
    if not record:
        raise HTTPException(status_code=404, detail="损耗记录不存在")
    return record

@router.post("/", response_model=LossRecordResponse)
def create_new_loss_record(record_data: LossRecordCreate, db: Session = Depends(get_db), current_user = Depends(get_current_active_user)):
    record = create_loss_record(db, record_data)
    return record

@router.put("/{record_id}", response_model=LossRecordResponse)
def update_existing_loss_record(record_id: int, record_data: LossRecordUpdate, db: Session = Depends(get_db), current_user = Depends(get_current_active_user)):
    record = update_loss_record(db, record_id, record_data)
    if not record:
        raise HTTPException(status_code=404, detail="损耗记录不存在")
    return record

@router.delete("/{record_id}")
def delete_existing_loss_record(record_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_active_user)):
    success = delete_loss_record(db, record_id)
    if not success:
        raise HTTPException(status_code=404, detail="损耗记录不存在")
    return {"message": "损耗记录已删除"}
