import json 
from pathlib import Path

BOOKMARKS_FILE = Path.home() / ".local" / "share" / "kohai" / "bookmarks.json"

def load_bookmarks() -> list[dict]:
    if not BOOKMARKS_FILE.exists():
        return []
    try:
        with BOOKMARKS_FILE.open("r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []

def save_bookmarks(bookmarks: list[dict]) -> None:
    BOOKMARKS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with BOOKMARKS_FILE.open("w", encoding="utf-8") as f:
        json.dump(bookmarks, f, ensure_ascii=False, indent=2)

def is_bookmarked(title: str) -> bool:
    return any(b["title"] == title for b in load_bookmarks())

def add_bookmark(title: str, original_title: str | None) -> None:
    bookmarks = load_bookmarks()
    bookmarks.append({
        "title": title,
        "original_title": original_title,
    })
    save_bookmarks(bookmarks)

def remove_bookmark(index: int) -> None:
    bookmarks = load_bookmarks()
    if 0 <= index < len(bookmarks):
        bookmarks.pop(index)
        save_bookmarks(bookmarks)
