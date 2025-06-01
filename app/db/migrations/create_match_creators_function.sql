-- Create a function to match creators against a campaign embedding
-- This allows us to perform vector similarity search through the Supabase API

CREATE OR REPLACE FUNCTION match_creators (
  query_embedding VECTOR(1536),
  match_threshold FLOAT,
  match_count INT
)
RETURNS TABLE (
  id UUID,
  name TEXT,
  platform TEXT,
  followers_count TEXT,
  engagement_rate FLOAT,
  niche TEXT,
  similarity FLOAT
)
LANGUAGE SQL STABLE
AS $$
  SELECT
    creators.id::UUID,
    creators.name,
    creators.platform,
    creators.followers_count,
    creators.engagement_rate,
    creators.niche,
    1 - (creators.embedding_vector <=> query_embedding) AS similarity
  FROM creators
  WHERE 1 - (creators.embedding_vector <=> query_embedding) > match_threshold
    AND creators.embedding_vector IS NOT NULL
  ORDER BY creators.embedding_vector <=> query_embedding
  LIMIT match_count;
$$; 