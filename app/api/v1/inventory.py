from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.schemas.inventory import InventoryCreate, InventoryUpdate, InventoryResponse, InventoryRecordCreate, InventoryRecordResponse
from app.services.inventory_service import get_inventory_by_id, get_inventory, create_inventory, update_inventory, adjust_inventory, get_inventory_records, get_low_stock_products
from app.api.deps import get_current_active_user

router = APIRouter(prefix="/inventory", tags=["库存管理"])

@router.get("/", response_model=List[InventoryResponse])
def list_inventory(
    store_id: Optional[int] = None,
    product_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    inventory = get_inventory(db, store_id=store_id, product_id=product_id)
    return inventory

@router.get("/low-stock", response_model=List[InventoryResponse])
def get_low_stock(
    store_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    low_stock = get_low_stock_products(db, store_id=store_id)
    return low_stock

@router.post("/adjust")
def adjust_stock(
    store_id: int,
    product_id: int,
    quantity: float,
    record_type: str = "in",
    remark: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    inventory = adjust_inventory(
        db, store_id, product_id, quantity,
        record_type=record_type,
        operator_id=current_user.id,
        remark=remark
    )
    return {"message": "库存调整成功", "inventory_id": inventory.id}

@router.get("/records", response_model=List[InventoryRecordResponse])
def list_inventory_records(
    store_id: Optional[int] = None,
    product_id: Optional[int] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    records = get_inventory_records(db, store_id=store_id, product_id=product_id, skip=skip, limit=limit)
    return records

@router.post("/", response_model=InventoryResponse)
def create_new_inventory(inventory_data: InventoryCreate, db: Session = Depends(get_db), current_user = Depends(get_current_active_user)):
    inventory = create_inventory(db, inventory_data)
    return inventory

@router.put("/{inventory_id}", response_model=InventoryResponse)
def update_existing_inventory(inventory_id: int, inventory_data: InventoryUpdate, db: Session = Depends(get_db), current_user = Depends(get_current_active_user)):
    inventory = update_inventory(db, inventory_id, inventory_data)
    if not inventory:
        raise HTTPException(status_code=404, detail="库存记录不存在")
    return inventory
