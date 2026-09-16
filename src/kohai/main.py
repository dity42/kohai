from kohai.cli.parser import build_parser
from kohai.app.aniselector import aniselector

def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    query = args.query
    if not query:
        query = input("Type anime name: ").strip()
        if not query:
            return
    
    aniselector(query, quality=args.quality)

if __name__ == "__main__":
    main()
