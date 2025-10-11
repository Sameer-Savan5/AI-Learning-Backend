from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from db_client import supabase
from openai import OpenAI
import os

app = FastAPI()

# =====================================================
# CORS CONFIG (allow frontend on Vercel)
# =====================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://ai-learning-website-zeta.vercel.app",  # Frontend URL
        "http://localhost:3000"  # Optional: for local testing
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =====================================================
# OPENAI CONFIG
# =====================================================
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# =====================================================
# ROOT / HEALTH CHECK
# =====================================================
@app.get("/")
def home():
    return {"message": "AI Learning Backend is running ✅"}

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
        print("DEBUG RAW RESPONSE:", response)  # helpful log
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
        gpt_res = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an AI tutor for machine learning and AI concepts."},
                {"role": "user", "content": request.message}
            ]
        )
        return {"response": gpt_res.choices[0].message.content}
    except Exception as e:
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
        gpt_res = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an AI tutor. Generate a detailed explanation or text."},
                {"role": "user", "content": request.prompt}
            ]
        )
        return {"output": gpt_res.choices[0].message.content}
    except Exception as e:
        return {"output": f"Could not generate text. Error: {e}"}