from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Literal, Dict, List, Any
from uuid import UUID
from datetime import datetime


# Base Contract schema (common properties)
class ContractBase(BaseModel):
    campaign_id: UUID
    creator_id: UUID
    terms: Optional[Dict[str, Any]] = None
    payment_amount: float
    payment_schedule: Optional[List[Dict[str, Any]]] = None


# Contract schema for creation
class ContractCreate(ContractBase):
    pass


# Contract schema for update (all fields optional)
class ContractUpdate(BaseModel):
    terms: Optional[Dict[str, Any]] = None
    payment_amount: Optional[float] = None
    payment_schedule: Optional[List[Dict[str, Any]]] = None
    status: Optional[Literal["draft", "sent", "signed", "completed"]] = None


# Contract schema for response (returned from API)
class Contract(ContractBase):
    id: UUID
    status: Literal["draft", "sent", "signed", "completed"]
    signed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# Contract schema for list response with minimal info
class ContractList(BaseModel):
    id: UUID
    campaign_title: str
    creator_name: str
    payment_amount: float
    status: str
    signed_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


# Contract schema for detailed response
class ContractDetail(BaseModel):
    id: UUID
    campaign: Dict[str, Any]
    creator: Dict[str, Any]
    terms: Optional[Dict[str, Any]] = None
    payment_amount: float
    payment_schedule: Optional[List[Dict[str, Any]]] = None
    status: str
    signed_at: Optional[datetime] = None
    deliverables_status: Optional[List[Dict[str, Any]]] = None
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True) 