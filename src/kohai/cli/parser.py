import argparse

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="kohai",
        description="Search and watch anime from the terminal.",
    )
    subparsers = parser.add_subparsers(dest="command", title="COMMAND")
    
    help = subparsers.add_parser("help", help="Show this help message")

    search = subparsers.add_parser("search", help="Search and watch anime")
    search.add_argument("query", nargs="?", default=None)
    search.add_argument("-q", "--quality", choices=["360", "480", "720"], default=None)

    return parser
