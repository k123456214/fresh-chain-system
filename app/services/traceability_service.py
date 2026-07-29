from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.traceability import Traceability, TraceabilityStep
from app.schemas.traceability import TraceabilityCreate, TraceabilityUpdate, TraceabilityStepCreate
from typing import Optional, List

def get_traceability_by_id(db: Session, traceability_id: int) -> Optional[Traceability]:
    return db.execute(select(Traceability).where(Traceability.id == traceability_id)).scalar_one_or_none()

def get_traceabilities(db: Session, skip: int = 0, limit: int = 100, product_id: Optional[int] = None, batch_no: Optional[str] = None, status: Optional[str] = None) -> List[Traceability]:
    query = select(Traceability)
    if product_id:
        query = query.where(Traceability.product_id == product_id)
    if batch_no:
        query = query.where(Traceability.batch_no.contains(batch_no))
    if status:
        query = query.where(Traceability.status == status)
    return db.execute(query.offset(skip).limit(limit)).scalars().all()

def get_traceability_by_batch(db: Session, batch_no: str) -> Optional[Traceability]:
    return db.execute(select(Traceability).where(Traceability.batch_no == batch_no)).scalar_one_or_none()

def create_traceability(db: Session, traceability_data: TraceabilityCreate) -> Traceability:
    traceability = Traceability(**traceability_data.model_dump())
    db.add(traceability)
    db.commit()
    db.refresh(traceability)
    return traceability

def update_traceability(db: Session, traceability_id: int, traceability_data: TraceabilityUpdate) -> Optional[Traceability]:
    traceability = get_traceability_by_id(db, traceability_id)
    if not traceability:
        return None
    update_data = traceability_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(traceability, key, value)
    db.commit()
    db.refresh(traceability)
    return traceability

def delete_traceability(db: Session, traceability_id: int) -> bool:
    traceability = get_traceability_by_id(db, traceability_id)
    if not traceability:
        return False
    db.delete(traceability)
    db.commit()
    return True

def get_traceability_steps(db: Session, traceability_id: int) -> List[TraceabilityStep]:
    return db.execute(
        select(TraceabilityStep).where(
            TraceabilityStep.traceability_id == traceability_id
        ).order_by(TraceabilityStep.step_no)
    ).scalars().all()

def create_traceability_step(db: Session, step_data: TraceabilityStepCreate) -> TraceabilityStep:
    step = TraceabilityStep(**step_data.model_dump())
    db.add(step)
    db.commit()
    db.refresh(step)
    return step

def get_full_traceability_chain(db: Session, traceability_id: int) -> dict:
    traceability = get_traceability_by_id(db, traceability_id)
    if not traceability:
        return {}
    steps = get_traceability_steps(db, traceability_id)
    return {
        "traceability": traceability,
        "steps": steps
    }
