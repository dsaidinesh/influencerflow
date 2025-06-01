from fastapi import APIRouter, Depends, HTTPException, Query, Path, Body
from typing import List, Optional, Dict, Any

from app.schemas.campaign import (
    CampaignCreate, CampaignUpdate, CampaignList, Campaign, 
    SelectInfluencer, MatchAnalysisRequest, MatchAnalysisResponse
)
from app.services.campaign_service import CampaignService

router = APIRouter()


@router.post("/", response_model=Dict[str, Any])
async def create_campaign(
    campaign: CampaignCreate
):
    """
    Create a new campaign
    """
    return await CampaignService.create_campaign(campaign)


@router.get("/", response_model=List[Dict[str, Any]])
async def get_campaigns(
    status: Optional[str] = None,
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    """
    List all campaigns
    """
    return await CampaignService.get_campaigns(skip=offset, limit=limit, status=status)


@router.get("/{campaign_id}", response_model=Dict[str, Any])
async def get_campaign_by_id(
    campaign_id: str = Path(..., description="The ID of the campaign to get")
):
    """
    Get campaign by ID
    """
    return await CampaignService.get_campaign(campaign_id)


@router.put("/{campaign_id}", response_model=Dict[str, Any])
async def update_campaign(
    campaign: CampaignUpdate,
    campaign_id: str = Path(..., description="The ID of the campaign to update")
):
    """
    Update an existing campaign
    """
    return await CampaignService.update_campaign(campaign_id, campaign)


@router.delete("/{campaign_id}", response_model=Dict[str, Any])
async def delete_campaign(
    campaign_id: str = Path(..., description="The ID of the campaign to delete")
):
    """
    Delete a campaign
    """
    return await CampaignService.delete_campaign(campaign_id)


@router.get("/brand/{brand_name}", response_model=List[Dict[str, Any]])
async def get_campaigns_by_brand(
    brand_name: str = Path(..., description="The brand name to filter campaigns by")
):
    """
    Get campaigns for a specific brand
    """
    return await CampaignService.get_campaigns_by_brand(brand_name)


@router.post("/{campaign_id}/select-influencer", response_model=Dict[str, Any])
async def select_influencer_for_campaign(
    influencer_data: SelectInfluencer,
    campaign_id: str = Path(..., description="The ID of the campaign")
):
    """
    Select influencer for campaign and move to outreach
    """
    # This functionality still needs to be migrated to Supabase
    campaign_service = CampaignService()
    result = await campaign_service.select_influencer(
        None,  # Passing None instead of db session 
        campaign_id, 
        influencer_data.influencer_id, 
        influencer_data.notes
    )
    
    if not result:
        raise HTTPException(status_code=404, detail="Campaign or influencer not found")
    
    return result


@router.post("/{campaign_id}/ai-match-analysis", response_model=Dict[str, Any])
async def analyze_campaign_influencer_match(
    match_request: MatchAnalysisRequest,
    campaign_id: str = Path(..., description="The ID of the campaign")
):
    """
    Get AI-powered match analysis for campaign and influencer
    """
    # This functionality still needs to be migrated to Supabase
    campaign_service = CampaignService()
    analysis = await campaign_service.ai_match_analysis(
        None,  # Passing None instead of db session
        campaign_id, 
        match_request.influencer_id
    )
    
    if not analysis:
        raise HTTPException(status_code=404, detail="Failed to perform match analysis")
    
    return analysis 