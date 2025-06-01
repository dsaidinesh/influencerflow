from typing import List, Dict, Any, Optional, Union
from app.core.supabase import supabase
from app.schemas import creator as creator_schemas
from app.schemas import campaign as campaign_schemas
from app.schemas import contract as contract_schemas
from app.schemas import outreach as outreach_schemas
from app.schemas import payment as payment_schemas
from uuid import UUID
import logging
import datetime
import uuid

logger = logging.getLogger(__name__)

class SupabaseService:
    """Service for handling database operations with Supabase"""
    
    @staticmethod
    async def get_creators(
        skip: int = 0,
        limit: int = 100,
        platform: Optional[str] = None,
        niche: Optional[str] = None,
        country: Optional[str] = None,
        min_followers: Optional[int] = None,
        max_followers: Optional[int] = None,
        min_engagement: Optional[float] = None
    ) -> List[Dict[str, Any]]:
        """Get creators with optional filtering"""
        try:
            query = supabase.table("creators").select("*")
            
            # Apply filters
            if platform:
                query = query.eq("platform", platform)
            if niche:
                query = query.eq("niche", niche)
            if country:
                query = query.eq("country", country)
            if min_followers:
                query = query.gte("followers_count_numeric", min_followers)
            if max_followers:
                query = query.lte("followers_count_numeric", max_followers)
            if min_engagement:
                query = query.gte("engagement_rate", min_engagement)
            
            # Apply pagination
            response = query.range(skip, skip + limit - 1).execute()
            
            return response.data
        except Exception as e:
            logger.error(f"Error fetching creators from Supabase: {e}")
            return []
    
    @staticmethod
    async def get_creators_with_embeddings(
        skip: int = 0,
        limit: int = 100,
        platform: Optional[str] = None,
        niche: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get creators with their embedding vectors"""
        try:
            query = supabase.table("creators").select("*").not_.is_("embedding_vector", "null")
            
            # Apply filters
            if platform:
                query = query.eq("platform", platform)
            if niche:
                query = query.eq("niche", niche)
            
            # Apply pagination
            response = query.range(skip, skip + limit - 1).execute()
            
            return response.data
        except Exception as e:
            logger.error(f"Error fetching creators with embeddings from Supabase: {e}")
            return []
    
    @staticmethod
    async def get_creator(creator_id: str) -> Optional[Dict[str, Any]]:
        """Get a creator by ID"""
        try:
            response = supabase.table("creators").select("*").eq("id", creator_id).execute()
            if response.data and len(response.data) > 0:
                return response.data[0]
            return None
        except Exception as e:
            logger.error(f"Error fetching creator {creator_id} from Supabase: {e}")
            return None
    
    @staticmethod
    async def create_creator(creator_data: creator_schemas.CreatorCreate) -> Optional[Dict[str, Any]]:
        """Create a new creator"""
        try:
            response = supabase.table("creators").insert(creator_data.model_dump()).execute()
            if response.data and len(response.data) > 0:
                return response.data[0]
            return None
        except Exception as e:
            logger.error(f"Error creating creator in Supabase: {e}")
            return None
    
    @staticmethod
    async def update_creator(creator_id: str, creator_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update a creator"""
        try:
            response = supabase.table("creators").update(creator_data).eq("id", creator_id).execute()
            if response.data and len(response.data) > 0:
                return response.data[0]
            return None
        except Exception as e:
            logger.error(f"Error updating creator {creator_id} in Supabase: {e}")
            return None
    
    @staticmethod
    async def update_creator_embedding(creator_id: str, embedding_vector: List[float]) -> bool:
        """Update a creator's embedding vector"""
        try:
            response = supabase.table("creators").update({
                "embedding_vector": embedding_vector,
                "updated_at": datetime.datetime.utcnow().isoformat()
            }).eq("id", creator_id).execute()
            
            return len(response.data) > 0
        except Exception as e:
            logger.error(f"Error updating embedding for creator {creator_id}: {e}")
            return False
    
    @staticmethod
    async def delete_creator(creator_id: str) -> bool:
        """Delete a creator"""
        try:
            response = supabase.table("creators").delete().eq("id", creator_id).execute()
            return True
        except Exception as e:
            logger.error(f"Error deleting creator {creator_id} from Supabase: {e}")
            return False

    @staticmethod
    async def get_campaigns(
        skip: int = 0,
        limit: int = 100,
        status: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get campaigns with optional filtering"""
        try:
            query = supabase.table("campaigns").select("*")
            
            # Apply filters
            if status:
                query = query.eq("status", status)
            
            # Apply pagination
            response = query.range(skip, skip + limit - 1).execute()
            
            return response.data
        except Exception as e:
            logger.error(f"Error fetching campaigns from Supabase: {e}")
            return []
    
    @staticmethod
    async def get_campaign(campaign_id: str) -> Optional[Dict[str, Any]]:
        """Get a campaign by ID"""
        try:
            response = supabase.table("campaigns").select("*").eq("id", campaign_id).execute()
            if response.data and len(response.data) > 0:
                return response.data[0]
            return None
        except Exception as e:
            logger.error(f"Error fetching campaign {campaign_id} from Supabase: {e}")
            return None
    
    @staticmethod
    async def create_campaign(campaign_data: Union[Dict[str, Any], campaign_schemas.CampaignCreate]) -> Optional[Dict[str, Any]]:
        """Create a new campaign"""
        try:
            # Convert to dict if it's a Pydantic model
            data_dict = campaign_data.model_dump() if hasattr(campaign_data, 'model_dump') else campaign_data
            
            response = supabase.table("campaigns").insert(data_dict).execute()
            if response.data and len(response.data) > 0:
                return response.data[0]
            return None
        except Exception as e:
            logger.error(f"Error creating campaign in Supabase: {e}")
            return None
    
    @staticmethod
    async def update_campaign(campaign_id: str, campaign_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update a campaign"""
        try:
            response = supabase.table("campaigns").update(campaign_data).eq("id", campaign_id).execute()
            if response.data and len(response.data) > 0:
                return response.data[0]
            return None
        except Exception as e:
            logger.error(f"Error updating campaign {campaign_id} in Supabase: {e}")
            return None
    
    @staticmethod
    async def delete_campaign(campaign_id: str) -> bool:
        """Delete a campaign"""
        try:
            response = supabase.table("campaigns").delete().eq("id", campaign_id).execute()
            return True
        except Exception as e:
            logger.error(f"Error deleting campaign {campaign_id} from Supabase: {e}")
            return False

    @staticmethod
    async def get_contracts(
        skip: int = 0,
        limit: int = 100,
        campaign_id: Optional[str] = None,
        creator_id: Optional[str] = None,
        status: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get contracts with optional filtering"""
        try:
            query = supabase.table("contracts").select("*")
            
            # Apply filters
            if campaign_id:
                query = query.eq("campaign_id", campaign_id)
            if creator_id:
                query = query.eq("creator_id", creator_id)
            if status:
                query = query.eq("status", status)
            
            # Apply pagination
            response = query.range(skip, skip + limit - 1).execute()
            
            return response.data
        except Exception as e:
            logger.error(f"Error fetching contracts from Supabase: {e}")
            return []
    
    @staticmethod
    async def get_contract(contract_id: str) -> Optional[Dict[str, Any]]:
        """Get a contract by ID"""
        try:
            response = supabase.table("contracts").select("*").eq("id", contract_id).execute()
            if response.data and len(response.data) > 0:
                return response.data[0]
            return None
        except Exception as e:
            logger.error(f"Error fetching contract {contract_id} from Supabase: {e}")
            return None
    
    @staticmethod
    async def create_contract(contract_data: contract_schemas.ContractCreate) -> Optional[Dict[str, Any]]:
        """Create a new contract"""
        try:
            response = supabase.table("contracts").insert(contract_data.model_dump()).execute()
            if response.data and len(response.data) > 0:
                return response.data[0]
            return None
        except Exception as e:
            logger.error(f"Error creating contract in Supabase: {e}")
            return None
    
    @staticmethod
    async def update_contract(contract_id: str, contract_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update a contract"""
        try:
            response = supabase.table("contracts").update(contract_data).eq("id", contract_id).execute()
            if response.data and len(response.data) > 0:
                return response.data[0]
            return None
        except Exception as e:
            logger.error(f"Error updating contract {contract_id} in Supabase: {e}")
            return None

    @staticmethod
    async def get_outreach_logs(
        skip: int = 0,
        limit: int = 100,
        campaign_id: Optional[str] = None,
        creator_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get outreach logs with optional filtering"""
        try:
            query = supabase.table("outreach_logs").select("*")
            
            # Apply filters
            if campaign_id:
                query = query.eq("campaign_id", campaign_id)
            if creator_id:
                query = query.eq("creator_id", creator_id)
            
            # Apply pagination
            response = query.range(skip, skip + limit - 1).execute()
            
            return response.data
        except Exception as e:
            logger.error(f"Error fetching outreach logs from Supabase: {e}")
            return []
    
    @staticmethod
    async def get_outreach_log(log_id: str) -> Optional[Dict[str, Any]]:
        """Get an outreach log by ID"""
        try:
            response = supabase.table("outreach_logs").select("*").eq("id", log_id).execute()
            if response.data and len(response.data) > 0:
                return response.data[0]
            return None
        except Exception as e:
            logger.error(f"Error fetching outreach log {log_id} from Supabase: {e}")
            return None
    
    @staticmethod
    async def create_outreach_log(log_data: Union[Dict[str, Any], outreach_schemas.OutreachCreate]) -> Optional[Dict[str, Any]]:
        """Create a new outreach log"""
        try:
            # Convert to dict if it's a Pydantic model
            data_dict = log_data.model_dump() if hasattr(log_data, 'model_dump') else log_data
            
            response = supabase.table("outreach_logs").insert(data_dict).execute()
            if response.data and len(response.data) > 0:
                return response.data[0]
            return None
        except Exception as e:
            logger.error(f"Error creating outreach log in Supabase: {e}")
            return None
    
    @staticmethod
    async def update_outreach_log(log_id: str, log_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update an outreach log"""
        try:
            response = supabase.table("outreach_logs").update(log_data).eq("id", log_id).execute()
            if response.data and len(response.data) > 0:
                return response.data[0]
            return None
        except Exception as e:
            logger.error(f"Error updating outreach log {log_id} in Supabase: {e}")
            return None

    @staticmethod
    async def get_payments(
        skip: int = 0,
        limit: int = 100,
        contract_id: Optional[str] = None,
        status: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get payments with optional filtering"""
        try:
            query = supabase.table("payments").select("*")
            
            # Apply filters
            if contract_id:
                query = query.eq("contract_id", contract_id)
            if status:
                query = query.eq("status", status)
            
            # Apply pagination
            response = query.range(skip, skip + limit - 1).execute()
            
            return response.data
        except Exception as e:
            logger.error(f"Error fetching payments from Supabase: {e}")
            return []
    
    @staticmethod
    async def get_payment(payment_id: str) -> Optional[Dict[str, Any]]:
        """Get a payment by ID"""
        try:
            response = supabase.table("payments").select("*").eq("id", payment_id).execute()
            if response.data and len(response.data) > 0:
                return response.data[0]
            return None
        except Exception as e:
            logger.error(f"Error fetching payment {payment_id} from Supabase: {e}")
            return None
    
    @staticmethod
    async def create_payment(payment_data: payment_schemas.PaymentCreate) -> Optional[Dict[str, Any]]:
        """Create a new payment"""
        try:
            response = supabase.table("payments").insert(payment_data.model_dump()).execute()
            if response.data and len(response.data) > 0:
                return response.data[0]
            return None
        except Exception as e:
            logger.error(f"Error creating payment in Supabase: {e}")
            return None
    
    @staticmethod
    async def update_payment(payment_id: str, payment_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update a payment"""
        try:
            response = supabase.table("payments").update(payment_data).eq("id", payment_id).execute()
            if response.data and len(response.data) > 0:
                return response.data[0]
            return None
        except Exception as e:
            logger.error(f"Error updating payment {payment_id} in Supabase: {e}")
            return None
    
    @staticmethod
    async def process_payment(payment_id: str, payment_details: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Process a payment (mock implementation)"""
        try:
            # Update payment status
            payment_data = {
                "status": "processing",
                "transaction_id": f"txn_mock_{uuid.uuid4().hex[:8]}",
                "payment_method": payment_details.get("payment_method", "card"),
                "updated_at": datetime.datetime.utcnow().isoformat()
            }
            
            response = supabase.table("payments").update(payment_data).eq("id", payment_id).execute()
            if response.data and len(response.data) > 0:
                return response.data[0]
            return None
        except Exception as e:
            logger.error(f"Error processing payment {payment_id} in Supabase: {e}")
            return None

    @staticmethod
    async def match_creators_by_embedding(
        embedding_vector: List[float],
        match_threshold: float = 0.5,
        match_count: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Find creators that match the given embedding vector using similarity search
        Uses the database match_creators function that implements vector similarity search
        
        Args:
            embedding_vector: The query embedding vector to match against
            match_threshold: Minimum similarity score (0-1) to include in results
            match_count: Maximum number of results to return
            
        Returns:
            List of creator records with similarity scores
        """
        try:
            # Call the RPC function in the database
            response = supabase.rpc(
                'match_creators',
                {
                    'query_embedding': embedding_vector,
                    'match_threshold': match_threshold,
                    'match_count': match_count
                }
            ).execute()
            
            if not response.data:
                return []
                
            return response.data
        except Exception as e:
            logger.error(f"Error performing similarity search: {e}")
            return []

    @staticmethod
    async def create_outreach_elevenlabs_entry(
        campaign_id: str,
        influencer_id: str,
        conversation_id: str,
        twilio_call_sid: str,
        status: str = "initiated"
    ) -> Dict[str, Any]:
        """Create a new outreach entry for ElevenLabs call"""
        try:
            data = {
                "id": str(uuid.uuid4()),
                "campaign_id": campaign_id,
                "influencer_id": influencer_id,
                "channel": "call",
                "message_type": "outreach",
                "status": status,
                "conversation_id": conversation_id,
                "twilio_call_sid": twilio_call_sid,
                "last_contact_date": datetime.now().isoformat(),
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }
            
            result = supabase.table("outreach_logs").insert(data).execute()
            
            if result.data and len(result.data) > 0:
                return result.data[0]
            
            return None
        except Exception as e:
            logger.error(f"Error creating outreach entry: {str(e)}")
            return None
    
    @staticmethod
    async def get_outreach_by_conversation_id(conversation_id: str) -> Optional[Dict[str, Any]]:
        """Get outreach log by ElevenLabs conversation ID"""
        try:
            result = supabase.table("outreach_logs") \
                .select("*") \
                .eq("conversation_id", conversation_id) \
                .execute()
            
            if result.data and len(result.data) > 0:
                return result.data[0]
            
            return None
        except Exception as e:
            logger.error(f"Error getting outreach by conversation ID: {str(e)}")
            return None
    
    @staticmethod
    async def update_outreach_from_elevenlabs_analysis(
        conversation_id: str,
        analysis: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Update outreach log with ElevenLabs conversation analysis"""
        try:
            # Get the outreach log
            outreach = await SupabaseService.get_outreach_by_conversation_id(conversation_id)
            
            if not outreach:
                logger.warning(f"No outreach log found for conversation ID: {conversation_id}")
                return None
            
            # Prepare update data
            update_data = {
                "status": "completed" if analysis["status"] == "done" else analysis["status"],
                "call_duration_seconds": analysis["metadata"]["duration_seconds"],
                "call_successful": analysis["analysis"]["call_successful"],
                "transcript_summary": analysis["analysis"]["transcript_summary"],
                "full_transcript": analysis["transcript"],
                "updated_at": datetime.now().isoformat()
            }
            
            # Extract evaluation criteria results
            if "evaluation_criteria_results" in analysis["analysis"]:
                eval_results = analysis["analysis"]["evaluation_criteria_results"]
                
                if "collaboration_interest_assessment" in eval_results:
                    update_data["interest_assessment_result"] = eval_results["collaboration_interest_assessment"]["result"]
                    update_data["interest_assessment_rationale"] = eval_results["collaboration_interest_assessment"]["rationale"]
                
                if "professional_communication_quality" in eval_results:
                    update_data["communication_quality_result"] = eval_results["professional_communication_quality"]["result"]
                    update_data["communication_quality_rationale"] = eval_results["professional_communication_quality"]["rationale"]
            
            # Extract data collection results
            if "data_collection_results" in analysis["analysis"]:
                data_results = analysis["analysis"]["data_collection_results"]
                
                if "interest_level" in data_results:
                    update_data["interest_level"] = data_results["interest_level"]["value"]
                
                if "collaboration_rate" in data_results:
                    update_data["collaboration_rate"] = data_results["collaboration_rate"]["value"]
                
                if "preferred_content_types" in data_results:
                    update_data["preferred_content_types"] = data_results["preferred_content_types"]["value"]
                
                if "timeline_availability" in data_results:
                    update_data["timeline_availability"] = data_results["timeline_availability"]["value"]
                
                if "contact_preferences" in data_results:
                    update_data["contact_preferences"] = data_results["contact_preferences"]["value"]
                
                if "audience_demographics" in data_results:
                    update_data["audience_demographics"] = data_results["audience_demographics"]["value"]
                
                if "brand_restrictions" in data_results:
                    update_data["brand_restrictions"] = data_results["brand_restrictions"]["value"]
                
                if "follow_up_actions" in data_results:
                    update_data["follow_up_actions"] = data_results["follow_up_actions"]["value"]
            
            # Determine sentiment based on interest level
            if "interest_level" in update_data:
                interest = update_data["interest_level"]
                if interest == "very_interested":
                    update_data["sentiment"] = "positive"
                elif interest == "interested":
                    update_data["sentiment"] = "neutral_positive"
                elif interest == "neutral":
                    update_data["sentiment"] = "neutral"
                else:
                    update_data["sentiment"] = "neutral_negative"
            
            # Update the record in Supabase
            result = supabase.table("outreach_logs") \
                .update(update_data) \
                .eq("id", outreach["id"]) \
                .execute()
            
            if result.data and len(result.data) > 0:
                return result.data[0]
            
            return None
        except Exception as e:
            logger.error(f"Error updating outreach from ElevenLabs analysis: {str(e)}")
            return None 