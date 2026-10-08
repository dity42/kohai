import os

from pathlib import Path
from platformdirs import user_data_dir

DATA_DIR = Path(user_data_dir("kohai", appauthor=False))
HISTORY_FILE = DATA_DIR / "history.json"
BOOKMARKS_FILE = DATA_DIR / "bookmarks.json"

def atomic_write_text(path: Path, text: str) -> None:
    """Write text to path atomically: temp file in same dir, then rename."""
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    os.replace(tmp, path)
