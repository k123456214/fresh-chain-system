from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.schemas.supplier import SupplierCreate, SupplierUpdate, SupplierResponse, PurchaseOrderCreate, PurchaseOrderUpdate, PurchaseOrderResponse
from app.services.supplier_service import get_supplier_by_id, get_suppliers, create_supplier, update_supplier, delete_supplier, get_purchase_orders, create_purchase_order, update_purchase_order
from app.api.deps import get_current_active_user

router = APIRouter(prefix="/suppliers", tags=["供应商管理"])

@router.get("/", response_model=List[SupplierResponse])
def list_suppliers(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    keyword: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    suppliers = get_suppliers(db, skip=skip, limit=limit, keyword=keyword)
    return suppliers

@router.get("/{supplier_id}", response_model=SupplierResponse)
def get_supplier(supplier_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_active_user)):
    supplier = get_supplier_by_id(db, supplier_id)
    if not supplier:
        raise HTTPException(status_code=404, detail="供应商不存在")
    return supplier

@router.post("/", response_model=SupplierResponse)
def create_new_supplier(supplier_data: SupplierCreate, db: Session = Depends(get_db), current_user = Depends(get_current_active_user)):
    supplier = create_supplier(db, supplier_data)
    return supplier

@router.put("/{supplier_id}", response_model=SupplierResponse)
def update_existing_supplier(supplier_id: int, supplier_data: SupplierUpdate, db: Session = Depends(get_db), current_user = Depends(get_current_active_user)):
    supplier = update_supplier(db, supplier_id, supplier_data)
    if not supplier:
        raise HTTPException(status_code=404, detail="供应商不存在")
    return supplier

@router.delete("/{supplier_id}")
def delete_existing_supplier(supplier_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_active_user)):
    success = delete_supplier(db, supplier_id)
    if not success:
        raise HTTPException(status_code=404, detail="供应商不存在")
    return {"message": "供应商已删除"}

@router.get("/purchase-orders", response_model=List[PurchaseOrderResponse])
def list_purchase_orders(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    supplier_id: Optional[int] = None,
    store_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    orders = get_purchase_orders(db, skip=skip, limit=limit, supplier_id=supplier_id, store_id=store_id)
    return orders

@router.post("/purchase-orders", response_model=PurchaseOrderResponse)
def create_new_purchase_order(order_data: PurchaseOrderCreate, db: Session = Depends(get_db), current_user = Depends(get_current_active_user)):
    order = create_purchase_order(db, order_data)
    return order

@router.put("/purchase-orders/{order_id}", response_model=PurchaseOrderResponse)
def update_existing_purchase_order(order_id: int, order_data: PurchaseOrderUpdate, db: Session = Depends(get_db), current_user = Depends(get_current_active_user)):
    order = update_purchase_order(db, order_id, order_data)
    if not order:
        raise HTTPException(status_code=404, detail="采购订单不存在")
    return order
