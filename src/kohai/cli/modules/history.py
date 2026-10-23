from kohai.exceptions import KohaiError
from .common import resolve_index
from kohai.app.history import get_all, get_recent, clear_history
from kohai.cli.format import format_relative_time
from kohai.app.player import play

def run_history_list(limit: int):
    if limit <= 0:
        raise KohaiError("Limit must be greater than 0.")
    
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

def run_history_watch(index):
    entries = get_all()
    if not entries:
        raise KohaiError("No history yet.")
    if index == "last":
        entry = entries[0]
    else:
        idx = resolve_index(index, entries,
            lambda e: f"{e['title']} ({e['translation']}) - {format_relative_time(e['watched_at'])}")
        if idx is None:
            return
        entry = entries[idx]
    play(entry["url"])

def run_history(args):
    action = getattr(args, "history_action", None)

    if action == "clear":
        run_history_clear()
        return

    if action == "watch":
        run_history_watch(args.index)
        return

    run_history_list(args.limit)
