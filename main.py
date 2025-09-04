from fastapi import FastAPI
from db_client import supabase  # re-use your existing Supabase connection

app = FastAPI()

@app.get("/")
def home():
    return {"message": "AI Learning Backend is running ✅"}

@app.get("/courses")
def get_courses():
    response = supabase.table("courses").select("*").execute()
    return response.data

@app.get("/lessons")
def get_lessons():
    response = supabase.table("lessons").select("*").execute()
    return response.data

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

@app.get("/achievements/{username}")
def get_achievements(username: str):
    response = supabase.table("user_achievements").select("""
        unlocked_at,
        users(username),
        achievements(name, description)
    """).execute()
    return [a for a in response.data if a["users"]["username"] == username]