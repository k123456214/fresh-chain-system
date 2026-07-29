from sqlalchemy.orm import Session
from sqlalchemy import select, or_
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate
from typing import Optional, List

def get_product_by_id(db: Session, product_id: int) -> Optional[Product]:
    return db.execute(select(Product).where(Product.id == product_id)).scalar_one_or_none()

def get_product_by_code(db: Session, code: str) -> Optional[Product]:
    return db.execute(select(Product).where(Product.code == code)).scalar_one_or_none()

def get_products(db: Session, skip: int = 0, limit: int = 100, keyword: Optional[str] = None, category: Optional[str] = None) -> List[Product]:
    query = select(Product)
    if keyword:
        query = query.where(or_(Product.name.contains(keyword), Product.code.contains(keyword), Product.barcode.contains(keyword)))
    if category:
        query = query.where(Product.category == category)
    return db.execute(query.offset(skip).limit(limit)).scalars().all()

def get_product_categories(db: Session) -> List[str]:
    result = db.execute(select(Product.category).distinct().where(Product.category.isnot(None)))
    return [row[0] for row in result if row[0]]

def create_product(db: Session, product_data: ProductCreate) -> Product:
    product = Product(**product_data.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

def update_product(db: Session, product_id: int, product_data: ProductUpdate) -> Optional[Product]:
    product = get_product_by_id(db, product_id)
    if not product:
        return None
    update_data = product_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(product, key, value)
    db.commit()
    db.refresh(product)
    return product

def delete_product(db: Session, product_id: int) -> bool:
    product = get_product_by_id(db, product_id)
    if not product:
        return False
    product.status = False
    db.commit()
    return True
