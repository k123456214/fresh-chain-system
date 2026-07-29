from sqlalchemy.orm import Session
from sqlalchemy import select, desc
from app.models.order import Order, OrderItem
from app.models.product import Product
from app.schemas.order import OrderCreate, OrderUpdate
from datetime import datetime
from typing import Optional, List
import json

def get_order_by_id(db: Session, order_id: int) -> Optional[Order]:
    return db.execute(select(Order).where(Order.id == order_id)).scalar_one_or_none()

def get_order_by_order_no(db: Session, order_no: str) -> Optional[Order]:
    return db.execute(select(Order).where(Order.order_no == order_no)).scalar_one_or_none()

def get_orders(db: Session, skip: int = 0, limit: int = 100, store_id: Optional[int] = None, status: Optional[str] = None, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> List[Order]:
    query = select(Order).order_by(desc(Order.created_at))
    if store_id:
        query = query.where(Order.store_id == store_id)
    if status:
        query = query.where(Order.status == status)
    if start_date:
        query = query.where(Order.created_at >= start_date)
    if end_date:
        query = query.where(Order.created_at <= end_date)
    return db.execute(query.offset(skip).limit(limit)).scalars().all()

def generate_order_no() -> str:
    now = datetime.now()
    return f"ORD{now.strftime('%Y%m%d%H%M%S%f')[:14]}"

def create_order(db: Session, order_data: OrderCreate, cashier_id: Optional[int] = None) -> Order:
    order_no = generate_order_no()
    items_data = order_data.items
    total_amount = sum(item.unit_price * item.quantity for item in items_data)
    
    order = Order(
        order_no=order_no,
        store_id=order_data.store_id,
        cashier_id=cashier_id,
        member_id=order_data.member_id,
        total_amount=total_amount,
        discount_amount=0,
        final_amount=total_amount,
        pay_method=order_data.pay_method,
        status="completed",
        remark=order_data.remark,
        items=json.dumps([item.model_dump() for item in items_data])
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    
    for item_data in items_data:
        order_item = OrderItem(
            order_id=order.id,
            product_id=item_data.product_id,
            product_name=item_data.product_name,
            quantity=item_data.quantity,
            unit_price=item_data.unit_price,
            subtotal=item_data.unit_price * item_data.quantity,
            weight=item_data.weight
        )
        db.add(order_item)
    
    for item_data in items_data:
        product = db.execute(select(Product).where(Product.id == item_data.product_id)).scalar_one_or_none()
        if product:
            product.stock -= item_data.quantity
    
    db.commit()
    return order

def update_order(db: Session, order_id: int, order_data: OrderUpdate) -> Optional[Order]:
    order = get_order_by_id(db, order_id)
    if not order:
        return None
    update_data = order_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(order, key, value)
    db.commit()
    db.refresh(order)
    return order

def get_order_items(db: Session, order_id: int) -> List[OrderItem]:
    return db.execute(select(OrderItem).where(OrderItem.order_id == order_id)).scalars().all()

def get_daily_sales(db: Session, store_id: Optional[int] = None, date: Optional[datetime] = None) -> dict:
    query = select(Order)
    if store_id:
        query = query.where(Order.store_id == store_id)
    if date:
        query = query.where(Order.created_at >= date.replace(hour=0, minute=0, second=0))
        query = query.where(Order.created_at < date.replace(hour=23, minute=59, second=59))
    
    orders = db.execute(query).scalars().all()
    total_amount = sum(order.final_amount for order in orders if order.status == "completed")
    return {
        "order_count": len(orders),
        "total_amount": total_amount
    }
