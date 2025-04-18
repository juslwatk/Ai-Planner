from datetime import datetime, timedelta

def get_available_time_range() -> tuple[datetime, datetime]:
    print("\n📅 Let's set your available time for today.")
    
    start_str = input("Start time (e.g., 09:00): ")
    end_str = input("End time (e.g., 17:00): ")

    start = datetime.strptime(start_str, "%H:%M")
    end = datetime.strptime(end_str, "%H:%M")

    return start, end