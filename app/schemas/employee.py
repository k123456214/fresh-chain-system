from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class EmployeeBase(BaseModel):
    name: str
    phone: Optional[str] = None
    position: Optional[str] = None
    department: Optional[str] = None
    store_id: Optional[int] = None

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    position: Optional[str] = None
    department: Optional[str] = None
    store_id: Optional[int] = None
    status: Optional[bool] = None

class EmployeeResponse(EmployeeBase):
    id: int
    entry_date: Optional[datetime] = None
    status: bool
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class ScheduleBase(BaseModel):
    employee_id: int
    store_id: Optional[int] = None
    shift_date: datetime
    shift_type: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None

class ScheduleCreate(ScheduleBase):
    pass

class ScheduleResponse(ScheduleBase):
    id: int

    class Config:
        from_attributes = True
