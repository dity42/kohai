from datetime import datetime, timedelta

def format_relative_time(iso: str) -> str:
    then = datetime.fromisoformat(iso)
    now = datetime.now()
    delta = now - then

    seconds = delta.total_seconds()

    if seconds < 60:
        return "just now"

    if seconds < 3600:
        minutes = int(seconds // 60)
        return f"{minutes} minute{'s' if minutes != 1 else ''} ago"

    yesterday = (now - timedelta(days=1)).date()
    if then.date() == yesterday:
        return f"yesterday at {then:%H:%M}"

    days = (now.date() - then.date()).days 
    if days < 7:
        return f"{days} day{'s' if days != 1 else ''} ago at {then:%H:%M}"

    return then.strftime("%Y-%m-$d %H:%M")
