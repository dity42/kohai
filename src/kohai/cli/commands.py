import subprocess
from anime_parsers_ru import AnimegoParser
from pyfzf import FzfPrompt

from kohai.app import bookmarks
from kohai.app.aniselector import aniselector, pick_anime
from kohai.app.api import anisearch
from kohai.app.history import get_all, get_recent, clear_history
from kohai.app.schedule import get_schedule, get_today, get_updates
from kohai.app.bookmarks import load_bookmarks, add_bookmark, is_bookmarked, remove_bookmark
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
    if not entries:
        return None 
    if len(entries) == 1:
        return entries[0]
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

def pick_bookmark(bookmarks):
    if not bookmarks:
        return None 
    if len(bookmarks) == 1:
        return 0
    display = [f"{b['title']}" for b in bookmarks]
    picked = FzfPrompt().prompt(display)
    if not picked:
        return None 
    return display.index(picked[0])

def run_bmark_rm(index: str | None) -> None:
    bookmarks = load_bookmarks()
    if not bookmarks:
        print("No bookmarks yet.")
        return 

    if index is None:
        idx = pick_bookmark(bookmarks)
        if idx is None:
            return
    else:
        try:
            n = int(index)
        except ValueError:
            print(f"Invalid index: {index}")
            return 
        if n < 1 or n > len(bookmarks):
            print(f"No bookmark number {n} (bookmarks has {len(bookmarks)} entries).")
            return
        idx = n - 1

    removed = bookmarks[idx]["title"]
    remove_bookmark(idx)
    print(f"Removed: {removed}")

def run_bmark_watch(index: str | None, quality=None) -> None:
    bookmarks = load_bookmarks()
    if not bookmarks:
        print("No bookmarks yet.")
        return

    if index is None:
        idx = pick_bookmark(bookmarks)
        if idx is None:
            return
    else:
        try:
            n = int(index)
        except ValueError:
            print(f"Invalid index: {index}")
            return
        if n < 1 or n > len(bookmarks):
            print(f"No bookmark number {n} (bookmarks has {len(bookmarks)} entries).")
            return
        idx = n - 1

    entry = bookmarks[idx]
    aniselector(
        entry["title"],
        quality=quality,
        original_title=entry.get("original_title"),
    )

def run_bmark_info(index: str | None) -> None:
    bookmarks = load_bookmarks()
    if not bookmarks:
        print("No bookmarks yet.")
        return

    if index is None:
        idx = pick_bookmark(bookmarks)
        if idx is None:
            return
    else:
        try:
            n = int(index)
        except ValueError:
            print(f"Invalid index: {index}")
            return
        if n < 1 or n > len(bookmarks):
            print(f"No bookmark number {n} (bookmarks has {len(bookmarks)} entries).")
            return
        idx = n - 1

    run_info(bookmarks[idx]["title"], skip_pick=True)

def run_bmark(args) -> None:
    action = getattr(args, "bmark_action", None)
    if action == "add":
        run_bmark_add(args.query)
        return

    if action == "rm":
        run_bmark_rm(args.index)
        return

    if action == "watch":
        run_bmark_watch(args.index, args.quality)
        return

    if action == "info":
        run_bmark_info(args.index)
        return

    run_bmark_list()

def print_info(info: dict) -> None:
    fields = [
        ("type", "Type"),
        ("aired_at", "Aired"),
        ("episodes", "Episodes"),
        ("status", "Status"),
        ("duration", "Duration"),
        ("studio", "Studio"),
        ("director", "Director"),
        ("author", "Author"),
        ("original_source", "Source"),
        ("score", "Score"),
    ]

    titles = [t.strip() for t in (info.get("title") or "").split("\n") if t.strip()]
    if titles:
        print(f"Title: {'/'.join(titles)}")

    for key, label in fields:
        value = info.get(key)
        if value:
            print(f"{label}: {value}")

    genres = info.get("genres")
    if genres:
        print(f"Genres: {', '.join(genres)}")

    description = info.get("description")
    if description:
        text = " ".join(description.split())
        print()
        print(text)

def run_info(query: str | None, skip_pick: bool = False) -> None:
    if not query:
        query = input("Type anime name: ").strip()
        if not query:
            return

    items = anisearch(query)
    if not items:
        print("Nothing found.")
        return

    if skip_pick:
        exact = [i for i in items if i.get("title") == query]
        anime = exact[0] if exact else items[0]
    else:
        anime = pick_anime(items)
        if not anime:
            return

    info = AnimegoParser().anime_info(url=anime["link"])
    if not info:
        print("No info available.")
        return

    print_info(info)


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
    elif args.command == "info":
        run_info(args.query)
    else: 
        print(f"Unknown command: {args.command}")
