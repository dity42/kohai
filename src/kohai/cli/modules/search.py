from kohai.app.aniselector import aniselector

def run_search_animego(query: str, quality: str | None, episode: int | None = None) -> None:
    if not query:
        query = input("Type anime name: ").strip()
        if not query:
            return
    aniselector(query, quality=quality, episode=episode)

def run_search_kodik(query: str, quality: str | None, episode: int | None = None) -> None:
    if not query:
        query = input("Type anime name: ").strip()
        if not query:
            return
    aniselector(atitle=query, original_title=query, quality=quality, episode=episode)

def run_search(args):
    if args.kodik:
        run_search_kodik(args.query, args.quality, args.episode)
    else:
        run_search_animego(args.query, args.quality, args.episode)
