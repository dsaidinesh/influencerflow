from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Literal, List
from uuid import UUID
from datetime import datetime


# Base Campaign schema (common properties)
class CampaignBase(BaseModel):
    product_name: str
    brand_name: str
    product_description: Optional[str] = None
    target_audience: Optional[str] = None
    key_use_cases: Optional[str] = None
    campaign_goal: Optional[str] = None
    product_niche: Optional[str] = None
    total_budget: float


# Campaign schema for creation
class CampaignCreate(CampaignBase):
    pass


# Campaign schema for update (all fields optional)
class CampaignUpdate(BaseModel):
    product_name: Optional[str] = None
    brand_name: Optional[str] = None
    product_description: Optional[str] = None
    target_audience: Optional[str] = None
    key_use_cases: Optional[str] = None
    campaign_goal: Optional[str] = None
    product_niche: Optional[str] = None
    total_budget: Optional[float] = None
    status: Optional[Literal["active", "draft", "completed", "paused"]] = None


# Campaign schema for response (returned from API)
class Campaign(CampaignBase):
    id: UUID
    status: Literal["active", "draft", "completed", "paused"]
    influencer_count: int
    campaign_code: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# Campaign schema for list response with minimal info
class CampaignList(BaseModel):
    id: UUID
    product_name: str
    brand_name: str
    total_budget: float
    status: str
    influencer_count: int
    campaign_code: Optional[str] = None
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# Schema for AI search request
class CampaignAISearch(BaseModel):
    query: str
    budget_range: Optional[List[float]] = None
    target_audience: Optional[str] = None


# Schema for select influencer request
class SelectInfluencer(BaseModel):
    influencer_id: UUID
    notes: Optional[str] = None


# Schema for AI match analysis request
class MatchAnalysisRequest(BaseModel):
    influencer_id: UUID


# Schema for AI match analysis response
class MatchAnalysisResponse(BaseModel):
    match_percentage: float
    match_status: Literal["high", "medium", "low"]
    detailed_analysis: dict
    recommendation: str
    estimated_performance: dict 