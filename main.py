from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from db_client import supabase
from openai import OpenAI
import os
from dotenv import load_dotenv

# =====================================================
# LOAD ENVIRONMENT VARIABLES
# =====================================================
load_dotenv()

# Verify environment variable (log to Render console)
openai_key = os.getenv("OPENAI_API_KEY")
if not openai_key:
    print("❌ OPENAI_API_KEY not found in environment!")
else:
    print("✅ OPENAI_API_KEY detected successfully.")

# =====================================================
# APP INIT
# =====================================================
app = FastAPI(title="AI Learning Backend")

# =====================================================
# CORS CONFIG (allow frontend on Vercel)
# =====================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://ai-learning-website-zeta.vercel.app",  # Frontend URL
        "https://ai-learning-website-one.vercel.app",   # Optional: your other frontend
        "http://localhost:3000"                         # Local testing
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =====================================================
# OPENAI CLIENT CONFIG
# =====================================================
try:
    client = OpenAI(api_key=openai_key)
except Exception as e:
    print(f"❌ Error initializing OpenAI client: {e}")
    client = None

# =====================================================
# ROOT / HEALTH CHECK
# =====================================================
@app.get("/")
def home():
    return {"message": "AI Learning Backend is running ✅"}

# =====================================================
# ENV TEST (Debug Only)
# =====================================================
@app.get("/check-env")
def check_env():
    """Debug endpoint to verify if Render can access API keys."""
    return {
        "OPENAI_API_KEY_found": bool(os.getenv("OPENAI_API_KEY")),
        "OPENAI_API_KEY_prefix": str(os.getenv("OPENAI_API_KEY"))[:8] + "..." if os.getenv("OPENAI_API_KEY") else None
    }

# =====================================================
# COURSES
# =====================================================
@app.get("/courses")
def get_courses():
    try:
        response = supabase.table("courses").select("*").execute()
        print("COURSE RESPONSE:", response)
        return response.data
    except Exception as e:
        import traceback
        print("ERROR in /courses:", e)
        traceback.print_exc()
        return {"error": str(e)}

# =====================================================
# LESSONS
# =====================================================
@app.get("/lessons")
def get_lessons():
    response = supabase.table("lessons").select("*").execute()
    return response.data

# =====================================================
# USERS
# =====================================================
@app.get("/users")
def get_users():
    try:
        response = supabase.table("users").select("*").execute()
        print("DEBUG RAW RESPONSE:", response)
        return response.data
    except Exception as e:
        import traceback
        print("ERROR in /users:", e)
        traceback.print_exc()
        return {"error": str(e)}

# =====================================================
# USER PROGRESS
# =====================================================
@app.get("/progress/{username}")
def get_progress(username: str):
    response = supabase.table("user_progress").select("""
        progress_percentage,
        completed,
        last_accessed,
        users(username),
        courses(title)
    """).execute()
    return [p for p in response.data if p["users"]["username"] == username]

# =====================================================
# USER ACHIEVEMENTS
# =====================================================
@app.get("/achievements/{username}")
def get_achievements(username: str):
    response = supabase.table("user_achievements").select("""
        unlocked_at,
        users(username),
        achievements(name, description)
    """).execute()
    return [a for a in response.data if a["users"]["username"] == username]

# =====================================================
# PLAYGROUND: CHAT
# =====================================================
class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
def chat(request: ChatRequest):
    """Answer all user questions using OpenAI GPT."""
    try:
        if not client:
            raise ValueError("OpenAI client not initialized")

        gpt_res = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an AI tutor for machine learning and AI concepts."},
                {"role": "user", "content": request.message}
            ]
        )
        return {"response": gpt_res.choices[0].message.content}
    except Exception as e:
        print("❌ Chat Error:", e)
        return {"response": f"Could not connect to AI model. Error: {e}"}

# =====================================================
# PLAYGROUND: TEXT GENERATION
# =====================================================
class TextGenRequest(BaseModel):
    prompt: str

@app.post("/generate-text")
def generate_text(request: TextGenRequest):
    """Generate explanations, summaries, or creative text using GPT."""
    try:
        if not client:
            raise ValueError("OpenAI client not initialized")

        gpt_res = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an AI tutor. Generate a detailed explanation or text."},
                {"role": "user", "content": request.prompt}
            ]
        )
        return {"output": gpt_res.choices[0].message.content}
    except Exception as e:
        print("❌ TextGen Error:", e)
        return {"output": f"Could not generate text. Error: {e}"}