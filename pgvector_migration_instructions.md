# Setting Up pgvector for AI-Powered Influencer Matching

This document provides step-by-step instructions for setting up pgvector in your Supabase database to enable AI-powered influencer matching using vector similarity search.

## Prerequisites

- Supabase project with database access
- OpenAI API key for generating embeddings
- Python environment with required packages installed

## Step 1: Enable the pgvector Extension in Supabase

1. Log in to your Supabase dashboard
2. Go to the SQL Editor
3. Run the following SQL to enable the pgvector extension:

```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

## Step 2: Apply the Database Migration

You can apply the migration in two ways:

### Option 1: Using the Supabase Dashboard SQL Editor

1. Go to the SQL Editor in your Supabase dashboard
2. Copy and paste the following SQL:

```sql
-- Add the embedding_vector column to the creators table if it doesn't exist
DO $$ 
BEGIN
    IF NOT EXISTS (
        SELECT 1 
        FROM information_schema.columns 
        WHERE table_name = 'creators' AND column_name = 'embedding_vector'
    ) THEN
        ALTER TABLE creators ADD COLUMN embedding_vector vector(1536);
    END IF;
END $$;

-- Create an IVF index for similarity search
DROP INDEX IF EXISTS creators_embedding_vector_idx;
CREATE INDEX creators_embedding_vector_idx ON creators 
USING ivfflat (embedding_vector vector_cosine_ops) WITH (lists = 100);

-- Create a function for vector similarity search
CREATE OR REPLACE FUNCTION match_creators (
  query_embedding vector(1536),
  match_threshold float,
  match_count int
)
RETURNS TABLE (
  id uuid,
  name text,
  platform text,
  followers_count text,
  engagement_rate float,
  niche text,
  similarity float
)
LANGUAGE SQL STABLE
AS $$
  SELECT
    creators.id::uuid,
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
```

3. Click "Run" to execute the SQL

### Option 2: Using the Migration Script

1. Make sure your `.env` file has the correct Supabase credentials:

```
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
OPENAI_API_KEY=your_openai_api_key
```

2. Run the migration script:

```bash
python scripts/apply_pgvector_migration.py
```

## Step 3: Generate Embeddings for Creators

After the migration is applied, you can generate embeddings for your creators:

```bash
python scripts/generate_embeddings.py
```

This script will:
1. Fetch all creators from the database
2. Generate an embedding vector for each creator using OpenAI's text-embedding model
3. Store the embedding in the creator's record

## Step 4: Test the Similarity Search

You can test the AI-powered similarity search with the test script:

```bash
python scripts/test_similarity_search.py
```

This will simulate a campaign search and show the matched creators with their scores.

## Step 5: Using the API Endpoint

The similarity search is now available through the API endpoint:

```
POST /api/v1/ai/similaritysearch
```

Request payload:
```json
{
  "product_name": "Your Product",
  "brand": "Your Brand",
  "product_description": "Product description...",
  "target_audience": "Target audience description...",
  "key_usecases": ["Use case 1", "Use case 2"],
  "campaign_goal": "Campaign goal...",
  "product_niche": "Product niche...",
  "total_budget": 25000
}
```

The response will contain a ranked list of creators with detailed matching scores.

## Troubleshooting

### Error: data type vector has no default operator class for access method "gin"

This error occurs when trying to create a GIN index directly on a vector column. Use the IVF index type instead as shown in the migration SQL.

### Error: relation "creators" does not exist

Make sure you're connected to the correct database and the creators table exists.

### Error: column "embedding_vector" does not exist

This means the migration did not complete successfully. Try running the migration again.

### Error: extension "vector" does not exist

The pgvector extension is not installed. Run `CREATE EXTENSION IF NOT EXISTS vector;` in the SQL Editor. 