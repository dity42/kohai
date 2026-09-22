from datetime import datetime, timedelta

def format_relative_time(iso: str) -> str:
    """Format an ISO timestamp as a human-readable relative time.

    Rules:
      < 1 min          -> "just now"
      < 1 hour         -> "N minutes ago"
      < 24h, same day  -> "N hours ago"
      yesterday        -> "yesterday at HH:MM"
      2-6 days         -> "N days ago at HH:MM"
      7+ days          -> "YYYY-MM-DD HH:MM"
    """
    then = datetime.fromisoformat(iso)
    now = datetime.now()
    delta = now - then

    seconds = delta.total_seconds()

    if seconds < 60:
        return "just now"

    if seconds < 3600:
        minutes = int(seconds // 60)
        return f"{minutes} minute{'s' if minutes != 1 else ''} ago"

    # same day, but more than an hour ago
    if then.date() == now.date():
        hours = int(seconds // 3600)
        return f"{hours} hour{'s' if hours != 1 else ''} ago"

    yesterday = (now - timedelta(days=1)).date()
    if then.date() == yesterday:
        return f"yesterday at {then:%H:%M}"

    days = (now.date() - then.date()).days
    if days < 7:
        return f"{days} day{'s' if days != 1 else ''} ago at {then:%H:%M}"

    return then.strftime("%Y-%m-%d %H:%M")
