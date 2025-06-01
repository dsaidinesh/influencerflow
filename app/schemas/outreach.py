from pydantic import BaseModel, Field, ConfigDict, UUID4
from typing import Optional, Literal, Dict, List, Any
from uuid import UUID
from datetime import datetime


# Schema for outreach dashboard overview
class OutreachDashboard(BaseModel):
    summary: Dict[str, int]
    outreach_log: List[Dict[str, Any]]


# Schema for creating a new outreach log
class OutreachCreate(BaseModel):
    campaign_id: str
    creator_id: str
    channel: str
    message_type: str
    content: Dict[str, Any]
    status: str


# Schema for simplified outreach creation (only needs campaign_id and creator_id)
class SimpleOutreachCreate(BaseModel):
    campaign_id: str
    creator_id: str


# Schema for updating an existing outreach log
class OutreachUpdate(BaseModel):
    channel: Optional[str] = None
    message_type: Optional[str] = None
    content: Optional[Dict[str, Any]] = None
    status: Optional[str] = None
    notes: Optional[str] = None
    last_contact_date: Optional[datetime] = None
    sentiment: Optional[str] = None


# Schema for sending an email
class SendEmail(BaseModel):
    campaign_id: str
    creator_id: str
    subject: str
    message: str


# Schema for scheduling a call
class ScheduleCall(BaseModel):
    campaign_id: str
    creator_id: str
    scheduled_time: datetime
    notes: Optional[str] = None


# Schema for schedule call response
class ScheduleCallResponse(BaseModel):
    call_id: UUID
    status: str
    calendar_link: str
    reminder_sent: bool


# Schema for completing a call
class CompleteCall(BaseModel):
    outreach_id: str
    call_status: str
    call_duration_minutes: Optional[int] = None
    call_recording_url: Optional[str] = None
    call_transcript: Optional[str] = None
    notes: Optional[str] = None
    next_steps: Optional[str] = None
    sentiment: Optional[str] = None


# Schema for complete call response
class CompleteCallResponse(BaseModel):
    call_id: UUID
    status: str
    transcript_generated: bool
    follow_up_created: bool


# Schema for call transcript
class CallTranscript(BaseModel):
    call_id: UUID
    transcript: str
    summary: str
    action_items: List[str]
    sentiment: str


# ElevenLabs-specific request models
class InitiateCallRequest(BaseModel):
    """Request model for initiating an outbound call via ElevenLabs"""
    campaign_id: str
    creator_id: str
    phone_number: str


class SyncConversationsRequest(BaseModel):
    from_date: Optional[datetime] = None
    limit: Optional[int] = Field(30, ge=1, le=100)


# Response models
class OutreachLogBase(BaseModel):
    id: str
    campaign_id: str
    influencer_id: str
    channel: str
    message_type: str
    status: str
    content: Optional[Dict[str, Any]] = None
    last_contact_date: Optional[datetime] = None
    notes: Optional[str] = None
    sentiment: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class OutreachLogCreate(OutreachLogBase):
    pass


class OutreachLogUpdate(BaseModel):
    channel: Optional[str] = None
    message_type: Optional[str] = None
    status: Optional[str] = None
    content: Optional[Dict[str, Any]] = None
    last_contact_date: Optional[datetime] = None
    notes: Optional[str] = None
    sentiment: Optional[str] = None


class CallAnalysisResponse(BaseModel):
    conversation_id: str
    status: str
    duration_seconds: Optional[int] = None
    call_successful: Optional[str] = None
    summary: Optional[str] = None
    evaluation_results: Optional[Dict[str, Any]] = None
    extracted_data: Optional[Dict[str, Any]] = None
    transcript: Optional[List[Dict[str, Any]]] = None


class InitiateCallResponse(BaseModel):
    success: bool
    conversation_id: Optional[str] = None
    outreach_id: Optional[str] = None
    call_status: str
    message: str


class SyncConversationsResponse(BaseModel):
    success: bool
    updated_conversations: int
    skipped_conversations: Optional[int] = None
    total_found: Optional[int] = None
    eligible_conversations: Optional[int] = None
    message: str


# Legacy schemas
class ScheduleCall(BaseModel):
    campaign_id: str
    creator_id: str
    scheduled_time: datetime
    notes: Optional[str] = None


class CompleteCall(BaseModel):
    outreach_id: str
    call_status: str
    call_duration_minutes: Optional[int] = None
    call_recording_url: Optional[str] = None
    call_transcript: Optional[str] = None
    notes: Optional[str] = None
    next_steps: Optional[str] = None
    sentiment: Optional[str] = None 