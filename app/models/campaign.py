from sqlalchemy import Column, String, Float, Integer, DateTime, Enum
from datetime import datetime
import uuid

from app.core.database import Base


class Campaign(Base):
    """Campaign model"""
    
    __tablename__ = "campaigns"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    product_name = Column(String, nullable=False)
    brand_name = Column(String, nullable=False)
    product_description = Column(String, nullable=True)
    target_audience = Column(String, nullable=True)
    key_use_cases = Column(String, nullable=True)
    campaign_goal = Column(String, nullable=True)
    product_niche = Column(String, nullable=True)
    total_budget = Column(Float, nullable=False)
    status = Column(Enum("active", "draft", "completed", "paused", name="campaign_status"), 
                    default="draft", nullable=False)
    influencer_count = Column(Integer, default=0, nullable=False)
    campaign_code = Column(String, unique=True, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Campaign {self.product_name} ({self.status})>" 