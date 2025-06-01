import logging
from typing import List, Dict, Any, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, func

from app.models.creator import Creator
from app.schemas.creator import CreatorCreate, CreatorUpdate

logger = logging.getLogger(__name__)


class CreatorService:
    """
    Service for managing creator-related operations
    """
    
    async def get_creators(self, db: Session, skip: int = 0, limit: int = 20,
                         search: Optional[str] = None, platform: Optional[str] = None,
                         niche: Optional[str] = None, min_followers: Optional[int] = None,
                         max_followers: Optional[int] = None, country: Optional[str] = None,
                         language: Optional[str] = None, min_engagement: Optional[float] = None) -> List[Creator]:
        """
        Get creators with optional filtering
        """
        try:
            # In a real implementation, this would query the database
            # For MVP, we'll return mock data
            from app.utils.mock_data import MOCK_CREATORS
            
            # Apply filters to mock data
            filtered_creators = MOCK_CREATORS
            
            # Apply search filter
            if search:
                search = search.lower()
                filtered_creators = [c for c in filtered_creators if search in c["name"].lower()]
            
            # Apply platform filter
            if platform:
                filtered_creators = [c for c in filtered_creators if c["platform"] == platform]
            
            # Apply niche filter
            if niche:
                filtered_creators = [c for c in filtered_creators if c["niche"] == niche]
            
            # Apply followers range filter
            if min_followers:
                filtered_creators = [c for c in filtered_creators if c["followers_count_numeric"] >= min_followers]
            if max_followers:
                filtered_creators = [c for c in filtered_creators if c["followers_count_numeric"] <= max_followers]
            
            # Apply country filter
            if country:
                filtered_creators = [c for c in filtered_creators if c["country"] == country]
            
            # Apply language filter
            if language:
                filtered_creators = [c for c in filtered_creators if c["language"] == language]
            
            # Apply engagement filter
            if min_engagement:
                filtered_creators = [c for c in filtered_creators if c["engagement_rate"] >= min_engagement]
            
            # Apply pagination
            paginated_creators = filtered_creators[skip:skip + limit]
            
            # Add filters applied summary
            filters_applied = {
                "niche": niche if niche else "all",
                "platform": platform if platform else "all",
                "size": "custom" if min_followers or max_followers else "all"
            }
            
            return {
                "creators": paginated_creators,
                "total": len(filtered_creators),
                "filters_applied": filters_applied
            }
            
        except Exception as e:
            logger.error(f"Error fetching creators: {str(e)}")
            return {"creators": [], "total": 0, "filters_applied": {}}
    
    async def get_creator_by_id(self, db: Session, creator_id: str, campaign_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Get detailed creator profile with optional campaign match analysis
        """
        try:
            # In a real implementation, this would query the database
            # For MVP, we'll return mock data
            from app.utils.mock_data import MOCK_CREATORS
            
            # Find creator by ID
            creator = None
            for c in MOCK_CREATORS:
                if c["id"] == creator_id:
                    creator = c
                    break
            
            if not creator:
                return None
            
            # Enhance with additional detail fields
            detailed_creator = {**creator}
            detailed_creator["about"] = "Experienced content creator specialized in technology reviews and tutorials."
            detailed_creator["audience_type"] = "Tech Enthusiasts"
            detailed_creator["languages"] = ["English"]
            detailed_creator["previous_brands"] = ["Samsung", "Sony", "Microsoft"]
            
            # Add campaign match if requested
            if campaign_id:
                # In a real implementation, this would call the AI service
                # For MVP, we'll return mock data
                detailed_creator["campaign_match"] = {
                    "percentage": creator["match_percentage"],
                    "status": "high" if creator["match_percentage"] >= 75 else "medium" if creator["match_percentage"] >= 50 else "low",
                    "reasons": [
                        {
                            "factor": "Niche alignment",
                            "description": f"Creator's {creator['niche']} niche aligns with campaign requirements",
                            "impact": "high" if creator["match_percentage"] >= 75 else "medium"
                        },
                        {
                            "factor": "Engagement rate",
                            "description": f"{creator['engagement_rate']}% engagement rate exceeds industry average of 3.1%",
                            "impact": "high" if creator["engagement_rate"] > 4.0 else "medium"
                        },
                        {
                            "factor": "Audience demographics",
                            "description": "Audience demographics align with campaign target audience",
                            "impact": "medium"
                        }
                    ]
                }
            
            return detailed_creator
            
        except Exception as e:
            logger.error(f"Error fetching creator by ID: {str(e)}")
            return None
    
    async def create_creator(self, db: Session, creator: CreatorCreate) -> Creator:
        """
        Create a new creator
        """
        try:
            # In a real implementation, this would create a new record in the database
            # For MVP, we'll just return a mock with the provided data
            import uuid
            from datetime import datetime
            
            new_creator = {
                "id": str(uuid.uuid4()),
                "name": creator.name,
                "email": creator.email,
                "platform": creator.platform,
                "followers_count": creator.followers_count,
                "followers_count_numeric": creator.followers_count_numeric,
                "engagement_rate": creator.engagement_rate,
                "niche": creator.niche,
                "language": creator.language,
                "country": creator.country,
                "avg_views": creator.avg_views,
                "collaboration_rate": creator.collaboration_rate,
                "profile_image": creator.profile_image,
                "rating": 5.0,
                "match_percentage": 50,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
            
            return new_creator
            
        except Exception as e:
            logger.error(f"Error creating creator: {str(e)}")
            return None
    
    async def update_creator(self, db: Session, creator_id: str, creator: CreatorUpdate) -> Creator:
        """
        Update an existing creator
        """
        try:
            # In a real implementation, this would update the record in the database
            # For MVP, we'll just return a mock with the updated data
            from app.utils.mock_data import MOCK_CREATORS
            from datetime import datetime
            
            # Find creator by ID
            existing_creator = None
            for c in MOCK_CREATORS:
                if c["id"] == creator_id:
                    existing_creator = c
                    break
            
            if not existing_creator:
                return None
            
            # Update fields if provided
            updated_creator = {**existing_creator}
            for field, value in creator.dict(exclude_unset=True).items():
                if value is not None:
                    updated_creator[field] = value
            
            updated_creator["updated_at"] = datetime.utcnow()
            
            return updated_creator
            
        except Exception as e:
            logger.error(f"Error updating creator: {str(e)}")
            return None
    
    async def delete_creator(self, db: Session, creator_id: str) -> bool:
        """
        Delete a creator
        """
        try:
            # In a real implementation, this would delete the record from the database
            # For MVP, we'll just return a success flag
            from app.utils.mock_data import MOCK_CREATORS
            
            # Check if creator exists
            creator_exists = False
            for c in MOCK_CREATORS:
                if c["id"] == creator_id:
                    creator_exists = True
                    break
            
            return creator_exists
            
        except Exception as e:
            logger.error(f"Error deleting creator: {str(e)}")
            return False 