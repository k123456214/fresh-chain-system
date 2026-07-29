from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.services.user_service import get_user_by_id, get_users, create_user, update_user, delete_user
from app.api.deps import get_current_admin

router = APIRouter(prefix="/users", tags=["用户管理"])

@router.get("/", response_model=List[UserResponse])
def list_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_admin)
):
    users = get_users(db, skip=skip, limit=limit)
    return users

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_admin)):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return user

@router.post("/", response_model=UserResponse)
def create_new_user(user_data: UserCreate, db: Session = Depends(get_db), current_user = Depends(get_current_admin)):
    user = create_user(db, user_data)
    return user

@router.put("/{user_id}", response_model=UserResponse)
def update_existing_user(user_id: int, user_data: UserUpdate, db: Session = Depends(get_db), current_user = Depends(get_current_admin)):
    user = update_user(db, user_id, user_data)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return user

@router.delete("/{user_id}")
def delete_existing_user(user_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_admin)):
    success = delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="用户不存在")
    return {"message": "用户已删除"}
