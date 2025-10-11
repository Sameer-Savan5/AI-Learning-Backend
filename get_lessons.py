from db_client import supabase

def get_lessons():
    response = supabase.table("lessons").select("*").execute()
    return response.data

if __name__ == "__main__":
    lessons = get_lessons()
    
    if not lessons:
        print("No lessons found.")
    else:
        print("Available Lessons:")
        for lesson in lessons:
            print(f"- {lesson['title']} ({lesson['content_type']}, {lesson['duration_minutes']} mins)")
            