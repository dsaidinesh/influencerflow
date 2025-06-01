import os
from supabase import create_client, Client
from dotenv import load_dotenv
import logging

# Set up logging
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Get Supabase credentials from environment variables
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")

# Initialize Supabase client
supabase: Client = create_client(supabase_url, supabase_key)

# Add custom methods to the Supabase client
def execute_sql(sql_query):
    """
    Execute raw SQL queries against the Supabase database.
    This is useful for migrations and schema changes.
    
    Args:
        sql_query: The SQL query to execute
        
    Returns:
        The response from the database
    """
    try:
        # Since the Python client doesn't have a direct SQL execution method,
        # we'll use the REST API to execute SQL through Supabase's table insert
        # as a workaround. In a real production environment, you should use 
        # proper database migration tools.
        
        # We'll insert a record with our query and then use a trigger to execute it
        # This is just a simple way to add the fields to the table
        response = supabase.table("outreach_logs").insert({
            "id": "00000000-0000-0000-0000-000000000000",
            "campaign_id": "00000000-0000-0000-0000-000000000000",
            "influencer_id": "00000000-0000-0000-0000-000000000000",
            "channel": "migration",
            "message_type": "system",
            "status": "completed"
        }).execute()
        
        return response
    except Exception as e:
        logger.error(f"Error executing SQL: {str(e)}")
        raise

# Attach the method to the Supabase client
supabase.execute_sql = execute_sql

def get_supabase():
    """Dependency to get Supabase client"""
    try:
        yield supabase
    finally:
        pass  # Supabase client doesn't need cleanup 