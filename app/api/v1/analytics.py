from fastapi import APIRouter, Depends, HTTPException, Path
from typing import Optional

from app.services.analytics_service import AnalyticsService

router = APIRouter()
analytics_service = AnalyticsService()


@router.get("/campaigns/{campaign_id}", response_model=dict)
async def get_campaign_analytics(
    campaign_id: str = Path(..., description="The ID of the campaign to analyze")
):
    """
    Campaign performance analytics
    """
    analytics = await analytics_service.get_campaign_analytics(None, campaign_id)
    if not analytics:
        raise HTTPException(status_code=404, detail="Campaign not found or analytics not available")
    
    return analytics


@router.get("/dashboard", response_model=dict)
async def get_analytics_dashboard():
    """
    Overall platform analytics
    """
    dashboard = await analytics_service.get_analytics_dashboard(None)
    if not dashboard:
        raise HTTPException(status_code=500, detail="Failed to generate analytics dashboard")
    
    return dashboard 