from sqlalchemy import Column, String, Float, Integer, DateTime, Enum, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.core.database import Base


class Contract(Base):
    """Contract model"""
    
    __tablename__ = "contracts"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    campaign_id = Column(String, ForeignKey("campaigns.id"), nullable=False)
    creator_id = Column(String, ForeignKey("creators.id"), nullable=False)
    terms = Column(JSON, nullable=True)
    deliverables = Column(JSON, nullable=True)
    payment_amount = Column(Float, nullable=False)
    payment_schedule = Column(JSON, nullable=True)
    status = Column(Enum("draft", "sent", "signed", "completed", name="contract_status"), 
                    default="draft", nullable=False)
    signed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    campaign = relationship("Campaign", backref="contracts")
    creator = relationship("Creator", backref="contracts")
    
    def __repr__(self):
        return f"<Contract {self.id} ({self.status})>" 