import json 
from datetime import datetime
from pathlib import Path

HISTORY_FILE = Path.home() / ".local" / "share" / "kohai" / "history.json"

def load_history() -> list[dict]:
    """Load watch history from disk.

    Returns an empty list if the file is missing, unreadable,
    or does not contain a JSON array.
    """
    if not HISTORY_FILE.exists():
        return [] 
    try: 
        with HISTORY_FILE.open("r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []

def save_history(history: list[dict]) -> None:
    """Persist history to disk, creating parent dirs if needed."""
    HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    with HISTORY_FILE.open("w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def add_to_history(title, episode, translation, translation_id, quality, url):
    """Append a watch event and save"""
    history = load_history()
    history.append({
        "title": title, 
        "episode": episode,
        "translation": translation,
        "translation_id": translation_id,
        "quality": quality,
        "url": url,
        "watched_at": datetime.now().isoformat(timespec="seconds")
    })
    save_history(history)

def get_recent(limit: int = 10) -> list[dict]:
    """Return the last `limit` entries, newest first."""
    history = load_history()
    return list(reversed(history))[:limit]

def get_all() -> list[dict]:
    """Return all entries, newest first."""
    return list(reversed(load_history()))

def clear_history() -> None:
    """Wipe the history file."""
    save_history([])
