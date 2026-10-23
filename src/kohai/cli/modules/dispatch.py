from kohai.exceptions import KohaiError
from kohai.cli.parser import build_parser
from .search import run_search
from .history import run_history
from .schedule import run_schedule
from .bookmarks import run_bmark
from .info import run_info
from .season import run_season

def dispatch(args) -> None:
    if args.command == "help":
        build_parser().print_help()
        return

    if args.command == "search":
        run_search(args.query, args.quality, args.episode)
    elif args.command == "history":
        run_history(args)
    elif args.command == "schedule":
        run_schedule(args)
    elif args.command == "bmark":
        run_bmark(args)
    elif args.command == "info":
        run_info(args.query)
    elif args.command == "season":
        run_season(args)
    else: 
        raise KohaiError(f"Unknown command: {args.command}")
