# Database configuration for Supabase PostgreSQL
import os
from supabase import create_client, Client

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Supabase configuration
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_ANON_KEY = os.getenv('SUPABASE_ANON_KEY')
SUPABASE_SERVICE_KEY = os.getenv('SUPABASE_SERVICE_KEY')

def get_supabase_client() -> Client:
    """Get Supabase client instance with service role for admin operations"""
    return create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

# Database table name
VIOLATIONS_TABLE = 'ppe_violations'