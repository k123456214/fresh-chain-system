from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.schemas.traceability import TraceabilityCreate, TraceabilityUpdate, TraceabilityResponse, TraceabilityStepCreate, TraceabilityStepResponse
from app.services.traceability_service import get_traceability_by_id, get_traceabilities, create_traceability, update_traceability, delete_traceability, get_traceability_steps, create_traceability_step, get_full_traceability_chain
from app.api.deps import get_current_active_user

router = APIRouter(prefix="/traceability", tags=["溯源管理"])

@router.get("/", response_model=List[TraceabilityResponse])
def list_traceabilities(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    product_id: Optional[int] = None,
    batch_no: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    traceabilities = get_traceabilities(db, skip=skip, limit=limit, product_id=product_id, batch_no=batch_no, status=status)
    return traceabilities

@router.get("/{traceability_id}", response_model=TraceabilityResponse)
def get_traceability(traceability_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_active_user)):
    traceability = get_traceability_by_id(db, traceability_id)
    if not traceability:
        raise HTTPException(status_code=404, detail="溯源记录不存在")
    return traceability

@router.get("/{traceability_id}/chain")
def get_traceability_chain(traceability_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_active_user)):
    chain = get_full_traceability_chain(db, traceability_id)
    if not chain:
        raise HTTPException(status_code=404, detail="溯源记录不存在")
    return chain

@router.post("/", response_model=TraceabilityResponse)
def create_new_traceability(traceability_data: TraceabilityCreate, db: Session = Depends(get_db), current_user = Depends(get_current_active_user)):
    traceability = create_traceability(db, traceability_data)
    return traceability

@router.put("/{traceability_id}", response_model=TraceabilityResponse)
def update_existing_traceability(traceability_id: int, traceability_data: TraceabilityUpdate, db: Session = Depends(get_db), current_user = Depends(get_current_active_user)):
    traceability = update_traceability(db, traceability_id, traceability_data)
    if not traceability:
        raise HTTPException(status_code=404, detail="溯源记录不存在")
    return traceability

@router.delete("/{traceability_id}")
def delete_existing_traceability(traceability_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_active_user)):
    success = delete_traceability(db, traceability_id)
    if not success:
        raise HTTPException(status_code=404, detail="溯源记录不存在")
    return {"message": "溯源记录已删除"}

@router.get("/{traceability_id}/steps", response_model=List[TraceabilityStepResponse])
def list_traceability_steps(traceability_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_active_user)):
    steps = get_traceability_steps(db, traceability_id)
    return steps

@router.post("/steps", response_model=TraceabilityStepResponse)
def create_new_traceability_step(step_data: TraceabilityStepCreate, db: Session = Depends(get_db), current_user = Depends(get_current_active_user)):
    step = create_traceability_step(db, step_data)
    return step
