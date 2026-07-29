from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.core.database import get_db
from app.schemas.order import OrderCreate, OrderUpdate, OrderResponse, OrderItemResponse
from app.services.order_service import get_order_by_id, get_order_by_order_no, get_orders, create_order, update_order, get_order_items, get_daily_sales
from app.api.deps import get_current_active_user, get_current_user
from app.models.user import User

router = APIRouter(prefix="/orders", tags=["订单管理"])

@router.get("/", response_model=List[OrderResponse])
def list_orders(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    store_id: Optional[int] = None,
    status: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    start = datetime.fromisoformat(start_date) if start_date else None
    end = datetime.fromisoformat(end_date) if end_date else None
    orders = get_orders(db, skip=skip, limit=limit, store_id=store_id, status=status, start_date=start, end_date=end)
    return orders

@router.get("/stats/daily")
def get_daily_stats(
    store_id: Optional[int] = None,
    date: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    target_date = datetime.fromisoformat(date) if date else datetime.now()
    stats = get_daily_sales(db, store_id=store_id, date=target_date)
    return stats

@router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    order = get_order_by_id(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="订单不存在")
    return order

@router.get("/{order_id}/items", response_model=List[OrderItemResponse])
def get_order_item_list(order_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    order = get_order_by_id(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="订单不存在")
    items = get_order_items(db, order_id)
    return items

@router.post("/", response_model=OrderResponse)
def create_new_order(
    order_data: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    order = create_order(db, order_data, cashier_id=current_user.id)
    return order

@router.put("/{order_id}", response_model=OrderResponse)
def update_existing_order(order_id: int, order_data: OrderUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    order = update_order(db, order_id, order_data)
    if not order:
        raise HTTPException(status_code=404, detail="订单不存在")
    return order
