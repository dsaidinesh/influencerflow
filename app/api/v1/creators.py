from fastapi import APIRouter, Depends, HTTPException, Query, Path
from typing import List, Optional
import uuid

from app.services.supabase_service import SupabaseService
from app.schemas.creator import CreatorCreate, CreatorUpdate, CreatorList, CreatorDetail, Creator
from app.services.ai_service import AIService

router = APIRouter()
supabase_service = SupabaseService()
ai_service = AIService()


@router.get("/", response_model=dict)
async def get_creators(
    search: Optional[str] = None,
    platform: Optional[str] = None,
    niche: Optional[str] = None,
    min_followers: Optional[int] = None,
    max_followers: Optional[int] = None,
    country: Optional[str] = None,
    language: Optional[str] = None,
    min_engagement: Optional[float] = None,
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    """
    Search and filter creators with match scoring
    """
    creators = await supabase_service.get_creators(
        skip=offset, 
        limit=limit,
        platform=platform,
        niche=niche,
        min_followers=min_followers,
        max_followers=max_followers,
        country=country,
        # Language filter to be added
        min_engagement=min_engagement
    )
    
    # Format the response
    return {
        "creators": creators,
        "total": len(creators),
        "filters_applied": {
            "niche": niche or "all",
            "platform": platform or "all",
            "size": "all"
        }
    }


@router.post("/search")
async def search_creators(
    query: dict,
):
    """
    AI-powered creator search
    """
    search_query = query.get("query", "")
    budget_range = query.get("budget_range")
    target_audience = query.get("target_audience")
    
    search_results = await ai_service.search_creators(
        search_query, 
        budget_range=budget_range, 
        target_audience=target_audience
    )
    
    return search_results


@router.get("/{creator_id}")
async def get_creator_by_id(
    creator_id: str = Path(..., description="The ID of the creator to get"),
    campaign_id: Optional[str] = None,
):
    """
    Get detailed creator profile with campaign match analysis
    """
    creator = await supabase_service.get_creator(creator_id)
    if not creator:
        raise HTTPException(status_code=404, detail="Creator not found")
    
    # Add campaign match analysis if campaign_id is provided
    if campaign_id:
        # This would be implemented in a real application
        creator["campaign_match"] = {
            "percentage": 85,
            "status": "high",
            "reasons": [
                {
                    "factor": "Perfect niche alignment",
                    "description": "Creator's niche perfectly matches campaign requirements",
                    "impact": "high"
                }
            ]
        }
    
    return creator


@router.post("/", response_model=dict)
async def create_creator(
    creator: CreatorCreate,
):
    """
    Create a new creator
    """
    created_creator = await supabase_service.create_creator(creator)
    if not created_creator:
        raise HTTPException(status_code=400, detail="Failed to create creator")
    
    return created_creator


@router.put("/{creator_id}", response_model=dict)
async def update_creator(
    creator: CreatorUpdate,
    creator_id: str = Path(..., description="The ID of the creator to update"),
):
    """
    Update an existing creator
    """
    # Remove None values to avoid overwriting with nulls
    update_data = {k: v for k, v in creator.model_dump().items() if v is not None}
    
    updated_creator = await supabase_service.update_creator(creator_id, update_data)
    if not updated_creator:
        raise HTTPException(status_code=404, detail="Creator not found")
    
    return updated_creator


@router.delete("/{creator_id}")
async def delete_creator(
    creator_id: str = Path(..., description="The ID of the creator to delete"),
):
    """
    Delete a creator
    """
    success = await supabase_service.delete_creator(creator_id)
    if not success:
        raise HTTPException(status_code=404, detail="Creator not found")
    
    return {"message": "Creator deleted successfully"} 