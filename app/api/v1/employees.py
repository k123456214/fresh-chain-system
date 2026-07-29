from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.core.database import get_db
from app.schemas.employee import EmployeeCreate, EmployeeUpdate, EmployeeResponse, ScheduleCreate, ScheduleResponse
from app.services.employee_service import get_employee_by_id, get_employees, create_employee, update_employee, delete_employee, get_schedules, create_schedule
from app.api.deps import get_current_active_user

router = APIRouter(prefix="/employees", tags=["员工管理"])

@router.get("/", response_model=List[EmployeeResponse])
def list_employees(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    store_id: Optional[int] = None,
    department: Optional[str] = None,
    keyword: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    employees = get_employees(db, skip=skip, limit=limit, store_id=store_id, department=department, keyword=keyword)
    return employees

@router.get("/{employee_id}", response_model=EmployeeResponse)
def get_employee(employee_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_active_user)):
    employee = get_employee_by_id(db, employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="员工不存在")
    return employee

@router.post("/", response_model=EmployeeResponse)
def create_new_employee(employee_data: EmployeeCreate, db: Session = Depends(get_db), current_user = Depends(get_current_active_user)):
    employee = create_employee(db, employee_data)
    return employee

@router.put("/{employee_id}", response_model=EmployeeResponse)
def update_existing_employee(employee_id: int, employee_data: EmployeeUpdate, db: Session = Depends(get_db), current_user = Depends(get_current_active_user)):
    employee = update_employee(db, employee_id, employee_data)
    if not employee:
        raise HTTPException(status_code=404, detail="员工不存在")
    return employee

@router.delete("/{employee_id}")
def delete_existing_employee(employee_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_active_user)):
    success = delete_employee(db, employee_id)
    if not success:
        raise HTTPException(status_code=404, detail="员工不存在")
    return {"message": "员工已删除"}

@router.get("/schedules", response_model=List[ScheduleResponse])
def list_schedules(
    employee_id: Optional[int] = None,
    store_id: Optional[int] = None,
    date: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    target_date = datetime.fromisoformat(date) if date else None
    schedules = get_schedules(db, employee_id=employee_id, store_id=store_id, date=target_date)
    return schedules

@router.post("/schedules", response_model=ScheduleResponse)
def create_new_schedule(schedule_data: ScheduleCreate, db: Session = Depends(get_db), current_user = Depends(get_current_active_user)):
    schedule = create_schedule(db, schedule_data)
    return schedule
