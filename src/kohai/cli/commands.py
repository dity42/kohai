from kohai.app.aniselector import aniselector

def run_search(query: str, quality: str | None) -> None:
    if not query:
        query = input("Type anime name: ").strip()
        if not query:
            return
    aniselector(query, quality)

def dispatch(args) -> None:
    if args.command == "search":
        run_search(args.query, args.quality)
    else: 
        print(f"Unknown command: {args.command}")
