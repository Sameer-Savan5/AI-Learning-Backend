@app.get("/progress/{username}")
def get_progress(username: str):
    response = supabase.table("user_progress").select("*").execute()
    return response.data