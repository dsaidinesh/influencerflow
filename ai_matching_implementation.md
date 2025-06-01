# AI-Powered Influencer Matching Implementation Guide

This document outlines the implementation details for adding AI-powered influencer matching to the InfluencerFlow platform.

## Overview

The AI matching system uses vector embeddings to compute similarity between campaign details and influencer profiles. This enables intelligent, AI-driven influencer discovery based on semantic similarity rather than just keyword matching.

## Database Changes

### 1. Enable pgvector Extension

First, enable the pgvector extension in your Supabase project:

```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

### 2. Add Embedding Column to Creators Table

Add the embedding vector column to store AI embeddings:

```sql
ALTER TABLE creators ADD COLUMN embedding_vector vector(1536);
```

### 3. Create Match Scores Table

Create a new table to store match scores between campaigns and creators:

```sql
CREATE TABLE match_scores (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  campaign_id UUID NOT NULL REFERENCES campaigns(id) ON DELETE CASCADE,
  creator_id UUID NOT NULL REFERENCES creators(id) ON DELETE CASCADE,
  match_score FLOAT NOT NULL,
  niche_match FLOAT NOT NULL,
  audience_match FLOAT NOT NULL,
  engagement_score FLOAT NOT NULL,
  budget_fit FLOAT NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  UNIQUE(campaign_id, creator_id)
);

-- Index for faster lookups
CREATE INDEX idx_match_scores_campaign_id ON match_scores(campaign_id);
CREATE INDEX idx_match_scores_creator_id ON match_scores(creator_id);
CREATE INDEX idx_match_scores_match_score ON match_scores(match_score);
```

### 4. Create Index on Embedding Vector

Create an index on the embedding vector for faster similarity searches:

```sql
CREATE INDEX idx_creators_embedding_vector ON creators USING ivfflat (embedding_vector vector_cosine_ops);
```

## Backend Implementation

### 1. Generate Embeddings for Creators

When a new creator is added or updated, generate an embedding vector based on their profile information:

```python
def generate_creator_embedding(creator_id):
    # Fetch creator data
    creator = db.query(Creator).filter(Creator.id == creator_id).first()
    if not creator:
        raise ValueError(f"Creator with ID {creator_id} not found")
    
    # Create text for embedding
    embedding_text = f"""
    Name: {creator.name}
    Platform: {creator.platform}
    Niche: {creator.niche}
    Bio: {creator.about or ''}
    Channel: {creator.channel_name or ''}
    Followers: {creator.followers_count_numeric}
    Engagement: {creator.engagement_rate}
    Country: {creator.country}
    Language: {creator.language}
    """
    
    # Generate embedding using OpenAI
    response = openai.Embedding.create(
        model="text-embedding-3-small",
        input=embedding_text.strip()
    )
    
    # Extract the embedding vector
    embedding_vector = response.data[0].embedding
    
    # Store the embedding vector in the database
    creator.embedding_vector = embedding_vector
    db.commit()
    
    return {
        "creator_id": creator_id,
        "embedding_updated": True,
        "embedding_dimensions": len(embedding_vector)
    }
```

### 2. Implement AI Similarity Search Endpoint

Create the main endpoint for AI-powered influencer matching:

```python
@router.post("/api/ai/similaritysearch")
def similarity_search(request: SimilaritySearchRequest, db: Session = Depends(get_db)):
    # Generate embedding for the campaign description
    campaign_text = f"""
    Product: {request.product_name}
    Brand: {request.brand_name}
    Description: {request.product_description or ''}
    Target Audience: {request.target_audience or ''}
    Key Use Cases: {', '.join(request.key_use_cases) if request.key_use_cases else ''}
    Campaign Goal: {request.campaign_goal or ''}
    Product Niche: {request.product_niche or ''}
    """
    
    campaign_embedding = openai.Embedding.create(
        model="text-embedding-3-small",
        input=campaign_text.strip()
    ).data[0].embedding
    
    # Build query constraints
    query_filters = []
    if request.min_followers:
        query_filters.append(f"followers_count_numeric >= {request.min_followers}")
    if request.max_followers:
        query_filters.append(f"followers_count_numeric <= {request.max_followers}")
    if request.min_engagement:
        query_filters.append(f"engagement_rate >= {request.min_engagement}")
    
    filters = " AND ".join(query_filters)
    where_clause = f"WHERE {filters}" if filters else ""
    
    # Query for similar creators using vector similarity
    query = f"""
    SELECT 
        id,
        name,
        platform,
        niche,
        followers_count,
        followers_count_numeric,
        engagement_rate,
        collaboration_rate,
        profile_image,
        1 - (embedding_vector <=> $1) as similarity_score
    FROM 
        creators
    {where_clause}
    ORDER BY 
        similarity_score DESC
    LIMIT {request.limit or 20}
    """
    
    # Execute the query
    results = db.execute(query, [campaign_embedding]).fetchall()
    
    # Calculate detailed scores
    matches = []
    for result in results:
        # Convert similarity score (0-1) to percentage
        match_score = result.similarity_score * 100
        
        # Calculate sub-scores
        niche_match = calculate_niche_match(request.product_niche, result.niche)
        audience_match = calculate_audience_match(request.target_audience, result)
        engagement_score = calculate_engagement_score(result.engagement_rate)
        budget_fit = calculate_budget_fit(request.total_budget, result.collaboration_rate)
        
        # Format output
        matches.append({
            "id": result.id,
            "influencer_name": f"{result.name} (@{result.platform})",
            "profile_image": result.profile_image,
            "platform": result.platform,
            "match_score": f"{match_score:.2f}%",
            "niche": result.niche,
            "followers": result.followers_count,
            "followers_count_numeric": result.followers_count_numeric,
            "engagement": f"{result.engagement_rate:.1f}%",
            "collaboration_rate": f"${result.collaboration_rate:.0f}",
            "detailed_scores": {
                "niche_match": f"{niche_match:.2f}%",
                "audience_match": f"{audience_match:.2f}%",
                "engagement_score": f"{engagement_score:.2f}%",
                "budget_fit": f"{budget_fit:.2f}%"
            }
        })
    
    return {
        "matches": matches,
        "total": len(matches),
        "page": 1,
        "pages": 1
    }
```

### 3. Implement Score Calculation Functions

Implement the utility functions for calculating detailed scores:

```python
def calculate_niche_match(campaign_niche, creator_niche):
    """Calculate niche match score based on similarity between campaign and creator niches"""
    if not campaign_niche:
        return 75.0  # Default score if no campaign niche specified
    
    # Basic exact match
    if campaign_niche.lower() == creator_niche.lower():
        return 100.0
    
    # Define niche relationships (could be expanded with ML-based similarity)
    niche_compatibility = {
        "fitness": {"health": 90, "sports": 85, "nutrition": 80},
        "technology": {"gadgets": 90, "gaming": 80, "software": 85},
        "beauty": {"fashion": 85, "cosmetics": 95, "lifestyle": 75},
        "food": {"cooking": 95, "nutrition": 85, "lifestyle": 70},
        "travel": {"lifestyle": 80, "adventure": 90, "photography": 75},
        "fashion": {"beauty": 85, "lifestyle": 80, "luxury": 75}
    }
    
    # Get compatibility score from the mapping
    campaign_niche_lower = campaign_niche.lower()
    creator_niche_lower = creator_niche.lower()
    
    if campaign_niche_lower in niche_compatibility and creator_niche_lower in niche_compatibility[campaign_niche_lower]:
        return float(niche_compatibility[campaign_niche_lower][creator_niche_lower])
    
    # Default compatibility score
    return 40.0

def calculate_audience_match(target_audience, creator):
    """Calculate audience match score based on target audience and creator's followers"""
    if not target_audience:
        return 50.0  # Default score if no target audience specified
    
    # This would ideally use NLP or demographic data about the creator's audience
    # For now, use a placeholder score
    base_score = 43.0
    
    # Adjust based on available creator metrics
    if creator.engagement_rate > 5.0:
        base_score += 10.0
    if creator.followers_count_numeric > 100000:
        base_score += 5.0
    
    return min(100.0, base_score)

def calculate_engagement_score(engagement_rate):
    """Calculate engagement score based on engagement rate"""
    if engagement_rate >= 10.0:
        return 100.0
    if engagement_rate >= 7.0:
        return 90.0
    if engagement_rate >= 5.0:
        return 80.0
    if engagement_rate >= 3.0:
        return 70.0
    if engagement_rate >= 2.0:
        return 60.0
    if engagement_rate >= 1.0:
        return 50.0
    
    return 40.0

def calculate_budget_fit(total_budget, collaboration_rate):
    """Calculate budget fit based on campaign budget and creator's rate"""
    if not total_budget or not collaboration_rate:
        return 50.0  # Default score if either value is missing
    
    # Ideal creator count for campaign (assuming ~10 creators)
    budget_per_creator = total_budget / 10
    
    # Calculate how well the creator's rate fits within the budget
    ratio = budget_per_creator / collaboration_rate
    
    if ratio >= 1.5:
        return 100.0  # Creator is well within budget
    if ratio >= 1.0:
        return 90.0   # Creator fits perfectly in budget
    if ratio >= 0.8:
        return 80.0   # Creator is slightly above budget
    if ratio >= 0.6:
        return 60.0   # Creator is moderately above budget
    if ratio >= 0.4:
        return 40.0   # Creator is significantly above budget
    
    return 20.0       # Creator is way above budget
```

### 4. Create Pydantic Models

Define the data models for request and response:

```python
from pydantic import BaseModel, Field
from typing import List, Optional

class SimilaritySearchRequest(BaseModel):
    product_name: str
    brand_name: str
    product_description: Optional[str] = None
    target_audience: Optional[str] = None
    key_use_cases: Optional[List[str]] = None
    campaign_goal: Optional[str] = None
    product_niche: Optional[str] = None
    total_budget: float
    min_followers: Optional[int] = None
    max_followers: Optional[int] = None
    min_engagement: Optional[float] = None
    limit: Optional[int] = 20

class DetailedScores(BaseModel):
    niche_match: str
    audience_match: str
    engagement_score: str
    budget_fit: str

class MatchResult(BaseModel):
    id: str
    influencer_name: str
    profile_image: Optional[str] = None
    platform: str
    match_score: str
    niche: str
    followers: str
    followers_count_numeric: int
    engagement: str
    collaboration_rate: str
    detailed_scores: DetailedScores

class SimilaritySearchResponse(BaseModel):
    matches: List[MatchResult]
    total: int
    page: int
    pages: int
```

## Automatic Embedding Generation

### 1. Add Trigger for New Creators

Create a database trigger to automatically queue embedding generation for new creators:

```sql
CREATE OR REPLACE FUNCTION trigger_creator_embedding_generation()
RETURNS TRIGGER AS $$
BEGIN
    -- Insert a task into a queue table or call a function directly
    PERFORM pg_notify('creator_embedding_needed', NEW.id::text);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER creator_embedding_trigger
AFTER INSERT OR UPDATE ON creators
FOR EACH ROW
EXECUTE FUNCTION trigger_creator_embedding_generation();
```

### 2. Background Worker for Processing Embeddings

Implement a background worker to listen for notifications and generate embeddings:

```python
import psycopg2
import select
import time
from contextlib import contextmanager

@contextmanager
def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    try:
        yield conn
    finally:
        conn.close()

def embedding_worker():
    with get_db_connection() as conn:
        conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        cursor.execute("LISTEN creator_embedding_needed;")
        
        print("Embedding worker started, waiting for notifications...")
        
        while True:
            if select.select([conn], [], [], 5) == ([], [], []):
                # Timeout, do any periodic tasks here
                pass
            else:
                conn.poll()
                while conn.notifies:
                    notify = conn.notifies.pop()
                    creator_id = notify.payload
                    print(f"Received embedding generation request for creator: {creator_id}")
                    
                    try:
                        # Call the embedding generation function
                        generate_creator_embedding(creator_id)
                        print(f"Successfully generated embedding for creator: {creator_id}")
                    except Exception as e:
                        print(f"Error generating embedding for creator {creator_id}: {str(e)}")

# Start the worker
if __name__ == "__main__":
    embedding_worker()
```

## Integration Steps

1. **Database Setup**:
   - Enable pgvector extension
   - Add embedding_vector column to creators table
   - Create match_scores table
   - Create necessary indexes

2. **Backend Implementation**:
   - Implement embedding generation for creators
   - Create AI similarity search endpoint
   - Implement match score calculation functions
   - Set up background worker for automatic embedding generation

3. **Frontend Integration**:
   - Add a new "AI Match" section to campaign details page
   - Create an interface for configuring and running AI matching
   - Display match results with detailed scores

4. **Testing**:
   - Verify embedding generation for existing creators
   - Test similarity search with various campaign parameters
   - Measure response times and optimize if needed

## Performance Considerations

1. **Batch Processing**: Generate embeddings in batches for existing creators.
2. **Caching**: Cache match results for campaigns that don't change frequently.
3. **Index Optimization**: Tune the vector index parameters based on your dataset size.
4. **Pagination**: Implement proper pagination for large result sets.

## Monitoring and Maintenance

1. **Monitor Embedding Generation**: Track success rates of embedding generation.
2. **API Usage**: Monitor OpenAI API usage to manage costs.
3. **User Feedback**: Collect feedback on match quality to improve the system.
4. **Model Updates**: Periodically update the embedding model as newer versions become available. 