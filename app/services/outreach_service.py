import logging
from typing import List, Dict, Any, Optional
from uuid import UUID
from datetime import datetime
from fastapi import HTTPException
from app.services.supabase_service import SupabaseService
from app.schemas import outreach as outreach_schemas
import uuid

logger = logging.getLogger(__name__)


class OutreachService:
    """
    Service for managing outreach-related operations
    """
    
    def __init__(self, db=None):
        self.db = db
    
    @staticmethod
    async def get_outreach_logs(
        skip: int = 0,
        limit: int = 100,
        campaign_id: Optional[str] = None,
        creator_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get all outreach logs with optional filtering
        """
        try:
            return await SupabaseService.get_outreach_logs(
                skip=skip, 
                limit=limit,
                campaign_id=campaign_id,
                creator_id=creator_id
            )
        except Exception as e:
            logger.error(f"Error getting outreach logs: {e}")
            raise HTTPException(status_code=500, detail="Error retrieving outreach logs")
    
    @staticmethod
    async def get_outreach_log(log_id: str) -> Dict[str, Any]:
        """
        Get a single outreach log by ID
        """
        try:
            log = await SupabaseService.get_outreach_log(log_id)
            if not log:
                raise HTTPException(status_code=404, detail=f"Outreach log with ID {log_id} not found")
            return log
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error getting outreach log {log_id}: {e}")
            raise HTTPException(status_code=500, detail=f"Error retrieving outreach log {log_id}")
    
    @staticmethod
    async def create_outreach_log(log_data: outreach_schemas.OutreachCreate) -> Dict[str, Any]:
        """
        Create a new outreach log
        """
        try:
            return await SupabaseService.create_outreach_log(log_data)
        except Exception as e:
            logger.error(f"Error creating outreach log: {e}")
            raise HTTPException(status_code=500, detail="Error creating outreach log")
    
    @staticmethod
    async def update_outreach_log(log_id: str, log_data: outreach_schemas.OutreachUpdate) -> Dict[str, Any]:
        """
        Update an existing outreach log
        """
        try:
            # Check if log exists
            existing_log = await SupabaseService.get_outreach_log(log_id)
            if not existing_log:
                raise HTTPException(status_code=404, detail=f"Outreach log with ID {log_id} not found")
            
            # Update log
            update_data = log_data.model_dump(exclude_unset=True)
            
            updated_log = await SupabaseService.update_outreach_log(log_id, update_data)
            if not updated_log:
                raise HTTPException(status_code=500, detail=f"Failed to update outreach log {log_id}")
            
            return updated_log
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error updating outreach log {log_id}: {e}")
            raise HTTPException(status_code=500, detail=f"Error updating outreach log {log_id}")
    
    @staticmethod
    async def get_outreach_history_by_campaign(campaign_id: str) -> List[Dict[str, Any]]:
        """
        Get all outreach logs for a specific campaign
        """
        try:
            return await SupabaseService.get_outreach_logs(campaign_id=campaign_id, limit=1000)
        except Exception as e:
            logger.error(f"Error getting outreach logs for campaign {campaign_id}: {e}")
            raise HTTPException(status_code=500, detail=f"Error retrieving outreach logs for campaign {campaign_id}")
    
    @staticmethod
    async def get_outreach_history_by_creator(creator_id: str) -> List[Dict[str, Any]]:
        """
        Get all outreach logs for a specific creator
        """
        try:
            return await SupabaseService.get_outreach_logs(creator_id=creator_id, limit=1000)
        except Exception as e:
            logger.error(f"Error getting outreach logs for creator {creator_id}: {e}")
            raise HTTPException(status_code=500, detail=f"Error retrieving outreach logs for creator {creator_id}")
    
    @staticmethod
    async def send_outreach_email(
        campaign_id: str,
        creator_id: str,
        subject: str,
        message: str
    ) -> Dict[str, Any]:
        """
        Send an outreach email to a creator
        This would typically integrate with an email service
        """
        try:
            # Log the outreach attempt
            outreach_data = outreach_schemas.OutreachCreate(
                campaign_id=campaign_id,
                creator_id=creator_id,
                channel="email",
                message_type="outreach",
                content={
                    "subject": subject,
                    "message": message
                },
                status="sent"
            )
            
            log = await OutreachService.create_outreach_log(outreach_data)
            
            # Return success response
            return {
                "id": log["id"],
                "status": "sent",
                "message": "Email sent successfully",
                "timestamp": log["timestamp"]
            }
        except Exception as e:
            logger.error(f"Error sending outreach email: {e}")
            raise HTTPException(status_code=500, detail="Error sending outreach email")
    
    async def get_outreach_dashboard(self, campaign_filter: Optional[str] = None, db=None) -> Dict[str, Any]:
        """
        Get outreach management dashboard
        """
        try:
            # Get all outreach logs with filtering if campaign_filter is provided
            logs = await SupabaseService.get_outreach_logs(
                campaign_id=campaign_filter,
                limit=100
            )
            
            # Calculate summary statistics
            total_contacts = len(logs)
            
            # Count various types of interactions
            calls_completed = sum(1 for log in logs if log.get("channel") == "call" and log.get("status") == "completed")
            email_replies = sum(1 for log in logs if log.get("channel") == "email" and log.get("message_type") == "reply")
            recordings = sum(1 for log in logs if log.get("channel") == "call" and log.get("content", {}).get("recording_url"))
            
            # Format the logs for display with related creator and campaign info
            formatted_logs = []
            for log in logs:
                # Get creator info for each log if available
                creator_info = {}
                if creator_id := log.get("creator_id"):
                    try:
                        creator = await SupabaseService.get_creator(creator_id)
                        if creator:
                            creator_info = {
                                "id": creator.get("id"),
                                "name": creator.get("name"),
                                "platform": creator.get("platform"),
                                "followers_count": creator.get("followers_count")
                            }
                    except Exception as e:
                        logger.warning(f"Error fetching creator info for dashboard: {e}")
                
                # Add to formatted logs
                formatted_logs.append({
                    "id": log.get("id"),
                    "timestamp": log.get("timestamp"),
                    "channel": log.get("channel"),
                    "message_type": log.get("message_type"),
                    "status": log.get("status"),
                    "creator": creator_info,
                    "campaign_id": log.get("campaign_id"),
                    "content_summary": self._summarize_content(log.get("content", {}))
                })
            
            return {
                "summary": {
                    "total_contacts": total_contacts,
                    "calls_completed": calls_completed,
                    "email_replies": email_replies,
                    "recordings": recordings
                },
                "outreach_log": formatted_logs
            }
            
        except Exception as e:
            logger.error(f"Error fetching outreach dashboard: {str(e)}")
            # Return empty dashboard data structure on error
            return {
                "summary": {
                    "total_contacts": 0,
                    "calls_completed": 0,
                    "email_replies": 0,
                    "recordings": 0
                },
                "outreach_log": []
            }
    
    def _summarize_content(self, content: Dict[str, Any]) -> str:
        """Helper method to create a short summary of content for dashboard display"""
        if not content:
            return "No content"
        
        if "subject" in content:
            return f"Email: {content.get('subject', '')}"
        elif "recording_url" in content:
            return "Call recording available"
        elif "message" in content:
            message = content.get("message", "")
            if len(message) > 50:
                return f"{message[:50]}..."
            return message
        
        return "Content available"
    
    async def schedule_call(self, call_data: outreach_schemas.ScheduleCall, db=None) -> Dict[str, Any]:
        """
        Schedule a call with an influencer
        """
        try:
            # TODO: Replace with Supabase implementation
            # For now, return placeholder data
            call_id = str(uuid.uuid4())
            calendar_link = f"https://calendar.example.com/meeting/{call_id}"
            
            return {
                "call_id": call_id,
                "status": "scheduled",
                "calendar_link": calendar_link,
                "reminder_sent": True
            }
            
        except Exception as e:
            logger.error(f"Error scheduling call: {str(e)}")
            return None
    
    async def complete_call(self, call_data: outreach_schemas.CompleteCall, db=None) -> Dict[str, Any]:
        """
        Mark call as completed and upload recording/transcript
        """
        try:
            # TODO: Replace with Supabase implementation
            # For now, return placeholder data
            return {
                "call_id": call_data.call_id,
                "status": call_data.status,
                "transcript_generated": bool(call_data.transcript),
                "follow_up_created": True
            }
            
        except Exception as e:
            logger.error(f"Error completing call: {str(e)}")
            return None
    
    async def get_call_recording(self, call_id: str, db=None) -> Dict[str, Any]:
        """
        Get call recording URL
        """
        try:
            # TODO: Replace with Supabase implementation
            # For now, return placeholder data
            return {
                "recording_url": f"https://example.com/recordings/call_{call_id}.mp3",
                "filename": f"call_{call_id}.mp3"
            }
            
        except Exception as e:
            logger.error(f"Error getting call recording: {str(e)}")
            return None
    
    async def get_call_transcript(self, call_id: str, db=None) -> Dict[str, Any]:
        """
        Get call transcript with summary and action items
        """
        try:
            # TODO: Replace with Supabase implementation
            # For now, return placeholder data
            return {
                "call_id": call_id,
                "transcript": "This is a placeholder transcript.",
                "summary": "Discussion about potential collaboration for the campaign. Influencer expressed interest.",
                "action_items": [
                    "Send product samples",
                    "Draft contract terms",
                    "Schedule follow-up call"
                ],
                "sentiment": "neutral"
            }
            
        except Exception as e:
            logger.error(f"Error getting call transcript: {str(e)}")
            return None
    
    async def create_outreach_entry(
        self,
        campaign_id: str,
        influencer_id: str,
        call_status: str,
        conversation_id: str,
        twilio_call_sid: str
    ) -> Dict[str, Any]:
        """Create a new outreach log entry for a call"""
        try:
            # Use Supabase service to create the entry
            return await SupabaseService.create_outreach_elevenlabs_entry(
                campaign_id=campaign_id,
                influencer_id=influencer_id,
                status=call_status,
                conversation_id=conversation_id,
                twilio_call_sid=twilio_call_sid
            )
        except Exception as e:
            logger.error(f"Error creating outreach entry: {str(e)}")
            return None
    
    async def get_outreach_by_conversation_id(self, conversation_id: str) -> Optional[Dict[str, Any]]:
        """Get an outreach log by its associated conversation ID"""
        try:
            return await SupabaseService.get_outreach_by_conversation_id(conversation_id)
        except Exception as e:
            logger.error(f"Error getting outreach by conversation ID: {str(e)}")
            return None
    
    async def update_from_elevenlabs_analysis(
        self,
        conversation_id: str,
        analysis: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Update outreach log with ElevenLabs conversation analysis"""
        try:
            return await SupabaseService.update_outreach_from_elevenlabs_analysis(
                conversation_id=conversation_id,
                analysis=analysis
            )
        except Exception as e:
            logger.error(f"Error updating outreach from ElevenLabs analysis: {str(e)}")
            return None
    
    async def get_outreach_logs_by_campaign(self, campaign_id: str) -> List[Dict[str, Any]]:
        """Get all outreach logs for a specific campaign"""
        try:
            return await SupabaseService.get_outreach_logs(campaign_id=campaign_id, limit=100)
        except Exception as e:
            logger.error(f"Error getting outreach logs by campaign: {str(e)}")
            return []
    
    async def get_outreach_logs_by_influencer(self, influencer_id: str) -> List[Dict[str, Any]]:
        """Get all outreach logs for a specific influencer"""
        try:
            return await SupabaseService.get_outreach_logs(creator_id=influencer_id, limit=100)
        except Exception as e:
            logger.error(f"Error getting outreach logs by influencer: {str(e)}")
            return []
    
    @staticmethod
    async def create_simple_outreach(data: outreach_schemas.SimpleOutreachCreate) -> Dict[str, Any]:
        """
        Create a new outreach log with just campaign_id and creator_id,
        automatically setting other required fields
        """
        try:
            # Create a standard outreach with default values
            outreach_data = outreach_schemas.OutreachCreate(
                campaign_id=data.campaign_id,
                creator_id=data.creator_id,
                channel="initial",
                message_type="outreach",
                content={},
                status="initialized"
            )
            
            # Convert to dict and add ID
            outreach_dict = outreach_data.model_dump()
            outreach_dict["id"] = str(uuid.uuid4())
            
            # Create the outreach log
            log = await SupabaseService.create_outreach_log(outreach_dict)
            
            if not log:
                raise HTTPException(status_code=500, detail="Failed to create outreach")
            
            # Return just the ID for simplicity
            return {"outreach_id": log["id"]}
            
        except Exception as e:
            logger.error(f"Error creating simple outreach: {e}")
            raise HTTPException(status_code=500, detail="Error creating outreach") 