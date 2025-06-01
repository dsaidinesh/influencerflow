from fastapi import APIRouter, Depends, HTTPException, Query, Path, Body
from typing import Dict, List, Any, Optional
from app.services.ai_service import AIService
from app.schemas.ai_matching import (
    AISimilaritySearchRequest, 
    AISimilaritySearchResponse,
    CampaignSimilaritySearchRequest
)

router = APIRouter()
ai_service = AIService()

@router.post("/similaritysearch", response_model=AISimilaritySearchResponse)
async def similarity_search(
    request_data: AISimilaritySearchRequest = Body(..., description="Campaign details for similarity search")
) -> Dict[str, Any]:
    """
    Perform AI-powered similarity search to find the best influencer matches for a campaign.
    This endpoint analyzes campaign details and computes similarity scores against creator profiles.
    """
    result = await ai_service.similarity_search(request_data)
    return result


@router.post("/campaign-similarity", response_model=AISimilaritySearchResponse)
async def campaign_similarity_search(
    request_data: CampaignSimilaritySearchRequest = Body(..., description="Campaign ID for similarity search")
) -> Dict[str, Any]:
    """
    Perform AI-powered similarity search using an existing campaign.
    This simplified endpoint just needs the campaign ID and will fetch the campaign details internally.
    """
    result = await ai_service.campaign_similarity_search(
        campaign_id=request_data.campaign_id,
        match_threshold=request_data.match_threshold,
        match_count=request_data.match_count
    )
    return result


@router.get("/campaign/{campaign_id}/matches", response_model=AISimilaritySearchResponse)
async def get_campaign_matches(
    campaign_id: str = Path(..., description="The ID of the campaign"),
    match_threshold: float = Query(0.5, description="Minimum similarity score (0-1) to include in results"),
    match_count: int = Query(10, description="Maximum number of results to return")
) -> Dict[str, Any]:
    """
    Get AI-powered influencer matches for an existing campaign.
    This endpoint provides a convenient GET method alternative to the POST campaign-similarity endpoint.
    """
    result = await ai_service.campaign_similarity_search(
        campaign_id=campaign_id,
        match_threshold=match_threshold,
        match_count=match_count
    )
    return result


@router.post("/creator/{creator_id}/generate-embedding", response_model=Dict[str, Any])
async def generate_creator_embedding(
    creator_id: str = Path(..., description="The ID of the creator")
) -> Dict[str, Any]:
    """
    Generate and store an embedding vector for a creator's profile.
    This is used for similarity matching with campaigns.
    """
    success = await ai_service.generate_creator_embedding(creator_id)
    
    if not success:
        raise HTTPException(status_code=400, detail="Failed to generate embedding for creator")
    
    return {"status": "success", "message": "Creator embedding generated successfully"} 