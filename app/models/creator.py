from sqlalchemy import Column, String, Float, Integer, DateTime, Enum, Text
from datetime import datetime
import uuid
from sqlalchemy.dialects.postgresql import ARRAY

from app.core.database import Base


class Creator(Base):
    """Creator/Influencer model"""
    
    __tablename__ = "creators"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    platform = Column(Enum("instagram", "youtube", "tiktok", "twitter", name="platform_types"), nullable=False)
    followers_count = Column(String, nullable=False)  # Display format like "125K", "1.2M"
    followers_count_numeric = Column(Integer, nullable=False)  # Actual number for calculations
    engagement_rate = Column(Float, nullable=False)
    niche = Column(Enum("fitness", "technology", "beauty", "food", "travel", "fashion", name="niche_types"), nullable=False)
    language = Column(String, nullable=False)
    country = Column(String, nullable=False)
    about = Column(Text, nullable=True)  # Creator description/bio
    channel_name = Column(String, nullable=True)  # Channel or account name
    avg_views = Column(Integer, nullable=True)
    collaboration_rate = Column(Float, nullable=True)
    rating = Column(Float, nullable=True)
    profile_image = Column(String, nullable=True)
    embedding_vector = Column(ARRAY(Float), nullable=True)  # Vector embedding for similarity matching
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Creator {self.name} ({self.platform})>" 