from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.employee import Employee, Schedule
from app.schemas.employee import EmployeeCreate, EmployeeUpdate, ScheduleCreate
from datetime import datetime
from typing import Optional, List

def get_employee_by_id(db: Session, employee_id: int) -> Optional[Employee]:
    return db.execute(select(Employee).where(Employee.id == employee_id)).scalar_one_or_none()

def get_employees(db: Session, skip: int = 0, limit: int = 100, store_id: Optional[int] = None, department: Optional[str] = None, keyword: Optional[str] = None) -> List[Employee]:
    query = select(Employee)
    if store_id:
        query = query.where(Employee.store_id == store_id)
    if department:
        query = query.where(Employee.department == department)
    if keyword:
        query = query.where((Employee.name.contains(keyword)) | (Employee.phone.contains(keyword)))
    return db.execute(query.offset(skip).limit(limit)).scalars().all()

def create_employee(db: Session, employee_data: EmployeeCreate) -> Employee:
    employee = Employee(
        **employee_data.model_dump(),
        entry_date=datetime.now()
    )
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee

def update_employee(db: Session, employee_id: int, employee_data: EmployeeUpdate) -> Optional[Employee]:
    employee = get_employee_by_id(db, employee_id)
    if not employee:
        return None
    update_data = employee_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(employee, key, value)
    db.commit()
    db.refresh(employee)
    return employee

def delete_employee(db: Session, employee_id: int) -> bool:
    employee = get_employee_by_id(db, employee_id)
    if not employee:
        return False
    employee.status = False
    db.commit()
    return True

def get_schedules(db: Session, employee_id: Optional[int] = None, store_id: Optional[int] = None, date: Optional[datetime] = None) -> List[Schedule]:
    query = select(Schedule)
    if employee_id:
        query = query.where(Schedule.employee_id == employee_id)
    if store_id:
        query = query.where(Schedule.store_id == store_id)
    if date:
        query = query.where(Schedule.shift_date == date)
    return db.execute(query).scalars().all()

def create_schedule(db: Session, schedule_data: ScheduleCreate) -> Schedule:
    schedule = Schedule(**schedule_data.model_dump())
    db.add(schedule)
    db.commit()
    db.refresh(schedule)
    return schedule
