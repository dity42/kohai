from pathlib import Path

from anime_parsers_ru import KodikParser

from kohai.app.storage import DATA_DIR

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
        cls.FILE.parent.mkdir(parents=True, exist_ok=True)
        cls.FILE.write_text(token)
