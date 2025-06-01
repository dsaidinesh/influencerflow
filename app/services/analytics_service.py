import logging
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import random
from app.services.supabase_service import SupabaseService

logger = logging.getLogger(__name__)


class AnalyticsService:
    """
    Service for analytics and reporting
    """
    
    async def get_campaign_analytics(self, db: Session, campaign_id: str) -> Dict[str, Any]:
        """
        Get analytics for a specific campaign
        """
        try:
            # Get the campaign from Supabase
            campaign = await SupabaseService.get_campaign(campaign_id)
            
            if not campaign:
                return None
            
            # TODO: Replace with actual data from Supabase
            # For now, generate placeholder analytics data
            
            # Generate placeholder performance data
            total_reach = random.randint(300000, 600000)
            total_engagement = int(total_reach * random.uniform(0.05, 0.08))
            total_views = int(total_reach * random.uniform(0.7, 0.9))
            avg_engagement_rate = round(total_engagement / total_reach * 100, 1)
            roi = round(random.uniform(2.5, 4.0), 1)
            
            # Get creators associated with this campaign via contracts
            contracts = await SupabaseService.get_contracts(campaign_id=campaign_id, limit=10)
            
            # Generate placeholder creator performance data
            creator_performance = []
            for i, contract in enumerate(contracts[:3]):  # Limit to 3 creators for placeholder
                creator_id = contract.get("creator_id")
                creator = await SupabaseService.get_creator(creator_id)
                
                if creator:
                    content_views = int(creator.get("followers_count_numeric", 10000) * random.uniform(0.2, 0.4))
                    engagement = int(content_views * (creator.get("engagement_rate", 5.0) / 100))
                    creator_performance.append({
                        "creator_id": creator["id"],
                        "creator_name": creator["name"],
                        "content_views": content_views,
                        "engagement": engagement,
                        "engagement_rate": creator.get("engagement_rate", 5.0),
                        "delivery_status": "completed" if i < 2 else "pending"
                    })
            
            # Generate placeholder timeline data (last 7 days)
            timeline = []
            base_date = datetime.utcnow() - timedelta(days=7)
            for i in range(7):
                date = base_date + timedelta(days=i)
                date_str = date.strftime("%Y-%m-%d")
                daily_views = int(total_views / 7 * random.uniform(0.8, 1.2))
                daily_engagement = int(daily_views * random.uniform(0.05, 0.08))
                timeline.append({
                    "date": date_str,
                    "views": daily_views,
                    "engagement": daily_engagement
                })
            
            return {
                "campaign_id": campaign_id,
                "performance": {
                    "total_reach": total_reach,
                    "total_engagement": total_engagement,
                    "total_views": total_views,
                    "average_engagement_rate": avg_engagement_rate,
                    "roi": roi
                },
                "creator_performance": creator_performance,
                "timeline": timeline
            }
            
        except Exception as e:
            logger.error(f"Error fetching campaign analytics: {str(e)}")
            return None
    
    async def get_analytics_dashboard(self, db: Session) -> Dict[str, Any]:
        """
        Get overall platform analytics dashboard
        """
        try:
            # Get actual data from Supabase
            campaigns = await SupabaseService.get_campaigns(limit=1000)
            creators = await SupabaseService.get_creators(limit=1000)
            contracts = await SupabaseService.get_contracts(limit=1000)
            
            # Generate overview data
            total_campaigns = len(campaigns)
            active_campaigns = len([c for c in campaigns if c.get("status") == "active"])
            total_creators = len(creators)
            total_contracts = len(contracts)
            total_budget = sum(c.get("total_budget", 0) for c in campaigns)
            
            # Generate placeholder performance metrics
            avg_campaign_roi = round(random.uniform(2.5, 3.5), 1)
            avg_engagement_rate = round(random.uniform(4.8, 5.5), 1)
            creator_satisfaction = round(random.uniform(4.3, 4.8), 1)
            contract_completion_rate = round(random.uniform(85, 95), 1)
            
            # Generate placeholder recent activity
            recent_activity = [
                {
                    "type": "contract_signed",
                    "description": "Contract signed with creator for campaign",
                    "timestamp": (datetime.utcnow() - timedelta(hours=3)).isoformat()
                },
                {
                    "type": "campaign_completed",
                    "description": "Campaign marked as completed",
                    "timestamp": (datetime.utcnow() - timedelta(days=1)).isoformat()
                },
                {
                    "type": "payment_processed",
                    "description": "Payment processed for creator",
                    "timestamp": (datetime.utcnow() - timedelta(days=2)).isoformat()
                },
                {
                    "type": "creator_added",
                    "description": "New creator added to the platform",
                    "timestamp": (datetime.utcnow() - timedelta(days=3)).isoformat()
                }
            ]
            
            return {
                "overview": {
                    "total_campaigns": total_campaigns,
                    "active_campaigns": active_campaigns,
                    "total_creators": total_creators,
                    "total_contracts": total_contracts,
                    "total_budget_managed": total_budget
                },
                "performance_metrics": {
                    "average_campaign_roi": avg_campaign_roi,
                    "average_engagement_rate": avg_engagement_rate,
                    "creator_satisfaction_score": creator_satisfaction,
                    "contract_completion_rate": contract_completion_rate
                },
                "recent_activity": recent_activity
            }
            
        except Exception as e:
            logger.error(f"Error generating analytics dashboard: {str(e)}")
            return {
                "overview": {
                    "total_campaigns": 0,
                    "active_campaigns": 0,
                    "total_creators": 0,
                    "total_contracts": 0,
                    "total_budget_managed": 0
                },
                "performance_metrics": {
                    "average_campaign_roi": 0,
                    "average_engagement_rate": 0,
                    "creator_satisfaction_score": 0,
                    "contract_completion_rate": 0
                },
                "recent_activity": []
            } 