from supabase import create_client, Client
from dotenv import load_dotenv
import os

# Load .env file if exists
load_dotenv()

# Read environment variables
url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")

# Validate before connecting
if not url or not key:
    raise ValueError("❌ Missing SUPABASE_URL or SUPABASE_KEY in environment variables")

# Create Supabase client
supabase: Client = create_client(url, key)

print("Connected to Supabase ✅")
print("URL:", url)