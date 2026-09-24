import re
from kohai.app.clients import animego

def _extract_total(raw: str) -> int | None:
    """Extract total episode count from a '... (из N)' string."""
    m = re.search(r'\(из (\d+)\)', raw)
    return int(m.group(1)) if m else None

def _normalize_time(raw: str) -> str:
    """Clean up the raw 'time' field from animego schedule.

    Chinese ongoing titles have no air time — animego puts
    'Серия N ... (из M)' into the time field instead. We return
    an empty string for those and keep only the first line
    (the actual air time) for normal entries.
    """
    if not raw:
        return ""
    first_line = raw.split("\n")[0].strip()
    if first_line.startswith("Серия"):
        return ""
    return first_line

def _normalize_entry(e: dict) -> dict:
    """Normalize a single schedule entry in place.

    Sets `time` to a clean value (or empty string) and extracts
    `total` (episode count) into a separate field.
    """
    raw_time = e.get("time", "")
    e["time"] = _normalize_time(raw_time)
    e["total"] = _extract_total(raw_time)
    return e

def get_schedule() -> dict:
    """Fetch the weekly schedule and normalize each entry."""
    data = animego.get_schedule()
    for day, entries in data["schedule"].items():
        for e in entries:
            _normalize_entry(e)
    return data

def get_today() -> tuple[str, list[dict]]:
    """Return (day_name, entries) for today's schedule.

    Uses `schedule_dates` (not the day name) to find today,
    because "today" is a date, not a weekday.
    """
    data = get_schedule()
    for day, date_label in data["schedule_dates"].items():
        if date_label == "Сегодня":
            return day, data["schedule"][day]
    return "", []

def get_updates() -> list[dict]:
    """Fetch recent translation updates (new dubs/subs)."""
    return animego.get_anime_updates()
