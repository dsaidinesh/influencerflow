import logging
from typing import List, Dict, Any, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from datetime import datetime
import uuid
from fastapi import HTTPException

from app.models.campaign import Campaign
from app.schemas.campaign import CampaignCreate, CampaignUpdate
from app.services.ai_service import AIService
from app.services.supabase_service import SupabaseService

logger = logging.getLogger(__name__)


class CampaignService:
    """
    Service for managing campaign-related operations
    """
    
    def __init__(self):
        self.ai_service = AIService()
    
    @staticmethod
    async def get_campaigns(
        skip: int = 0,
        limit: int = 100,
        status: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get all campaigns with optional filtering
        """
        try:
            return await SupabaseService.get_campaigns(skip=skip, limit=limit, status=status)
        except Exception as e:
            logger.error(f"Error getting campaigns: {e}")
            raise HTTPException(status_code=500, detail="Error retrieving campaigns")
    
    @staticmethod
    async def get_campaign(campaign_id: str) -> Dict[str, Any]:
        """
        Get a single campaign by ID
        """
        try:
            campaign = await SupabaseService.get_campaign(campaign_id)
            if not campaign:
                raise HTTPException(status_code=404, detail=f"Campaign with ID {campaign_id} not found")
            return campaign
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error getting campaign {campaign_id}: {e}")
            raise HTTPException(status_code=500, detail=f"Error retrieving campaign {campaign_id}")
    
    @staticmethod
    async def create_campaign(campaign_data: CampaignCreate) -> Dict[str, Any]:
        """
        Create a new campaign
        """
        try:
            # Set default values
            campaign_dict = campaign_data.model_dump()
            campaign_dict["id"] = str(uuid.uuid4())
            campaign_dict["created_at"] = datetime.utcnow().isoformat()
            campaign_dict["updated_at"] = datetime.utcnow().isoformat()
            
            # Create campaign in database
            campaign = await SupabaseService.create_campaign(CampaignCreate(**campaign_dict))
            if not campaign:
                raise HTTPException(status_code=500, detail="Failed to create campaign")
            
            return campaign
        except Exception as e:
            logger.error(f"Error creating campaign: {e}")
            raise HTTPException(status_code=500, detail="Error creating campaign")
    
    @staticmethod
    async def update_campaign(campaign_id: str, campaign_data: CampaignUpdate) -> Dict[str, Any]:
        """
        Update an existing campaign
        """
        try:
            # Check if campaign exists
            existing_campaign = await SupabaseService.get_campaign(campaign_id)
            if not existing_campaign:
                raise HTTPException(status_code=404, detail=f"Campaign with ID {campaign_id} not found")
            
            # Update campaign
            update_data = campaign_data.model_dump(exclude_unset=True)
            update_data["updated_at"] = datetime.utcnow().isoformat()
            
            updated_campaign = await SupabaseService.update_campaign(campaign_id, update_data)
            if not updated_campaign:
                raise HTTPException(status_code=500, detail=f"Failed to update campaign {campaign_id}")
            
            return updated_campaign
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error updating campaign {campaign_id}: {e}")
            raise HTTPException(status_code=500, detail=f"Error updating campaign {campaign_id}")
    
    @staticmethod
    async def delete_campaign(campaign_id: str) -> Dict[str, Any]:
        """
        Delete a campaign by ID
        """
        try:
            # Check if campaign exists
            existing_campaign = await SupabaseService.get_campaign(campaign_id)
            if not existing_campaign:
                raise HTTPException(status_code=404, detail=f"Campaign with ID {campaign_id} not found")
            
            # Delete campaign
            success = await SupabaseService.delete_campaign(campaign_id)
            if not success:
                raise HTTPException(status_code=500, detail=f"Failed to delete campaign {campaign_id}")
            
            return {"id": campaign_id, "deleted": True}
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error deleting campaign {campaign_id}: {e}")
            raise HTTPException(status_code=500, detail=f"Error deleting campaign {campaign_id}")
    
    @staticmethod
    async def get_campaigns_by_brand(brand_name: str) -> List[Dict[str, Any]]:
        """
        Get all campaigns for a specific brand
        """
        try:
            # Get all campaigns
            campaigns = await SupabaseService.get_campaigns(limit=1000)
            
            # Filter by brand name
            return [c for c in campaigns if c.get("brand_name", "").lower() == brand_name.lower()]
        except Exception as e:
            logger.error(f"Error getting campaigns for brand {brand_name}: {e}")
            raise HTTPException(status_code=500, detail=f"Error retrieving campaigns for brand {brand_name}")
    
    async def select_influencer(self, db: Session, campaign_id: str, 
                             influencer_id: str, notes: Optional[str] = None) -> Dict[str, Any]:
        """
        Select an influencer for a campaign and move to outreach
        """
        try:
            # TODO: Replace with Supabase implementation
            # For now, return placeholder data
            outreach_id = str(uuid.uuid4())
            
            return {
                "campaign_id": campaign_id,
                "influencer_id": influencer_id,
                "status": "selected_for_outreach",
                "outreach_entry_created": True,
                "next_step": "outreach_management",
                "outreach_id": outreach_id
            }
            
        except Exception as e:
            logger.error(f"Error selecting influencer for campaign: {str(e)}")
            return None
    
    async def ai_match_analysis(self, db: Session, campaign_id: str, 
                             influencer_id: str) -> Dict[str, Any]:
        """
        Get AI-powered match analysis for campaign and influencer
        """
        try:
            # Call the AI service for match analysis
            return await self.ai_service.analyze_creator_match(campaign_id, influencer_id)
            
        except Exception as e:
            logger.error(f"Error getting AI match analysis: {str(e)}")
            return None 