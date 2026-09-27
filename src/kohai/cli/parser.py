import argparse
from importlib.metadata import version

class SubcommandHelpFormatter(argparse.RawDescriptionHelpFormatter):
    """Remove the blank line argparse inserts before the subcommand list."""
    def _format_action(self, action):
        parts = super(argparse.RawDescriptionHelpFormatter, self)._format_action(action)
        if action.nargs == argparse.PARSER:
            # drop the leading empty line before the "commands:" header
            parts = "\n".join(parts.split("\n")[1:])
        return parts

def build_parser() -> argparse.ArgumentParser:
    """Build the top-level argparse parser with all subcommands."""
    parser = argparse.ArgumentParser(
        prog="kohai",
        usage="kohai [OPTIONS] <COMMAND>",
        description="Search and watch anime from the terminal.",
        formatter_class=SubcommandHelpFormatter,
    )

    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"kohai {version('kohai')}",
    )

    subparsers = parser.add_subparsers(dest="command", title="commands", metavar="")
    
    help = subparsers.add_parser("help", help="Show this help message")

    search = subparsers.add_parser("search", help="Search and watch anime")
    # query is optional; if omitted, run_search prompts interactively
    search.add_argument("query", nargs="?", default=None)
    search.add_argument("-q", "--quality", choices=["360", "480", "720"], default=None)

    history = subparsers.add_parser("history", help="Show watch history")
    history.add_argument("-l", "--limit", type=int, default=10, help="Number of entries to show (default: 10)")

    history_sub = history.add_subparsers(dest="history_action")
    history_sub.add_parser("clear", help="Clear watch history")

    history_watch = history_sub.add_parser("watch", help="Replay from history")
    # index: None -> fzf, "last" -> most recent, N -> Nth from the end
    history_watch.add_argument("index", nargs="?", default=None)

    schedule = subparsers.add_parser("schedule", help="Show anime schedule")
    schedule.add_argument("-t", "--today", action="store_true", help="Show only today's schedule")
    schedule.add_argument("-u", "--updates", action="store_true", help="Show recent translation updates")

    bmark = subparsers.add_parser("bmark", help="Manage bookmarks")
    
    bmark_sub = bmark.add_subparsers(dest="bmark_action")

    add = bmark_sub.add_parser("add", help="Add a bookmark")
    add.add_argument("query", help="Anime title to search")

    rm = bmark_sub.add_parser("rm", help="Remove a bookmark")
    rm.add_argument("index", nargs="?", default=None, help="Bookmark number (optional)")

    bmark_watch = bmark_sub.add_parser("watch", help="Watch from bookmarks")
    bmark_watch.add_argument("index", nargs="?", default=None, help="Bookmark number (optional)")
    bmark_watch.add_argument("-q", "--quality", choices=["360", "480", "720"], default=None)

    bmark_info = bmark_sub.add_parser("info", help="Show info for a bookmark")
    bmark_info.add_argument("index", nargs="?", default=None, help="Bookmark number (optional)")

    info = subparsers.add_parser("info", help="Show anime info")
    info.add_argument("query", nargs="?", default=None, help="Anime title")

    season = subparsers.add_parser("season", help="Show anime from the current season")
    season.add_argument("-l", "--limit", type=int, default=None, help="Number of entries to show")
    
    season_sub = season.add_subparsers(dest="season_action")
    season_watch = season_sub.add_parser("watch", help="Watch an anime from the current season")
    season_watch.add_argument("index", nargs="?", default=None, help="Number in the season list (optional, fzf if omitted)")

    return parser
