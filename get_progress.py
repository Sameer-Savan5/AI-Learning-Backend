from db_client import supabase

def get_progress():
    response = supabase.table("user_progress").select("""
        id,
        progress_percentage,
        completed,
        last_accessed,
        users(username),
        courses(title)
    """).execute()
    return response.data

if __name__ == "__main__":
    progress = get_progress()
    for p in progress:
        print(f"{p['users']['username']} is {p['progress_percentage']}% done with {p['courses']['title']}")