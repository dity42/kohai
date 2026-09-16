import subprocess
from pyfzf import FzfPrompt

from kohai.app.aniselector import aniselector
from kohai.app.history import get_all, get_recent, clear_history
from kohai.cli.format import format_relative_time
from kohai.cli.parser import build_parser

def run_search(query: str, quality: str | None) -> None:
    if not query:
        query = input("Type anime name: ").strip()
        if not query:
            return
    aniselector(query, quality)

def run_history_list(limit: int):
    if limit <= 0:
        print("Limit must be greater than 0.")
        return
    
    entries = get_recent(limit)
    if not entries:
        print("No history yet.")
        return
    
    for i, entry in enumerate(entries, start=1):
        when = format_relative_time(entry["watched_at"])
        print(f"{i}. {entry['title']} ({entry['translation']}) - {when}")

def run_history_clear():
    entries = get_all()
    if not entries:
        print("History is already empty.")
        return

    if len(entries) >= 50:
        answer = input(f"Clear {len(entries)} entries? [y/N]: ").strip().lower()
        if answer not in ("y", "yes"):
            print("Canceled.")
            return

    clear_history()
    print("History cleared.")

def pick_history_entry(entries):
    display = [
        f"{e['title']} ({e['translation']}) - {format_relative_time(e['watched_at'])}"
        for e in entries
    ] 
    picked = FzfPrompt().prompt(display)
    if not picked:
        return None
    return entries[display.index(picked[0])]

def run_history_watch(index: str | None) -> None:
    entries = get_all()
    if not entries:
        print("No history yet.")
        return

    if index is None:
        entry = pick_history_entry(entries)
    elif index == "last":
        entry = entries[0]
    else:
        try:
            n = int(index)
        except ValueError:
            print(f"Invalid index: {index}")
            return
        if n < 1 or n > len(entries):
            print(f"No entry number {n} (history has {len(entries)} entries).")
            return
        entry = entries[n-1]

    if not entry:
        return

    url = entry['url']
    try:
        subprocess.run(["mpv", url])
    except FileNotFoundError:
        print("mpv not found.")

def run_history(args):
    action = getattr(args, "history_action", None)

    if action == "clear":
        run_history_clear()
        return

    if action == "watch":
        run_history_watch(args.index)
        return

    run_history_list(args.limit)


def dispatch(args) -> None:
    if args.command == "help":
        build_parser().print_help()
        return

    if args.command == "search":
        run_search(args.query, args.quality)
    elif args.command == "history":
        run_history(args)
    else: 
        print(f"Unknown command: {args.command}")
