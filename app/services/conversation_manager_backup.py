"""Conversation manager for handling negotiation conversations.

This service manages conversation state, messages, and provides analytics
for influencer negotiations in the InfluencerFlow platform.
"""

import logging
from datetime import datetime
from enum import Enum
from typing import Dict, List, Any, Optional
import uuid
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MessageRole(str, Enum):
    """Roles for conversation participants."""
    AGENCY = "agency"  # Brand/agency representative
    CREATOR = "creator"  # Influencer/creator
    AI_AGENT = "ai_agent"  # AI negotiation agent
    SYSTEM = "system"  # System messages

class ConversationStatus(str, Enum):
    """Status of the negotiation conversation."""
    INITIALIZED = "initialized"
    NEGOTIATING = "negotiating"
    PAUSED = "paused"
    AGREEMENT_REACHED = "agreement_reached"
    DECLINED = "declined"
    COMPLETED = "completed"

class ConversationManager:
    """Service for managing negotiation conversations."""
    
    def __init__(self):
        # In-memory storage - would be replaced with a database in production
        self.conversations: Dict[str, Dict] = {}
        self.messages: Dict[str, List[Dict]] = {}
        self.deal_history: Dict[str, List[Dict]] = {}
        logger.info("Conversation manager initialized")
    
    def create_conversation(self, campaign_brief: Dict, creator_profile: Dict, 
                           initial_strategy: Dict) -> str:
        """Create a new conversation and return its ID."""
        conversation_id = str(uuid.uuid4())
        
        # Set initial deal parameters
        initial_deal = {
            "price": initial_strategy.get("opening_price", 0),
            "deliverables": campaign_brief.get("deliverables", []),
            "timeline": campaign_brief.get("timeline", "2 weeks"),
            "usage_rights": "6 months",
            "revisions": 2
        }
        
        # Create conversation record
        self.conversations[conversation_id] = {
            "id": conversation_id,
            "campaign_brief": campaign_brief,
            "creator_profile": creator_profile,
            "strategy": initial_strategy,
            "deal_params": initial_deal,
            "status": ConversationStatus.INITIALIZED,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        # Initialize messages list
        self.messages[conversation_id] = []
        
        # Initialize deal history
        self.deal_history[conversation_id] = [{
            "timestamp": datetime.now().isoformat(),
            "deal_params": initial_deal,
            "change_source": "initialization",
            "notes": "Initial deal parameters"
        }]
        
        logger.info(f"Created new conversation: {conversation_id}")
        return conversation_id
    
    def get_conversation(self, conversation_id: str) -> Optional[Dict]:
        """Get conversation by ID."""
        return self.conversations.get(conversation_id)
    
    def update_conversation_status(self, conversation_id: str, status: ConversationStatus, 
                                  reason: str = "") -> bool:
        """Update conversation status."""
        if conversation_id not in self.conversations:
            logger.warning(f"Attempted to update non-existent conversation: {conversation_id}")
            return False
        
        self.conversations[conversation_id]["status"] = status
        self.conversations[conversation_id]["updated_at"] = datetime.now().isoformat()
        
        # Add system message about status change
        self.add_message(
            conversation_id,
            MessageRole.SYSTEM,
            f"Conversation status changed to {status}",
            {"reason": reason}
        )
        
        logger.info(f"Updated conversation {conversation_id} status to {status}")
        return True
    
    def add_message(self, conversation_id: str, role: MessageRole, content: str, 
                   metadata: Optional[Dict] = None) -> bool:
        """Add message to conversation."""
        if conversation_id not in self.conversations:
            logger.warning(f"Attempted to add message to non-existent conversation: {conversation_id}")
            return False
        
        message = {
            "id": str(uuid.uuid4()),
            "conversation_id": conversation_id,
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {}
        }
        
        if conversation_id not in self.messages:
            self.messages[conversation_id] = []
            
        self.messages[conversation_id].append(message)
        self.conversations[conversation_id]["updated_at"] = datetime.now().isoformat()
        
        logger.info(f"Added {role} message to conversation {conversation_id}")
        return True
    
    def get_messages(self, conversation_id: str) -> List[Dict]:
        """Get all messages for a conversation."""
        return self.messages.get(conversation_id, [])
    
    def update_deal_parameters(self, conversation_id: str, deal_params: Dict, 
                              rationale: str) -> bool:
        """Update deal parameters with historical tracking."""
        if conversation_id not in self.conversations:
            logger.warning(f"Attempted to update non-existent conversation: {conversation_id}")
            return False
        
        # Get current deal parameters
        current_deal = self.conversations[conversation_id]["deal_params"]
        
        # Create a merged deal (with current values for any missing keys)
        updated_deal = {**current_deal, **deal_params}
        
        # Update conversation with new parameters
        self.conversations[conversation_id]["deal_params"] = updated_deal
        self.conversations[conversation_id]["updated_at"] = datetime.now().isoformat()
        
        # Add to deal history
        if conversation_id not in self.deal_history:
            self.deal_history[conversation_id] = []
            
        self.deal_history[conversation_id].append({
            "timestamp": datetime.now().isoformat(),
            "deal_params": updated_deal,
            "previous_params": current_deal,
            "changes": {k: v for k, v in deal_params.items() if k in current_deal and current_deal[k] != v},
            "rationale": rationale
        })
        
        logger.info(f"Updated deal parameters for conversation {conversation_id}")
        return True
    
    def get_conversation_summary(self, conversation_id: str) -> Optional[Dict]:
        """Get a summary of the conversation status and deal parameters."""
        if conversation_id not in self.conversations:
            logger.warning(f"Attempted to get summary for non-existent conversation: {conversation_id}")
            return None
        
        conversation = self.conversations[conversation_id]
        messages = self.get_messages(conversation_id)
        deal_history = self.deal_history.get(conversation_id, [])
        
        # Calculate negotiation progress
        initial_price = deal_history[0]["deal_params"]["price"] if deal_history else 0
        current_price = conversation["deal_params"]["price"]
        creator_rate = conversation["creator_profile"].get("typical_rate", 0)
        
        # Simplified progress calculation
        progress = 0
        if creator_rate > 0 and initial_price > 0:
            # Progress based on how close the current price is to creator's typical rate
            price_ratio = current_price / creator_rate
            if price_ratio >= 0.95:  # Very close to typical rate
                progress = 95
            elif price_ratio >= 0.9:
                progress = 90
            elif price_ratio >= 0.85:
                progress = 80
            elif price_ratio >= 0.8:
                progress = 70
            else:
                progress = 60
        
        # If status is agreement reached, set progress to 100
        if conversation["status"] == ConversationStatus.AGREEMENT_REACHED:
            progress = 100
        
        return {
            "conversation_id": conversation_id,
            "status": conversation["status"],
            "message_count": len(messages),
            "deal_summary": {
                "creator_typical_rate": creator_rate,
                "initial_offer": initial_price,
                "current_offer": current_price,
                "negotiation_progress": progress,
                "price_changes": len(deal_history) - 1,
                "total_price_changes": sum(1 for d in deal_history if "changes" in d and "price" in d["changes"]),
                "timeline": conversation["deal_params"]["timeline"],
                "deliverables": conversation["deal_params"].get("deliverables", [])
            },
            "last_updated": conversation["updated_at"]
        }
    
    def get_negotiation_insights(self, conversation_id: str) -> List[str]:
        """Get insights from the negotiation process."""
        if conversation_id not in self.conversations:
            logger.warning(f"Attempted to get insights for non-existent conversation: {conversation_id}")
            return []
        
        # Extract insights from AI agent messages
        insights = []
        for message in self.get_messages(conversation_id):
            if message["role"] == MessageRole.AI_AGENT and "metadata" in message:
                metadata = message["metadata"]
                if "insights" in metadata and isinstance(metadata["insights"], list):
                    insights.extend(metadata["insights"])
        
        # Return unique insights (no duplicates)
        return list(set(insights))

# Create a singleton instance
conversation_manager = ConversationManager()