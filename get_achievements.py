from db_client import supabase

def get_achievements():
    response = supabase.table("user_achievements").select("""
        id,
        unlocked_at,
        users(username),
        achievements(name, description)
    """).execute()
    return response.data

if __name__ == "__main__":
    achievements = get_achievements()
    for a in achievements:
        print(f"{a['users']['username']} unlocked {a['achievements']['name']} on {a['unlocked_at']}")