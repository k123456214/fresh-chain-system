from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse
from app.services.product_service import get_product_by_id, get_product_by_code, get_products, create_product, update_product, delete_product, get_product_categories
from app.api.deps import get_current_active_user

router = APIRouter(prefix="/products", tags=["商品管理"])

@router.get("/", response_model=List[ProductResponse])
def list_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    keyword: Optional[str] = None,
    category: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    products = get_products(db, skip=skip, limit=limit, keyword=keyword, category=category)
    return products

@router.get("/categories", response_model=List[str])
def list_categories(db: Session = Depends(get_db), current_user = Depends(get_current_active_user)):
    categories = get_product_categories(db)
    return categories

@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_active_user)):
    product = get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="商品不存在")
    return product

@router.post("/", response_model=ProductResponse)
def create_new_product(product_data: ProductCreate, db: Session = Depends(get_db), current_user = Depends(get_current_active_user)):
    existing = get_product_by_code(db, product_data.code)
    if existing:
        raise HTTPException(status_code=400, detail="商品编号已存在")
    product = create_product(db, product_data)
    return product

@router.put("/{product_id}", response_model=ProductResponse)
def update_existing_product(product_id: int, product_data: ProductUpdate, db: Session = Depends(get_db), current_user = Depends(get_current_active_user)):
    product = update_product(db, product_id, product_data)
    if not product:
        raise HTTPException(status_code=404, detail="商品不存在")
    return product

@router.delete("/{product_id}")
def delete_existing_product(product_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_active_user)):
    success = delete_product(db, product_id)
    if not success:
        raise HTTPException(status_code=404, detail="商品不存在")
    return {"message": "商品已删除"}
