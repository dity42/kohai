import re
from anime_parsers_ru import AnimegoParser

def _extract_total(raw: str) -> int | None:
    m = re.search(r'\(из (\d+)\)', raw)
    return int(m.group(1)) if m else None

def _normalize_time(raw: str) -> str:
    if not raw:
        return ""
    first_line = raw.split("\n")[0].strip()
    if first_line.startswith("Серия"):
        return ""
    return first_line

def _normalize_entry(e: dict) -> dict:
    raw_time = e.get("time", "")
    e["time"] = _normalize_time(raw_time)
    e["total"] = _extract_total(raw_time)
    return e

def get_schedule() -> dict:
    data = AnimegoParser().get_schedule()
    for day, entries in data["schedule"].items():
        for e in entries:
            _normalize_entry(e)
    return data

def get_today() -> tuple[str, list[dict]]:
    data = get_schedule()
    for day, date_label in data["schedule_dates"].items():
        if date_label == "Сегодня":
            return day, data["schedule"][day]
    return "", []

def get_updates() -> list[dict]:
    return AnimegoParser().get_anime_updates()
