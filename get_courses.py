from db_client import supabase

def get_courses():
    # Ask Supabase for all rows in the "courses" table
    response = supabase.table("courses").select("*").execute()
    return response.data

if __name__ == "__main__":
    courses = get_courses()
    
    if not courses:
        print("No courses found. Did you add sample data?")
    else:
        print("Available Courses:")
        for course in courses:
            print(f"- {course['title']} ({course['difficulty_level']})")