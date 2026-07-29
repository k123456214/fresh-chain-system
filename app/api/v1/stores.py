from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.schemas.store import StoreCreate, StoreUpdate, StoreResponse
from app.services.store_service import get_store_by_id, get_store_by_code, get_stores, create_store, update_store, delete_store
from app.api.deps import get_current_active_user

router = APIRouter(prefix="/stores", tags=["门店管理"])

@router.get("/", response_model=List[StoreResponse])
def list_stores(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    stores = get_stores(db, skip=skip, limit=limit)
    return stores

@router.get("/{store_id}", response_model=StoreResponse)
def get_store(store_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_active_user)):
    store = get_store_by_id(db, store_id)
    if not store:
        raise HTTPException(status_code=404, detail="门店不存在")
    return store

@router.post("/", response_model=StoreResponse)
def create_new_store(store_data: StoreCreate, db: Session = Depends(get_db), current_user = Depends(get_current_active_user)):
    existing = get_store_by_code(db, store_data.code)
    if existing:
        raise HTTPException(status_code=400, detail="门店编号已存在")
    store = create_store(db, store_data)
    return store

@router.put("/{store_id}", response_model=StoreResponse)
def update_existing_store(store_id: int, store_data: StoreUpdate, db: Session = Depends(get_db), current_user = Depends(get_current_active_user)):
    store = update_store(db, store_id, store_data)
    if not store:
        raise HTTPException(status_code=404, detail="门店不存在")
    return store

@router.delete("/{store_id}")
def delete_existing_store(store_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_active_user)):
    success = delete_store(db, store_id)
    if not success:
        raise HTTPException(status_code=404, detail="门店不存在")
    return {"message": "门店已删除"}
