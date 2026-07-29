from sqlalchemy.orm import Session
from sqlalchemy import select, desc
from app.models.inventory import Inventory, InventoryRecord
from app.schemas.inventory import InventoryCreate, InventoryUpdate, InventoryRecordCreate
from datetime import datetime
from typing import Optional, List

def get_inventory_by_id(db: Session, inventory_id: int) -> Optional[Inventory]:
    return db.execute(select(Inventory).where(Inventory.id == inventory_id)).scalar_one_or_none()

def get_inventory(db: Session, store_id: Optional[int] = None, product_id: Optional[int] = None) -> List[Inventory]:
    query = select(Inventory)
    if store_id:
        query = query.where(Inventory.store_id == store_id)
    if product_id:
        query = query.where(Inventory.product_id == product_id)
    return db.execute(query).scalars().all()

def get_inventory_by_store_and_product(db: Session, store_id: int, product_id: int) -> Optional[Inventory]:
    return db.execute(
        select(Inventory).where(
            Inventory.store_id == store_id,
            Inventory.product_id == product_id
        )
    ).scalar_one_or_none()

def create_inventory(db: Session, inventory_data: InventoryCreate) -> Inventory:
    inventory = Inventory(**inventory_data.model_dump())
    db.add(inventory)
    db.commit()
    db.refresh(inventory)
    return inventory

def update_inventory(db: Session, inventory_id: int, inventory_data: InventoryUpdate) -> Optional[Inventory]:
    inventory = get_inventory_by_id(db, inventory_id)
    if not inventory:
        return None
    update_data = inventory_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(inventory, key, value)
    db.commit()
    db.refresh(inventory)
    return inventory

def adjust_inventory(db: Session, store_id: int, product_id: int, quantity: float, record_type: str, operator_id: Optional[int] = None, remark: Optional[str] = None) -> Inventory:
    inventory = get_inventory_by_store_and_product(db, store_id, product_id)
    if not inventory:
        inventory = Inventory(store_id=store_id, product_id=product_id, quantity=0)
        db.add(inventory)
        db.flush()
    
    before_quantity = inventory.quantity
    if record_type in ["in", "restock"]:
        inventory.quantity += quantity
    elif record_type in ["out", "sale", "loss"]:
        inventory.quantity -= quantity
    elif record_type == "set":
        inventory.quantity = quantity
    
    after_quantity = inventory.quantity
    
    record = InventoryRecord(
        store_id=store_id,
        product_id=product_id,
        type=record_type,
        quantity=quantity,
        before_quantity=before_quantity,
        after_quantity=after_quantity,
        remark=remark,
        operator_id=operator_id
    )
    db.add(record)
    db.commit()
    db.refresh(inventory)
    return inventory

def get_inventory_records(db: Session, store_id: Optional[int] = None, product_id: Optional[int] = None, skip: int = 0, limit: int = 100) -> List[InventoryRecord]:
    query = select(InventoryRecord).order_by(desc(InventoryRecord.created_at))
    if store_id:
        query = query.where(InventoryRecord.store_id == store_id)
    if product_id:
        query = query.where(InventoryRecord.product_id == product_id)
    return db.execute(query.offset(skip).limit(limit)).scalars().all()

def get_low_stock_products(db: Session, store_id: Optional[int] = None) -> List[Inventory]:
    query = select(Inventory).where(Inventory.quantity <= Inventory.warning_quantity)
    if store_id:
        query = query.where(Inventory.store_id == store_id)
    return db.execute(query).scalars().all()
