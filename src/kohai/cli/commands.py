import subprocess
from pyfzf import FzfPrompt

from kohai.app.aniselector import aniselector, pick_anime
from kohai.app.api import anisearch
from kohai.app.history import get_all, get_recent, clear_history
from kohai.app.schedule import get_schedule, get_today, get_updates
from kohai.app.bookmarks import load_bookmarks, add_bookmark, is_bookmarked
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

def run_schedule_list(entries):
    for e in entries:
        time = e["time"]
        prefix = f"{time}  " if time else ""
        total = e.get("total")
        suffix = f" (из {total})" if total else ""
        print(f"  {prefix}{e['title']} — эп. {e['episode']}{suffix}")

def run_schedule_all() -> None:
    data = get_schedule()
    for day, entries in data["schedule"].items():
        label = data["schedule_dates"].get(day, "")
        header = f"{day} ({label})" if label else day
        print(f"{header}:")
        run_schedule_list(entries)
        print()
        
def run_schedule_updates(entries) -> None:
    if not entries:
        print("No recent updates.")
        return

    for e in entries:
        time = (e.get("time") or "").strip()
        translation = e.get("translation") or ""
        episode = e.get("episode")

        prefix = f"{time}  " if time else ""
        suffix = f" ({translation})" if translation else ""

        if episode and episode != "None":
            ep_str = f" — эп. {episode}"
        else:
            ep_str = ""

        print(f"{prefix}{e['title']}{suffix}{ep_str}")

def run_schedule(args):
    if args.updates:
        entries = get_updates()
        run_schedule_updates(entries)
        return

    if args.today:
        day, entries = get_today()
        if not entries:
            print("Nothing scheduled for today.")
            return
        print(f"{day}:")
        run_schedule_list(entries)
        return
    
    run_schedule_all()

def run_bmark_list() -> None:
    bookmarks = load_bookmarks()
    if not bookmarks:
        print("No bookmarks yet.")
        return

    for i, b in enumerate(bookmarks, start=1):
        print(f"{i}. {b['title']}")

def run_bmark_add(query: str) -> None:
    items = anisearch(query)
    if not items:
        print("Nothing found.")
        return

    anime = pick_anime(items)
    if not anime:
        return

    title = anime["title"]
    if is_bookmarked(title):
        print(f"'{title}' is already in bookmarks.")
        return

    add_bookmark(title, anime.get("original_title"))
    print(f"Added: {title}")

def run_bmark(args) -> None:
    action = getattr(args, "bmark_action", None)
    if action == "add":
        run_bmark_add(args.query)
        return

    run_bmark_list()


def dispatch(args) -> None:
    if args.command == "help":
        build_parser().print_help()
        return

    if args.command == "search":
        run_search(args.query, args.quality)
    elif args.command == "history":
        run_history(args)
    elif args.command == "schedule":
        run_schedule(args)
    elif args.command == "bmark":
        run_bmark(args)
    else: 
        print(f"Unknown command: {args.command}")
