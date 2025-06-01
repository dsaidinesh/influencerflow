from sqlalchemy import Column, String, DateTime, Integer, Text, JSON, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid

class OutreachLog:
    """Outreach Log model for tracking communication with influencers"""
    
    __tablename__ = "outreach_logs"
    
    id = str(uuid.uuid4())
    campaign_id = None
    influencer_id = None
    
    # Basic outreach info
    channel = "call"  # call, email, message
    message_type = "outreach"  # outreach, follow_up, reply
    status = None  # initiated, in-progress, completed, failed, no_answer
    
    # Call tracking for ElevenLabs integration
    conversation_id = None  # ElevenLabs conversation ID
    twilio_call_sid = None  # Twilio call SID
    call_duration_seconds = None
    
    # ElevenLabs analysis results
    call_successful = None  # success, failure, unknown
    transcript_summary = None
    full_transcript = None
    
    # Evaluation criteria results
    interest_assessment_result = None
    interest_assessment_rationale = None
    communication_quality_result = None
    communication_quality_rationale = None
    
    # Extracted data
    interest_level = None  # very_interested, interested, neutral, not_interested
    collaboration_rate = None
    preferred_content_types = None
    timeline_availability = None
    contact_preferences = None
    audience_demographics = None
    brand_restrictions = None
    follow_up_actions = None
    
    # General outreach content
    content = None  # For email content, call details, etc.
    
    # Standard tracking
    email_status = None
    last_contact_date = None
    notes = None
    sentiment = None
    created_at = None
    updated_at = None
    
    def __repr__(self):
        return f"<OutreachLog {self.id} {self.status}>" 