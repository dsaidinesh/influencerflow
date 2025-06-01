from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Literal, Dict, List, Any
from uuid import UUID
from datetime import datetime


# Base Payment schema (common properties)
class PaymentBase(BaseModel):
    contract_id: UUID
    amount: float
    due_date: Optional[datetime] = None


# Payment schema for creation
class PaymentCreate(PaymentBase):
    pass


# Payment schema for update (all fields optional)
class PaymentUpdate(BaseModel):
    amount: Optional[float] = None
    status: Optional[Literal["pending", "processing", "completed", "failed"]] = None
    payment_method: Optional[str] = None
    transaction_id: Optional[str] = None
    due_date: Optional[datetime] = None
    paid_at: Optional[datetime] = None


# Payment schema for response (returned from API)
class Payment(PaymentBase):
    id: UUID
    status: Literal["pending", "processing", "completed", "failed"]
    payment_method: Optional[str] = None
    transaction_id: Optional[str] = None
    paid_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# Payment schema for list response with minimal info
class PaymentList(BaseModel):
    id: UUID
    contract_id: UUID
    amount: float
    status: str
    payment_method: Optional[str] = None
    due_date: Optional[datetime] = None
    paid_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


# Schema for processing payment
class PaymentProcess(BaseModel):
    payment_method: str = Field(default="card", description="Payment method to use for processing")


# Schema for payment process response
class ProcessPaymentResponse(BaseModel):
    payment_id: UUID
    status: str
    transaction_id: str
    estimated_completion: datetime


# Schema for payment dashboard
class PaymentDashboard(BaseModel):
    total_payments: Dict[str, Any]
    pending_payments: Dict[str, Any]
    completed_payments: Dict[str, Any]
    recent_payments: List[Dict[str, Any]] 