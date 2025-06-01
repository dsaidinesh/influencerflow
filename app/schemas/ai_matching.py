from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class AISimilaritySearchRequest(BaseModel):
    """Request model for AI similarity search"""
    product_name: str = Field(..., description="The name of the product being promoted")
    brand: str = Field(..., description="The brand name")
    product_description: str = Field(..., description="Description of the product")
    target_audience: str = Field(..., description="Description of the target audience")
    key_usecases: List[str] = Field(..., description="Key use cases for the product")
    campaign_goal: str = Field(..., description="Goal or objective of the campaign")
    product_niche: str = Field(..., description="Product category or niche")
    total_budget: float = Field(..., description="Total budget allocated for the campaign")
    
    class Config:
        schema_extra = {
            "example": {
                "product_name": "FitBand Pro",
                "brand": "TechFit",
                "product_description": "A smart fitness band that tracks activities and provides health insights",
                "target_audience": "Health-conscious individuals aged 25-45 who are interested in tracking their fitness",
                "key_usecases": ["Activity tracking", "Heart rate monitoring", "Sleep analysis"],
                "campaign_goal": "Increase brand awareness and drive sales for the new FitBand Pro",
                "product_niche": "Fitness Technology",
                "total_budget": 25000
            }
        }


class CampaignSimilaritySearchRequest(BaseModel):
    """Request model for campaign-based AI similarity search"""
    campaign_id: str = Field(..., description="The ID of the campaign to use for matching")
    match_threshold: float = Field(0.5, description="Minimum similarity score (0-1) to include in results")
    match_count: int = Field(10, description="Maximum number of results to return")
    
    class Config:
        schema_extra = {
            "example": {
                "campaign_id": "550e8400-e29b-41d4-a716-446655440000",
                "match_threshold": 0.5,
                "match_count": 10
            }
        }


class DetailedScores(BaseModel):
    """Detailed match scores for an influencer"""
    niche_match: str = Field(..., description="Niche compatibility score as percentage")
    audience_match: str = Field(..., description="Audience compatibility score as percentage")
    engagement_score: str = Field(..., description="Engagement quality score as percentage")
    budget_fit: str = Field(..., description="Budget compatibility score as percentage")


class InfluencerMatch(BaseModel):
    """Model for a matched influencer with scores"""
    id: str = Field(..., description="The influencer's unique ID")
    influencer_name: str = Field(..., description="The name of the influencer with handle")
    match_score: str = Field(..., description="Overall match score as percentage")
    niche: str = Field(..., description="The influencer's content niche")
    followers: str = Field(..., description="Number of followers formatted (e.g., '374K')")
    engagement: str = Field(..., description="Engagement rate as percentage")
    collaboration_rate: str = Field(..., description="Standard rate for collaborations")
    detailed_scores: DetailedScores = Field(..., description="Detailed breakdown of match scores")
    
    class Config:
        schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "influencer_name": "Mia Martinez (@mia_martinez838)",
                "match_score": "78.31%",
                "niche": "Fitness",
                "followers": "374K",
                "engagement": "5.9%",
                "collaboration_rate": "$3769",
                "detailed_scores": {
                    "niche_match": "91.60%",
                    "audience_match": "43.00%",
                    "engagement_score": "82.00%",
                    "budget_fit": "100.00%"
                }
            }
        }


class AISimilaritySearchResponse(BaseModel):
    """Response model for AI similarity search"""
    matches: List[InfluencerMatch] = Field(..., description="List of matched influencers with scores")
    total_matches: int = Field(..., description="Total number of matches found")
    search_parameters: Dict[str, Any] = Field(..., description="The parameters used for the search") 