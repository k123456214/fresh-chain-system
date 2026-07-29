from sqlalchemy.orm import Session
from sqlalchemy import select, desc
from app.models.supplier import Supplier, PurchaseOrder
from app.schemas.supplier import SupplierCreate, SupplierUpdate, PurchaseOrderCreate, PurchaseOrderUpdate
from datetime import datetime
from typing import Optional, List

def get_supplier_by_id(db: Session, supplier_id: int) -> Optional[Supplier]:
    return db.execute(select(Supplier).where(Supplier.id == supplier_id)).scalar_one_or_none()

def get_suppliers(db: Session, skip: int = 0, limit: int = 100, keyword: Optional[str] = None) -> List[Supplier]:
    query = select(Supplier)
    if keyword:
        query = query.where((Supplier.name.contains(keyword)) | (Supplier.contact_person.contains(keyword)))
    return db.execute(query.offset(skip).limit(limit)).scalars().all()

def create_supplier(db: Session, supplier_data: SupplierCreate) -> Supplier:
    supplier = Supplier(
        **supplier_data.model_dump(),
        cooperation_start=datetime.now()
    )
    db.add(supplier)
    db.commit()
    db.refresh(supplier)
    return supplier

def update_supplier(db: Session, supplier_id: int, supplier_data: SupplierUpdate) -> Optional[Supplier]:
    supplier = get_supplier_by_id(db, supplier_id)
    if not supplier:
        return None
    update_data = supplier_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(supplier, key, value)
    db.commit()
    db.refresh(supplier)
    return supplier

def delete_supplier(db: Session, supplier_id: int) -> bool:
    supplier = get_supplier_by_id(db, supplier_id)
    if not supplier:
        return False
    supplier.status = False
    db.commit()
    return True

def get_purchase_orders(db: Session, skip: int = 0, limit: int = 100, supplier_id: Optional[int] = None, store_id: Optional[int] = None) -> List[PurchaseOrder]:
    query = select(PurchaseOrder).order_by(desc(PurchaseOrder.created_at))
    if supplier_id:
        query = query.where(PurchaseOrder.supplier_id == supplier_id)
    if store_id:
        query = query.where(PurchaseOrder.store_id == store_id)
    return db.execute(query.offset(skip).limit(limit)).scalars().all()

def generate_purchase_order_no() -> str:
    now = datetime.now()
    return f"PO{now.strftime('%Y%m%d%H%M%S%f')[:14]}"

def create_purchase_order(db: Session, order_data: PurchaseOrderCreate) -> PurchaseOrder:
    order_no = generate_purchase_order_no()
    order = PurchaseOrder(
        order_no=order_no,
        supplier_id=order_data.supplier_id,
        store_id=order_data.store_id,
        total_amount=order_data.total_amount,
        remark=order_data.remark,
        items=order_data.items
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    return order

def update_purchase_order(db: Session, order_id: int, order_data: PurchaseOrderUpdate) -> Optional[PurchaseOrder]:
    order = db.execute(select(PurchaseOrder).where(PurchaseOrder.id == order_id)).scalar_one_or_none()
    if not order:
        return None
    update_data = order_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(order, key, value)
    db.commit()
    db.refresh(order)
    return order
