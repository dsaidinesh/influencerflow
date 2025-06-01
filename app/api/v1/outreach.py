from fastapi import APIRouter, Depends, HTTPException, Query, Path, status, Response
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session

from app.schemas.outreach import OutreachCreate, OutreachUpdate, SendEmail, OutreachDashboard, InitiateCallRequest, InitiateCallResponse, CallAnalysisResponse, SyncConversationsRequest, SyncConversationsResponse, SimpleOutreachCreate
from app.services.outreach_service import OutreachService
from app.services.elevenlabs_service import ElevenLabsService
from app.services.supabase_service import SupabaseService
from app.core import deps

router = APIRouter()


@router.post("/", response_model=Dict[str, Any])
async def create_outreach_log(
    data: SimpleOutreachCreate,
    outreach_service: OutreachService = Depends()
):
    """
    Create a new outreach log with minimal information.
    Only campaign_id and creator_id are required.
    The status will be automatically set to 'initialized'.
    Returns the outreach_id.
    """
    return await outreach_service.create_simple_outreach(data)


@router.get("/", response_model=List[Dict[str, Any]])
async def get_outreach_logs(
    skip: int = 0,
    limit: int = 100,
    campaign_id: str = None,
    creator_id: str = None,
    outreach_service: OutreachService = Depends()
):
    """
    Get all outreach logs with optional filtering.
    """
    return await outreach_service.get_outreach_logs(
        skip=skip, 
        limit=limit,
        campaign_id=campaign_id,
        creator_id=creator_id
    )


@router.get("/dashboard", response_model=Dict[str, Any])
async def get_outreach_dashboard(
    db: Session = Depends(deps.get_db),
    campaign_filter: str = None,
    outreach_service: OutreachService = Depends()
):
    """
    Get outreach management dashboard with summary statistics.
    """
    return await outreach_service.get_outreach_dashboard(db, campaign_filter)


@router.get("/{log_id}", response_model=Dict[str, Any])
async def get_outreach_log(
    log_id: str,
    outreach_service: OutreachService = Depends()
):
    """
    Get a specific outreach log by ID.
    """
    return await outreach_service.get_outreach_log(log_id)


@router.put("/{log_id}", response_model=Dict[str, Any])
async def update_outreach_log(
    log_id: str,
    log_data: OutreachUpdate,
    outreach_service: OutreachService = Depends()
):
    """
    Update an existing outreach log.
    """
    return await outreach_service.update_outreach_log(log_id, log_data)


@router.post("/email", response_model=Dict[str, Any])
async def send_outreach_email(
    campaign_id: str,
    creator_id: str,
    subject: str,
    message: str,
    outreach_service: OutreachService = Depends()
):
    """
    Send an outreach email to a creator.
    """
    return await outreach_service.send_outreach_email(
        campaign_id=campaign_id,
        creator_id=creator_id,
        subject=subject,
        message=message
    )


@router.get("/campaign/{campaign_id}", response_model=List[Dict[str, Any]])
async def get_outreach_by_campaign(
    campaign_id: str = Path(..., description="The ID of the campaign")
):
    """
    Get all outreach logs for a campaign
    """
    return await OutreachService.get_outreach_history_by_campaign(campaign_id)


@router.get("/creator/{creator_id}", response_model=List[Dict[str, Any]])
async def get_outreach_by_creator(
    creator_id: str = Path(..., description="The ID of the creator")
):
    """
    Get all outreach logs for a creator
    """
    return await OutreachService.get_outreach_history_by_creator(creator_id)


# ElevenLabs integration endpoints
@router.post("/call/initiate", response_model=InitiateCallResponse)
async def initiate_influencer_call(
    request: InitiateCallRequest,
    elevenlabs_service: ElevenLabsService = Depends(),
    outreach_service: OutreachService = Depends()
):
    """Initiate outbound call to influencer via ElevenLabs + Twilio"""
    
    try:
        # Get outreach log
        outreach_log = await outreach_service.get_outreach_log(request.outreach_id)
        if not outreach_log:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Outreach log with ID {request.outreach_id} not found"
            )
            
        # Get campaign and creator data
        campaign = await SupabaseService.get_campaign(outreach_log["campaign_id"])
        creator = await SupabaseService.get_creator(outreach_log["creator_id"])
        
        if not campaign or not creator:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Campaign or creator not found"
            )
        
        # Get phone number from request
        creator_phone = request.phone_number
        if not creator_phone:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Creator phone number required"
            )
        
        # Initiate call via ElevenLabs
        call_result = await elevenlabs_service.initiate_outbound_call(
            creator_phone=creator_phone,
            campaign_data=campaign,
            creator_data=creator
        )
        
        # Update the outreach log with call information
        updated_log = await outreach_service.update_outreach_with_call_info(
            outreach_id=request.outreach_id,
            conversation_id=call_result["conversation_id"],
            twilio_call_sid=call_result.get("callSid", "")
        )
        
        return {
            "success": True,
            "conversation_id": call_result["conversation_id"],
            "outreach_id": request.outreach_id,
            "call_status": "initiated",
            "message": "Call initiated successfully"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to initiate call: {str(e)}"
        )

@router.get("/call/{conversation_id}/analysis", response_model=CallAnalysisResponse)
async def get_call_analysis(
    conversation_id: str,
    elevenlabs_service: ElevenLabsService = Depends()
):
    """Get detailed call analysis from ElevenLabs"""
    
    try:
        analysis = await elevenlabs_service.get_conversation_analysis(conversation_id)
        
        # Process and structure the analysis for frontend
        processed_analysis = {
            "conversation_id": conversation_id,
            "status": analysis.get("status", ""),
            "duration_seconds": analysis.get("metadata", {}).get("call_duration_secs", 0),
            "call_successful": analysis.get("analysis", {}).get("call_successful", False),
            "summary": analysis.get("analysis", {}).get("transcript_summary", ""),
            "evaluation_results": {
                "interest_assessment": analysis.get("analysis", {}).get("evaluation_criteria_results", {}).get("collaboration_interest_assessment", {}),
                "communication_quality": analysis.get("analysis", {}).get("evaluation_criteria_results", {}).get("professional_communication_quality", {}),
                "information_gathering": analysis.get("analysis", {}).get("evaluation_criteria_results", {}).get("information_gathering_success", {}),
                "next_steps": analysis.get("analysis", {}).get("evaluation_criteria_results", {}).get("next_steps_clarity", {})
            },
            "extracted_data": {
                "interest_level": analysis.get("analysis", {}).get("data_collection_results", {}).get("interest_level", {}).get("value", ""),
                "collaboration_rate": analysis.get("analysis", {}).get("data_collection_results", {}).get("collaboration_rate", {}).get("value", ""),
                "content_preferences": analysis.get("analysis", {}).get("data_collection_results", {}).get("preferred_content_types", {}).get("value", ""),
                "timeline": analysis.get("analysis", {}).get("data_collection_results", {}).get("timeline_availability", {}).get("value", ""),
                "contact_info": analysis.get("analysis", {}).get("data_collection_results", {}).get("contact_preferences", {}).get("value", ""),
                "follow_up_actions": analysis.get("analysis", {}).get("data_collection_results", {}).get("follow_up_actions", {}).get("value", "")
            },
            "transcript": analysis.get("transcript", [])
        }
        
        return processed_analysis
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get call analysis: {str(e)}"
        )

@router.post("/sync-conversations", response_model=SyncConversationsResponse)
async def sync_elevenlabs_conversations(
    request: SyncConversationsRequest = None,
    elevenlabs_service: ElevenLabsService = Depends(),
    supabase_service: SupabaseService = Depends()
):
    """Sync recent conversations from ElevenLabs and update outreach logs"""
    
    try:
        limit = 50
        if request and request.limit:
            limit = request.limit
            
        # Get recent conversations
        conversations_response = await elevenlabs_service.list_conversations(
            call_successful="success",
            page_size=limit
        )
        
        conversations = conversations_response.get("conversations", [])
        
        # Debug information
        debug_info = {
            "total_conversations": len(conversations),
            "successful_conversations": len([c for c in conversations if c.get("call_successful") == "success" and c.get("status") == "done"]),
            "conversation_ids": [c.get("conversation_id") for c in conversations if c.get("call_successful") == "success" and c.get("status") == "done"]
        }
        
        print(f"DEBUG - Sync conversations: {debug_info}")
        
        updated_count = 0
        skipped_count = 0
        for conversation in conversations:
            conversation_id = conversation.get("conversation_id")
            
            # Skip if no conversation ID
            if not conversation_id:
                continue
                
            # Only process successful calls
            if conversation.get("call_successful") != "success" or conversation.get("status") != "done":
                continue
            
            # Check if this conversation is already in the database
            existing_record = await SupabaseService.get_outreach_by_conversation_id(conversation_id)
            if not existing_record:
                print(f"DEBUG - No existing outreach record found for conversation_id: {conversation_id}")
                skipped_count += 1
                continue
            
            # Get detailed analysis
            analysis = await elevenlabs_service.get_conversation_analysis(conversation_id)
            
            # Update outreach log with analysis results
            updated = await SupabaseService.update_outreach_from_elevenlabs_analysis(
                conversation_id=conversation_id,
                analysis=analysis
            )
            
            if updated:
                updated_count += 1
                print(f"DEBUG - Successfully updated conversation_id: {conversation_id}")
            else:
                print(f"DEBUG - Failed to update conversation_id: {conversation_id}")
                skipped_count += 1
        
        return {
            "success": True,
            "updated_conversations": updated_count,
            "skipped_conversations": skipped_count,
            "total_found": len(conversations),
            "eligible_conversations": debug_info["successful_conversations"],
            "message": f"Successfully synced {updated_count} conversations, skipped {skipped_count}"
        }
        
    except Exception as e:
        print(f"DEBUG - Error in sync_elevenlabs_conversations: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to sync conversations: {str(e)}"
        )

@router.get("/debug/conversations", response_model=Dict[str, Any])
async def debug_get_conversations(
    elevenlabs_service: ElevenLabsService = Depends()
):
    """Debug endpoint to get raw conversation data from ElevenLabs"""
    try:
        conversations = await elevenlabs_service.list_conversations(
            page_size=10
        )
        return {
            "success": True,
            "data": conversations
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@router.get("/debug/conversation/{conversation_id}", response_model=Dict[str, Any])
async def debug_get_conversation(
    conversation_id: str,
    elevenlabs_service: ElevenLabsService = Depends()
):
    """Debug endpoint to get a specific conversation's details"""
    try:
        conversation = await elevenlabs_service.get_conversation_analysis(conversation_id)
        existing_record = await SupabaseService.get_outreach_by_conversation_id(conversation_id)
        
        return {
            "success": True,
            "has_existing_record": existing_record is not None,
            "existing_record": existing_record,
            "elevenlabs_data": conversation
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@router.get("/call/{conversation_id}/audio")
async def get_call_audio(
    conversation_id: str,
    elevenlabs_service: ElevenLabsService = Depends()
):
    """Get audio recording of a call from ElevenLabs"""
    
    try:
        audio_content = await elevenlabs_service.get_conversation_audio(conversation_id)
        
        return Response(
            content=audio_content,
            media_type="audio/mp3",
            headers={
                "Content-Disposition": f"attachment; filename={conversation_id}.mp3"
            }
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get call audio: {str(e)}"
        ) 