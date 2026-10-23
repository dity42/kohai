from kohai.app.aniselector import aniselector

def run_search(query: str, quality: str | None, episode: int | None = None) -> None:
    if not query:
        query = input("Type anime name: ").strip()
        if not query:
            return
    aniselector(query, quality=quality, episode=episode)
