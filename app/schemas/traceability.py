from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class TraceabilityBase(BaseModel):
    product_id: int
    product_name: Optional[str] = None
    batch_no: Optional[str] = None
    origin: Optional[str] = None
    supplier: Optional[str] = None
    harvest_date: Optional[datetime] = None
    arrival_date: Optional[datetime] = None
    storage_condition: Optional[str] = None
    quality_report: Optional[str] = None

class TraceabilityCreate(TraceabilityBase):
    pass

class TraceabilityUpdate(BaseModel):
    product_name: Optional[str] = None
    origin: Optional[str] = None
    supplier: Optional[str] = None
    harvest_date: Optional[datetime] = None
    arrival_date: Optional[datetime] = None
    storage_condition: Optional[str] = None
    quality_report: Optional[str] = None
    status: Optional[str] = None

class TraceabilityResponse(TraceabilityBase):
    id: int
    status: str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class TraceabilityStepBase(BaseModel):
    traceability_id: int
    step_no: int = 1
    step_name: str
    description: Optional[str] = None
    operator: Optional[str] = None

class TraceabilityStepCreate(TraceabilityStepBase):
    pass

class TraceabilityStepResponse(TraceabilityStepBase):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
