from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.user import UserLogin, UserResponse, Token
from app.services.user_service import login_user, create_user
from app.schemas.user import UserCreate

router = APIRouter(prefix="/auth", tags=["认证"])

@router.post("/login", response_model=dict)
def login(form_data: UserLogin, db: Session = Depends(get_db)):
    result = login_user(db, form_data.username, form_data.password)
    if not result:
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    return result

@router.post("/register", response_model=UserResponse)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    from app.services.user_service import get_user_by_username
    existing_user = get_user_by_username(db, user_data.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="用户名已存在")
    user = create_user(db, user_data)
    return user
