from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional, Literal
from uuid import UUID
from datetime import datetime


# Base Creator schema (common properties)
class CreatorBase(BaseModel):
    name: str
    email: EmailStr
    platform: Literal["instagram", "youtube", "tiktok", "twitter"]
    followers_count: str
    followers_count_numeric: int
    engagement_rate: float
    niche: str
    language: str
    country: str
    about: Optional[str] = None
    channel_name: Optional[str] = None
    avg_views: Optional[int] = None
    collaboration_rate: Optional[float] = None
    profile_image: Optional[str] = None


# Creator schema for creation
class CreatorCreate(CreatorBase):
    pass


# Creator schema for update (all fields optional)
class CreatorUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    platform: Optional[Literal["instagram", "youtube", "tiktok", "twitter"]] = None
    followers_count: Optional[str] = None
    followers_count_numeric: Optional[int] = None
    engagement_rate: Optional[float] = None
    niche: Optional[str] = None
    language: Optional[str] = None
    country: Optional[str] = None
    about: Optional[str] = None
    channel_name: Optional[str] = None
    avg_views: Optional[int] = None
    collaboration_rate: Optional[float] = None
    rating: Optional[float] = None
    profile_image: Optional[str] = None


# Creator schema for response (returned from API)
class Creator(CreatorBase):
    id: UUID
    rating: Optional[float] = None
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# Creator schema for list response with minimal info
class CreatorList(BaseModel):
    id: UUID
    name: str
    platform: str
    followers_count: str
    engagement_rate: float
    niche: str
    about: Optional[str] = None
    channel_name: Optional[str] = None
    match_percentage: Optional[float] = None
    match_status: Optional[Literal["high", "medium", "low"]] = None
    profile_image: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)


# Creator schema for detailed response with campaign match analysis
class CreatorDetail(Creator):
    audience_type: Optional[str] = None
    previous_brands: Optional[list[str]] = None
    campaign_match: Optional[dict] = None
    
    model_config = ConfigDict(from_attributes=True) 