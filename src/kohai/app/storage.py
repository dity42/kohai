from pathlib import Path
from platformdirs import user_data_dir

DATA_DIR = Path(user_data_dir("kohai", appauthor=False))
HISTORY_FILE = DATA_DIR / "history.json"
BOOKMARKS_FILE = DATA_DIR / "bookmarks.json"
