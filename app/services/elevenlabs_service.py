import httpx
from typing import Dict, Optional, Any, Union
import json
from app.core.config import settings

class ElevenLabsService:
    def __init__(self):
        self.api_key = settings.ELEVENLABS_API_KEY
        self.base_url = "https://api.elevenlabs.io/v1/convai"
        self.agent_id = settings.ELEVENLABS_AGENT_ID
        self.phone_number_id = settings.ELEVENLABS_PHONE_NUMBER_ID
    
    async def initiate_outbound_call(
        self,
        creator_phone: str,
        campaign_data: Dict[str, Any],
        creator_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Initiate outbound call to creator"""
        
        # Format followers count safely
        followers_count = creator_data.get('followers_count', 0)
        if isinstance(followers_count, str):
            try:
                followers_count = int(followers_count)
            except (ValueError, TypeError):
                followers_count = 0
                
        # Format average views safely
        avg_views = creator_data.get('avg_views', 0)
        if isinstance(avg_views, str):
            try:
                avg_views = int(avg_views)
            except (ValueError, TypeError):
                avg_views = 0
        
        # Create a single influencer profile string
        influencer_profile = {
            "name": creator_data.get("name", ""),
            "channel": creator_data.get("username", creator_data.get("handle", "")),
            "niche": creator_data.get("niche", ""),
            "about": creator_data.get("bio", "Content creator"),
            "followers": f"{followers_count/1000:.1f}K" if followers_count >= 1000 else str(followers_count),
            "audienceType": creator_data.get("audience_type", creator_data.get("niche", "") + " Enthusiasts"),
            "engagement": f"{creator_data.get('engagement_rate', 0)}%",
            "avgViews": f"{avg_views/1000:.1f}K" if avg_views >= 1000 else str(avg_views),
            "location": f"{creator_data.get('city', '')}, {creator_data.get('country', '')}",
            "languages": creator_data.get("languages", ["English"]),
            "collaboration_rate": creator_data.get("rate", 0)
        }
        
        # Prepare dynamic variables for personalization
        dynamic_variables = {
            "InfluencerProfile": json.dumps(influencer_profile),
            "campaignBrief": self._generate_campaign_brief(campaign_data),
            "priceRange": f"{campaign_data.get('min_budget', 0)}-{campaign_data.get('max_budget', 0)}",
            "influencerName": creator_data.get("name", "")
        }
        
        payload = {
            "agent_id": self.agent_id,
            "agent_phone_number_id": self.phone_number_id,
            "to_number": creator_phone,
            "conversation_initiation_client_data": {
                "dynamic_variables": dynamic_variables
            }
        }
        
        headers = {
            "xi-api-key": self.api_key,
            "Content-Type": "application/json"
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/twilio/outbound-call",
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            return response.json()
    
    async def get_conversation_analysis(self, conversation_id: str) -> Dict[str, Any]:
        """Get detailed conversation analysis"""
        headers = {"xi-api-key": self.api_key}
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/conversations/{conversation_id}",
                headers=headers
            )
            response.raise_for_status()
            return response.json()
    
    async def list_conversations(
        self,
        agent_id: Optional[str] = None,
        call_successful: Optional[str] = None,
        cursor: Optional[str] = None,
        page_size: int = 30
    ) -> Dict[str, Any]:
        """List conversations with filters"""
        headers = {"xi-api-key": self.api_key}
        params = {}
        
        # Add optional parameters
        if cursor:
            params["cursor"] = cursor
        if page_size:
            params["page_size"] = page_size
        if agent_id:
            params["agent_id"] = agent_id
        if call_successful:
            params["call_successful"] = call_successful
            
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/conversations",
                headers=headers,
                params=params
            )
            response.raise_for_status()
            return response.json()
    
    def _generate_campaign_brief(self, campaign_data: Dict[str, Any]) -> str:
        """Generate comprehensive campaign brief from campaign data"""
        brand_name = campaign_data.get("brand_name", "")
        product_name = campaign_data.get("product_name", "")
        product_description = campaign_data.get("product_description", "")
        target_audience = campaign_data.get("target_audience", "")
        total_budget = campaign_data.get("total_budget", 0)
        key_usecases = campaign_data.get("key_usecases", "")
        campaign_goal = campaign_data.get("campaign_goal", "increase brand awareness")
        
        return f"""{brand_name} is launching a strategic marketing campaign for its latest innovation — the {product_name}, {product_description}. 
        The campaign's primary objective is to {campaign_goal} by highlighting the {product_name}'s features, such as {key_usecases}. 
        Through a mix of visually engaging and informative content, the campaign will position {product_name} as a must-have tool for anyone serious about improving their lifestyle. 
        Targeting {target_audience}, the campaign will roll out across multiple digital channels including social media, influencer partnerships, and digital marketing. 
        Creative messaging will focus on empowering users with a budget of ${total_budget:,.0f} for this campaign."""
    
    def _determine_collaboration_type(self, campaign_data: Dict[str, Any]) -> str:
        """Determine collaboration type based on campaign data"""
        if campaign_data.get("key_usecases") and "video" in str(campaign_data.get("key_usecases", "")).lower():
            return "video content creation"
        elif campaign_data.get("campaign_goal") and "post" in campaign_data.get("campaign_goal", "").lower():
            return "social media posts"
        else:
            return "content collaboration"
    
    async def get_conversation_audio(self, conversation_id: str) -> bytes:
        """Get audio recording of a conversation"""
        headers = {"xi-api-key": self.api_key}
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/conversations/{conversation_id}/audio",
                headers=headers
            )
            response.raise_for_status()
            return response.content 