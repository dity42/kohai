import argparse

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="kohai",
        description="Search and watch anime from the terminal.",
    )

    parser.add_argument(
        "query",
        nargs="?",
        default=None,
        help="Anime title to search for. If omitted, you'll be prompted.",
    )

    parser.add_argument(
        "-q", "--quality",
        choices=["360", "480", "720"],
        default=None,
        help="Video quality. If omitted, you'll be prompted.",
    )

    return parser
