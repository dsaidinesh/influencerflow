import logging
from typing import List, Dict, Any, Optional
import openai
from openai import OpenAI
from app.core.config import settings
from app.models.creator import Creator
from app.models.campaign import Campaign
import json
from app.services.supabase_service import SupabaseService
import numpy as np
from app.schemas.ai_matching import AISimilaritySearchRequest

logger = logging.getLogger(__name__)


class AIService:
    """
    Service for AI-powered functionality, including creator discovery and matching
    """
    
    def __init__(self):
        self.api_key = settings.OPENAI_API_KEY
        if not self.api_key:
            logger.warning("OpenAI API key not found. AI service will use placeholder data.")
            self.use_mock = True
            self.client = None
        else:
            self.use_mock = False
            self.client = OpenAI(api_key=self.api_key)
    
    async def search_creators(self, query: str, budget_range: Optional[List[float]] = None, 
                             target_audience: Optional[str] = None) -> Dict[str, Any]:
        """
        AI-powered creator search based on natural language query
        """
        try:
            if self.use_mock:
                return await self._get_placeholder_search_results(query, budget_range, target_audience)
            
            # Prepare system message context
            system_message = """
            You are an AI assistant that helps find the best influencers for marketing campaigns.
            Based on the user's query, extract key search criteria and provide search insights.
            """
            
            # Prepare user message with query details
            user_message = f"Query: {query}\n"
            if budget_range:
                user_message += f"Budget Range: ${budget_range[0]} to ${budget_range[1]}\n"
            if target_audience:
                user_message += f"Target Audience: {target_audience}\n"
            
            # Call OpenAI API with new client pattern
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            # Extract the response
            ai_analysis = response.choices[0].message.content
            
            # Parse AI analysis to extract search criteria
            # In a real implementation, this would be more sophisticated
            search_insights = {
                "query_interpretation": "Based on your query, I understand you're looking for...",
                "recommended_filters": ["tech", "gadgets", "reviews"],
                "budget_analysis": "Your budget range is suitable for micro to mid-tier influencers"
            }
            
            # Get creators from Supabase and apply filters based on AI insights
            creators = await SupabaseService.get_creators(limit=5)
            
            return {
                "creators": creators,
                "search_insights": search_insights
            }
            
        except Exception as e:
            logger.error(f"Error in AI creator search: {str(e)}")
            return await self._get_placeholder_search_results(query, budget_range, target_audience)
    
    async def analyze_creator_match(self, campaign_id: str, creator_id: str) -> Dict[str, Any]:
        """
        Analyze how well a creator matches a campaign and provide detailed analysis
        """
        try:
            if self.use_mock:
                return self._get_placeholder_match_analysis()
            
            # Fetch campaign and creator details from Supabase
            campaign = await SupabaseService.get_campaign(campaign_id)
            creator = await SupabaseService.get_creator(creator_id)
            
            if not campaign or not creator:
                logger.error(f"Campaign {campaign_id} or creator {creator_id} not found")
                return self._get_placeholder_match_analysis()
            
            # Call OpenAI API for analysis
            system_message = """
            You are an AI assistant specialized in matching influencers to marketing campaigns.
            Analyze how well the influencer matches the campaign based on the provided details.
            Provide a detailed analysis of the match with scores and explanations.
            """
            
            user_message = f"""
            Campaign ID: {campaign_id}
            Creator ID: {creator_id}
            
            Campaign details:
            - Product: {campaign.get('product_name', 'Unknown')}
            - Brand: {campaign.get('brand_name', 'Unknown')}
            - Target audience: {campaign.get('target_audience', 'Unknown')}
            - Campaign goal: {campaign.get('campaign_goal', 'Unknown')}
            
            Creator details:
            - Name: {creator.get('name', 'Unknown')}
            - Platform: {creator.get('platform', 'Unknown')}
            - Followers: {creator.get('followers_count', 'Unknown')}
            - Engagement rate: {creator.get('engagement_rate', 'Unknown')}%
            - Niche: {creator.get('niche', 'Unknown')}
            """
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            # Extract and structure the response
            # This would be more sophisticated in a real implementation
            ai_analysis = response.choices[0].message.content
            
            # For now, return placeholder match analysis
            return self._get_placeholder_match_analysis()
            
        except Exception as e:
            logger.error(f"Error in AI match analysis: {str(e)}")
            return self._get_placeholder_match_analysis()
    
    async def similarity_search(self, request_data: AISimilaritySearchRequest) -> Dict[str, Any]:
        """
        Perform similarity search to find the best influencer matches for a campaign
        based on vector embeddings and specific campaign criteria
        """
        try:
            if self.use_mock:
                return await self._get_placeholder_similarity_results(request_data)
            
            # Generate campaign embedding vector
            campaign_text = f"""
            Product: {request_data.product_name}
            Brand: {request_data.brand}
            Description: {request_data.product_description}
            Target Audience: {request_data.target_audience}
            Use Cases: {', '.join(request_data.key_usecases)}
            Campaign Goal: {request_data.campaign_goal}
            Product Niche: {request_data.product_niche}
            """
            
            # Generate embedding for campaign text
            campaign_embedding = await self._generate_embedding(campaign_text)
            
            if not campaign_embedding:
                logger.error("Failed to generate campaign embedding")
                return await self._get_placeholder_similarity_results(request_data)
            
            # Use the database function to find matching creators
            matched_creators = await SupabaseService.match_creators_by_embedding(
                embedding_vector=campaign_embedding,
                match_threshold=0.5,  # Adjust this threshold as needed
                match_count=20  # Get more results than needed for filtering
            )
            
            # If no creators with embeddings found, return placeholder
            if not matched_creators:
                logger.warning("No matching creators found")
                return await self._get_placeholder_similarity_results(request_data)
            
            # Format results into the expected response format
            matches = []
            for creator in matched_creators:
                # Calculate detailed scores
                overall_score = creator.get('similarity', 0)
                niche_match = min(overall_score * 1.2, 1.0) * 100  # Just an example calculation
                audience_match = min(overall_score * 0.9, 1.0) * 100
                engagement_score = min((creator.get('engagement_rate', 2) / 10) * 100, 100)
                budget_fit = self._calculate_budget_fit(request_data.total_budget, creator.get('collaboration_rate', 0)) * 100
                
                # Format the rates for display
                match_score_str = f"{overall_score * 100:.2f}%"
                niche_match_str = f"{niche_match:.2f}%"
                audience_match_str = f"{audience_match:.2f}%"
                engagement_score_str = f"{engagement_score:.2f}%"
                budget_fit_str = f"{budget_fit:.2f}%"
                
                # Get additional creator details if needed
                creator_details = await SupabaseService.get_creator(creator.get('id'))
                if not creator_details:
                    creator_details = creator
                    
                # Format creator name with handle
                name = creator_details.get('name', creator.get('name', 'Unknown'))
                platform = creator_details.get('platform', creator.get('platform', 'instagram'))
                channel_name = creator_details.get('channel_name', name.lower().replace(' ', '_'))
                influencer_name = f"{name} (@{channel_name})"
                
                # Create match object
                match = {
                    "id": creator.get('id'),
                    "influencer_name": influencer_name,
                    "match_score": match_score_str,
                    "niche": creator.get('niche', 'Unknown'),
                    "followers": creator_details.get('followers_count', creator.get('followers_count', '0')),
                    "engagement": f"{creator_details.get('engagement_rate', creator.get('engagement_rate', 0))}%",
                    "collaboration_rate": f"${creator_details.get('collaboration_rate', 0):.0f}",
                    "detailed_scores": {
                        "niche_match": niche_match_str,
                        "audience_match": audience_match_str,
                        "engagement_score": engagement_score_str,
                        "budget_fit": budget_fit_str
                    }
                }
                matches.append(match)
            
            # Sort matches by score (descending)
            matches.sort(key=lambda x: float(x["match_score"].rstrip('%')), reverse=True)
            
            # Limit to top 10 matches
            matches = matches[:10]
            
            return {
                "matches": matches,
                "total_matches": len(matches),
                "search_parameters": request_data.dict()
            }
        except Exception as e:
            logger.error(f"Error in AI similarity search: {str(e)}")
            return await self._get_placeholder_similarity_results(request_data)
    
    async def _generate_embedding(self, text: str) -> List[float]:
        """Generate an embedding vector for the given text using OpenAI API"""
        try:
            if self.use_mock:
                # Return a random vector of appropriate dimension
                return [0.01] * 1536
                
            response = self.client.embeddings.create(
                model="text-embedding-ada-002",
                input=text
            )
            embedding = response.data[0].embedding
            return embedding
        except Exception as e:
            logger.error(f"Error generating embedding: {str(e)}")
            return None
    
    async def generate_creator_embedding(self, creator_id: str) -> bool:
        """
        Generate and store an embedding vector for a creator
        Returns True if successful, False otherwise
        """
        try:
            # Get creator details
            creator = await SupabaseService.get_creator(creator_id)
            
            if not creator:
                logger.error(f"Creator {creator_id} not found")
                return False
            
            # Create text representation of creator for embedding
            creator_text = f"""
            Name: {creator.get('name', '')}
            Platform: {creator.get('platform', '')}
            Niche: {creator.get('niche', '')}
            About: {creator.get('about', '')}
            Followers: {creator.get('followers_count', '')}
            Engagement Rate: {creator.get('engagement_rate', '')}%
            Country: {creator.get('country', '')}
            Language: {creator.get('language', '')}
            """
            
            # Generate embedding
            embedding = await self._generate_embedding(creator_text)
            
            if not embedding:
                return False
            
            # Update creator with embedding
            success = await SupabaseService.update_creator_embedding(creator_id, embedding)
            
            return success
        except Exception as e:
            logger.error(f"Error generating creator embedding: {str(e)}")
            return False
    
    def _calculate_cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between two vectors"""
        if not vec1 or not vec2:
            return 0.0
        
        # Convert to numpy arrays
        a = np.array(vec1)
        b = np.array(vec2)
        
        # Calculate cosine similarity
        cosine_similarity = np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
        
        return max(0.0, min(cosine_similarity, 1.0))  # Ensure value is between 0 and 1
    
    def _calculate_budget_fit(self, campaign_budget: float, creator_rate: float) -> float:
        """Calculate budget compatibility score"""
        if creator_rate <= 0:
            return 1.0  # Assume perfect fit if rate is not specified
        
        # Simple calculation: is the creator's rate within 20% of campaign budget / 10?
        # Assuming campaign might want to work with around 10 creators
        budget_per_creator = campaign_budget / 10
        
        if creator_rate <= budget_per_creator * 1.2:
            # Creator is within budget or slightly above
            return 1.0
        elif creator_rate <= budget_per_creator * 2:
            # Creator is moderately above budget
            return 0.7
        elif creator_rate <= budget_per_creator * 3:
            # Creator is significantly above budget
            return 0.4
        else:
            # Creator is way above budget
            return 0.2
    
    async def _get_placeholder_search_results(self, query: str, budget_range: Optional[List[float]] = None,
                                target_audience: Optional[str] = None) -> Dict[str, Any]:
        """Get placeholder search results when OpenAI API is not available"""
        try:
            # Get actual creators from Supabase
            creators = await SupabaseService.get_creators(limit=5)
            
            # If no creators found, return empty results
            if not creators:
                creators = []
            
            # Placeholder search insights
            search_insights = {
                "query_interpretation": f"Looking for creators in the requested niche",
                "recommended_filters": ["niche", "platform", "engagement_rate"],
                "budget_analysis": "Budget range suitable for micro to mid-tier influencers" if budget_range else "No budget range specified"
            }
            
            return {
                "creators": creators,
                "search_insights": search_insights
            }
        except Exception as e:
            logger.error(f"Error getting placeholder search results: {e}")
            return {
                "creators": [],
                "search_insights": {
                    "query_interpretation": "Could not process query",
                    "recommended_filters": [],
                    "budget_analysis": "Not available"
                }
            }
    
    def _get_placeholder_match_analysis(self) -> Dict[str, Any]:
        """Get placeholder match analysis when OpenAI API is not available"""
        return {
            "match_percentage": 85,
            "match_status": "high",
            "detailed_analysis": {
                "niche_alignment": {
                    "score": 95,
                    "explanation": "Perfect alignment - both campaign and influencer focus on technology content"
                },
                "audience_match": {
                    "score": 80,
                    "explanation": "Target demographic overlaps significantly with influencer's audience"
                },
                "engagement_quality": {
                    "score": 85,
                    "explanation": "Above-average engagement rate indicates strong audience connection"
                },
                "brand_safety": {
                    "score": 90,
                    "explanation": "Previous collaborations with reputable tech brands show professionalism"
                }
            },
            "recommendation": "Highly recommended for this campaign",
            "estimated_performance": {
                "expected_reach": "400K-450K",
                "expected_engagement": "15K-18K",
                "estimated_roi": "3.2x"
            }
        }
    
    async def _get_placeholder_similarity_results(self, request_data: AISimilaritySearchRequest) -> Dict[str, Any]:
        """Get placeholder similarity search results when OpenAI API is not available"""
        # Sample influencer matches with scores
        sample_matches = [
            {
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
            },
            {
                "id": "550e8400-e29b-41d4-a716-446655440001",
                "influencer_name": "TechGuy (@techguy_reviews)",
                "match_score": "75.42%",
                "niche": "Technology",
                "followers": "220K",
                "engagement": "4.2%",
                "collaboration_rate": "$2500",
                "detailed_scores": {
                    "niche_match": "85.30%",
                    "audience_match": "68.50%",
                    "engagement_score": "72.00%",
                    "budget_fit": "95.00%"
                }
            },
            {
                "id": "550e8400-e29b-41d4-a716-446655440002",
                "influencer_name": "Lifestyle Sarah (@sarahlifestyle)",
                "match_score": "67.88%",
                "niche": "Fashion",
                "followers": "528K",
                "engagement": "3.8%",
                "collaboration_rate": "$4200",
                "detailed_scores": {
                    "niche_match": "62.40%",
                    "audience_match": "78.20%",
                    "engagement_score": "65.00%",
                    "budget_fit": "82.00%"
                }
            }
        ]
        
        return {
            "matches": sample_matches,
            "total_matches": len(sample_matches),
            "search_parameters": request_data.dict()
        }
    
    async def campaign_similarity_search(
        self, 
        campaign_id: str,
        match_threshold: float = 0.5,
        match_count: int = 10
    ) -> Dict[str, Any]:
        """
        Perform similarity search using an existing campaign to find matching creators.
        This uses the campaign details to generate an embedding and find similar creators.
        
        Args:
            campaign_id: ID of the existing campaign to use for matching
            match_threshold: Minimum similarity score (0-1) to include in results
            match_count: Maximum number of creators to return
            
        Returns:
            Dictionary with matched creators and search parameters
        """
        try:
            if self.use_mock:
                return await self._get_placeholder_similarity_results_for_campaign(campaign_id)
            
            # Fetch campaign details
            campaign = await SupabaseService.get_campaign(campaign_id)
            
            if not campaign:
                logger.error(f"Campaign {campaign_id} not found")
                return await self._get_placeholder_similarity_results_for_campaign(campaign_id)
            
            # Generate campaign embedding vector from campaign details
            campaign_text = f"""
            Product: {campaign.get('product_name', '')}
            Brand: {campaign.get('brand_name', '')}
            Description: {campaign.get('product_description', '')}
            Target Audience: {campaign.get('target_audience', '')}
            Campaign Goal: {campaign.get('campaign_goal', '')}
            Product Niche: {campaign.get('product_niche', '')}
            """
            
            # Generate embedding for campaign text
            campaign_embedding = await self._generate_embedding(campaign_text)
            
            if not campaign_embedding:
                logger.error("Failed to generate campaign embedding")
                return await self._get_placeholder_similarity_results_for_campaign(campaign_id)
            
            # Use the database function to find matching creators
            matched_creators = await SupabaseService.match_creators_by_embedding(
                embedding_vector=campaign_embedding,
                match_threshold=match_threshold,
                match_count=match_count
            )
            
            # If no creators with embeddings found, return placeholder
            if not matched_creators:
                logger.warning("No matching creators found")
                return await self._get_placeholder_similarity_results_for_campaign(campaign_id)
            
            # Format results into the expected response format
            matches = []
            for creator in matched_creators:
                # Calculate detailed scores
                overall_score = creator.get('similarity', 0)
                niche_match = min(overall_score * 1.2, 1.0) * 100  # Just an example calculation
                audience_match = min(overall_score * 0.9, 1.0) * 100
                engagement_score = min((creator.get('engagement_rate', 2) / 10) * 100, 100)
                budget_fit = self._calculate_budget_fit(campaign.get('total_budget', 0), creator.get('collaboration_rate', 0)) * 100
                
                # Format the rates for display
                match_score_str = f"{overall_score * 100:.2f}%"
                niche_match_str = f"{niche_match:.2f}%"
                audience_match_str = f"{audience_match:.2f}%"
                engagement_score_str = f"{engagement_score:.2f}%"
                budget_fit_str = f"{budget_fit:.2f}%"
                
                # Get additional creator details if needed
                creator_details = await SupabaseService.get_creator(creator.get('id'))
                if not creator_details:
                    creator_details = creator
                    
                # Format creator name with handle
                name = creator_details.get('name', creator.get('name', 'Unknown'))
                platform = creator_details.get('platform', creator.get('platform', 'instagram'))
                channel_name = creator_details.get('channel_name', name.lower().replace(' ', '_'))
                influencer_name = f"{name} (@{channel_name})"
                
                # Create match object
                match = {
                    "id": creator.get('id'),
                    "influencer_name": influencer_name,
                    "match_score": match_score_str,
                    "niche": creator.get('niche', 'Unknown'),
                    "followers": creator_details.get('followers_count', creator.get('followers_count', '0')),
                    "engagement": f"{creator_details.get('engagement_rate', creator.get('engagement_rate', 0))}%",
                    "collaboration_rate": f"${creator_details.get('collaboration_rate', 0):.0f}",
                    "detailed_scores": {
                        "niche_match": niche_match_str,
                        "audience_match": audience_match_str,
                        "engagement_score": engagement_score_str,
                        "budget_fit": budget_fit_str
                    }
                }
                matches.append(match)
            
            # Sort matches by score (descending)
            matches.sort(key=lambda x: float(x["match_score"].rstrip('%')), reverse=True)
            
            # Limit to top match_count matches
            matches = matches[:match_count]
            
            return {
                "matches": matches,
                "total_matches": len(matches),
                "search_parameters": {
                    "campaign_id": campaign_id,
                    "campaign_name": campaign.get('product_name', 'Unknown Campaign'),
                    "match_threshold": match_threshold,
                    "match_count": match_count
                }
            }
        except Exception as e:
            logger.error(f"Error in campaign similarity search: {str(e)}")
            return await self._get_placeholder_similarity_results_for_campaign(campaign_id)
            
    async def _get_placeholder_similarity_results_for_campaign(self, campaign_id: str) -> Dict[str, Any]:
        """Get placeholder similarity search results for a campaign when API is not available"""
        # Sample influencer matches with scores
        sample_matches = [
            {
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
            },
            {
                "id": "550e8400-e29b-41d4-a716-446655440001",
                "influencer_name": "TechGuy (@techguy_reviews)",
                "match_score": "75.42%",
                "niche": "Technology",
                "followers": "220K",
                "engagement": "4.2%",
                "collaboration_rate": "$2500",
                "detailed_scores": {
                    "niche_match": "85.30%",
                    "audience_match": "68.50%",
                    "engagement_score": "72.00%",
                    "budget_fit": "95.00%"
                }
            },
            {
                "id": "550e8400-e29b-41d4-a716-446655440002",
                "influencer_name": "Lifestyle Sarah (@sarahlifestyle)",
                "match_score": "67.88%",
                "niche": "Fashion",
                "followers": "528K",
                "engagement": "3.8%",
                "collaboration_rate": "$4200",
                "detailed_scores": {
                    "niche_match": "62.40%",
                    "audience_match": "78.20%",
                    "engagement_score": "65.00%",
                    "budget_fit": "82.00%"
                }
            }
        ]
        
        # Get campaign name if available
        campaign_name = "Unknown Campaign"
        try:
            campaign = await SupabaseService.get_campaign(campaign_id)
            if campaign:
                campaign_name = campaign.get('product_name', 'Unknown Campaign')
        except:
            pass
        
        return {
            "matches": sample_matches,
            "total_matches": len(sample_matches),
            "search_parameters": {
                "campaign_id": campaign_id,
                "campaign_name": campaign_name,
                "match_threshold": 0.5,
                "match_count": 10
            }
        } 