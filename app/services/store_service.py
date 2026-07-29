from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.store import Store
from app.schemas.store import StoreCreate, StoreUpdate
from typing import Optional, List

def get_store_by_id(db: Session, store_id: int) -> Optional[Store]:
    return db.execute(select(Store).where(Store.id == store_id)).scalar_one_or_none()

def get_store_by_code(db: Session, code: str) -> Optional[Store]:
    return db.execute(select(Store).where(Store.code == code)).scalar_one_or_none()

def get_stores(db: Session, skip: int = 0, limit: int = 100) -> List[Store]:
    return db.execute(select(Store).offset(skip).limit(limit)).scalars().all()

def create_store(db: Session, store_data: StoreCreate) -> Store:
    store = Store(**store_data.model_dump())
    db.add(store)
    db.commit()
    db.refresh(store)
    return store

def update_store(db: Session, store_id: int, store_data: StoreUpdate) -> Optional[Store]:
    store = get_store_by_id(db, store_id)
    if not store:
        return None
    update_data = store_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(store, key, value)
    db.commit()
    db.refresh(store)
    return store

def delete_store(db: Session, store_id: int) -> bool:
    store = get_store_by_id(db, store_id)
    if not store:
        return False
    store.status = False
    db.commit()
    return True
