from pathlib import Path

from anime_parsers_ru import KodikParser

from kohai.app.storage import DATA_DIR, atomic_write_text

class KodikToken:
    FILE: Path = DATA_DIR / "kodik_token"

    @classmethod
    def get(cls) -> str:
        cached = cls.load()
        if cached:
            return cached
        token = KodikParser.get_token()
        cls.save(token)
        return token

    @classmethod
    def load(cls) -> str | None:
        try:
            return cls.FILE.read_text().strip()
        except OSError:
            return None

    @classmethod
    def save(cls, token: str) -> None:
        atomic_write_text(cls.FILE, token)
