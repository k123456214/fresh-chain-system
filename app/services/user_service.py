from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash, verify_password, create_access_token
from typing import Optional, List

def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    return db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()

def get_user_by_username(db: Session, username: str) -> Optional[User]:
    return db.execute(select(User).where(User.username == username)).scalar_one_or_none()

def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    return db.execute(select(User).offset(skip).limit(limit)).scalars().all()

def create_user(db: Session, user_data: UserCreate) -> User:
    hashed_password = get_password_hash(user_data.password)
    user = User(
        username=user_data.username,
        password=hashed_password,
        real_name=user_data.real_name,
        phone=user_data.phone,
        email=user_data.email,
        role=user_data.role,
        store_id=user_data.store_id
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def update_user(db: Session, user_id: int, user_data: UserUpdate) -> Optional[User]:
    user = get_user_by_id(db, user_id)
    if not user:
        return None
    update_data = user_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user

def delete_user(db: Session, user_id: int) -> bool:
    user = get_user_by_id(db, user_id)
    if not user:
        return False
    user.is_active = False
    db.commit()
    return True

def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    user = get_user_by_username(db, username)
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    if not user.is_active:
        return None
    return user

def login_user(db: Session, username: str, password: str) -> Optional[dict]:
    user = authenticate_user(db, username, password)
    if not user:
        return None
    token = create_access_token(data={
        "user_id": user.id,
        "username": user.username,
        "role": user.role
    })
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "username": user.username,
            "real_name": user.real_name,
            "role": user.role,
            "store_id": user.store_id
        }
    }
