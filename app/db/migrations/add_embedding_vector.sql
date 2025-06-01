-- Migration to add embedding_vector column to the creators table
-- This enables AI-powered similarity matching functionality

-- Check if pgvector extension is installed
CREATE EXTENSION IF NOT EXISTS vector;

-- Add the embedding_vector column to the creators table
ALTER TABLE creators ADD COLUMN IF NOT EXISTS embedding_vector VECTOR(1536);

-- Create an index for faster similarity searches
-- Using IVF (Inverted File) index which is more suitable for pgvector
-- The 100 represents the number of lists to create - adjust based on your data size
CREATE INDEX IF NOT EXISTS creators_embedding_vector_idx ON creators 
USING ivfflat (embedding_vector vector_cosine_ops) WITH (lists = 100);

-- Add a trigger to update the updated_at timestamp when the embedding is updated
CREATE OR REPLACE FUNCTION update_modified_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ language 'plpgsql';

DROP TRIGGER IF EXISTS update_creators_modtime ON creators;

CREATE TRIGGER update_creators_modtime
BEFORE UPDATE ON creators
FOR EACH ROW
EXECUTE PROCEDURE update_modified_column(); 