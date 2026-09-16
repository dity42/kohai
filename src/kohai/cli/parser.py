import argparse

class SubcommandHelpFormatter(argparse.RawDescriptionHelpFormatter):
    def _format_action(self, action):
        parts = super(argparse.RawDescriptionHelpFormatter, self)._format_action(action)
        if action.nargs == argparse.PARSER:
            parts = "\n".join(parts.split("\n")[1:])
        return parts
    def add_usage(self, usage, actions, groups, prefix=None):
        if prefix is None:
            prefix = "Usage: "
        return super().add_usage(usage, actions, groups, prefix)

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="kohai",
        usage="kohai [OPTIONS] <COMMAND>",
        description="Search and watch anime from the terminal.",
        formatter_class=SubcommandHelpFormatter,
        add_help=False,
    )
    subparsers = parser.add_subparsers(dest="command", title="Commands", metavar="")
    
    help = subparsers.add_parser("help", help="Show this help message")

    search = subparsers.add_parser("search", help="Search and watch anime")
    search.add_argument("query", nargs="?", default=None)
    search.add_argument("-q", "--quality", choices=["360", "480", "720"], default=None)

    history = subparsers.add_parser("history", help="Show watch history")
    history.add_argument("-l", "--limit", type=int, default=10, help="Number of entries to show (default: 10")

    history_sub = history.add_subparsers(dest="history_action")
    history_sub.add_parser("clear", help="Clear watch history")

    options = parser.add_argument_group("Options")
    options.add_argument("-h", "--help", action="help", help="Show this help message and exit")

    return parser
