import subprocess

from rich.console import Console
from rich.table import Table
from rich import box

from kohai.app.clients import animego
from kohai.app.aniselector import aniselector, pick_anime
from kohai.app.api import anisearch
from kohai.app.history import get_all, get_recent, clear_history
from kohai.app.schedule import get_schedule, get_today, get_updates
from kohai.app.bookmarks import load_bookmarks, add_bookmark, is_bookmarked, remove_bookmark
from kohai.app.picker import pick
from kohai.app.player import play
from kohai.cli.format import format_relative_time
from kohai.cli.parser import build_parser

console = Console()

def resolve_index(arg: str | None, items, fmt) -> int | None:
    if arg is None:
        picked = pick(list(enumerate(items)), fmt=lambda t: fmt(t[1]))
        return picked[0] if picked is not None else None
    try:
        n = int(arg)
    except ValueError:
        print(f"Invalid index: {arg}")
        return None
    if n < 1 or n > len(items):
        print(f"No entry number {n} ({len(items)} available).")
        return None
    return n - 1

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

def run_history_watch(index):
    entries = get_all()
    if not entries:
        print("No history yet.")
        return
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
            # animego returns the string "None" for some entries
            ep_str = f" — эп. {episode}"
        else:
            ep_str = ""

        print(f"{prefix}{e['title']}{suffix}{ep_str}")

def run_schedule(args):
    if args.updates:
        # -u takes precedence over -t
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
    """Search animego and save the exact title as a bookmark.

    Skips if the title is already bookmarked.
    """
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

def run_bmark_rm(index: str | None) -> None:
    bookmarks = load_bookmarks()
    if not bookmarks:
        print("No bookmarks yet.")
        return 
    idx = resolve_index(index, bookmarks, lambda b: b["title"])
    if idx is None:
        return
    removed = bookmarks[idx]["title"]
    remove_bookmark(idx)
    print(f"Removed: {removed}")

def run_bmark_watch(index: str | None, quality=None) -> None:
    bookmarks = load_bookmarks()
    if not bookmarks:
        print("No bookmarks yet.")
        return
    idx = resolve_index(index, bookmarks, lambda b: b["title"])
    if idx is None:
        return
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
    idx = resolve_index(index, bookmarks, lambda b: b["title"])
    if idx is None:
        return
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
    """Render anime info with rich tables.

    Table layout:
      - title + score (top)
      - two tables side by side: general | staff
      - genres + description (bottom)
    """
    title_table = Table(show_header=False, box=box.ROUNDED, padding=(0, 2))
    titles = [t.strip() for t in (info.get("title") or "").split("\n") if t.strip()]
    if len(titles) == 1:
        title_table.add_row(f"[bold cyan]Title:[/bold cyan] {titles[0]}")
    elif len(titles) > 1:
        title_table.add_row("[bold cyan]Titles:[/bold cyan]")
        for t in titles:
            title_table.add_row(f"  — {t}")
    title_table.add_row(f"[bold cyan]Score:[/bold cyan] {info.get("score") or "—"}")
    console.print(title_table)

    table1 = Table(show_header=False, box=box.ROUNDED, padding=(0, 2))
    table1.add_row("[bold cyan]Aired[/bold cyan]", info.get("aired_at") or "—")
    table1.add_row("[bold cyan]Type[/bold cyan]", info.get("type") or "—")
    table1.add_row("[bold cyan]Status[/bold cyan]", info.get("status") or "—")

    type_ = info.get("type") or ""
    episodes = info.get("episodes")
    duration = info.get("duration")

    if type_ == "Фильм" or episodes == "1":
        # single-episode titles (movies, some ONA) show Duration instead of Episodes
        table1.add_row("[bold cyan]Duration[/bold cyan]", duration or "—")
    else:
        if episodes and duration:
            ep_str = f"{episodes} по {duration}"
        elif episodes:
            ep_str = episodes
        elif duration:
            ep_str = duration
        else:
            ep_str = "—"
        table1.add_row("[bold cyan]Episodes[/bold cyan]", ep_str)

    table2 = Table(show_header=False, box=box.ROUNDED, padding=(0, 2))
    table2.add_row("[bold cyan]Source[/bold cyan]", info.get("original_source") or "—")
    table2.add_row("[bold cyan]Author[/bold cyan]", info.get("author") or "—")
    table2.add_row("[bold cyan]Studio[/bold cyan]", info.get("studio") or "—")
    table2.add_row("[bold cyan]Director[/bold cyan]", info.get("director") or "—")

    layout = Table.grid(padding=(0, 1))
    layout.add_column()
    layout.add_column()
    layout.add_row(table1, table2)
    console.print(layout)

    genres = info.get("genres")
    description = info.get("description")
    if genres or description:
        desc_table = Table(show_header=False, box=box.ROUNDED, padding=(0, 2))
        if genres:
            desc_table.add_row(f"[bold cyan]Genres:[/bold cyan] {', '.join(genres)}")
        if description:
            desc_table.add_row("[bold cyan]Description[/bold cyan]")
            desc_table.add_row(" ".join(description.split()))
        console.print(desc_table)

def run_info(query: str | None, skip_pick: bool = False) -> None:
    """Show anime info.

    If skip_pick is True (e.g. from bmark info), the query is assumed
    to be an exact title — try exact match in animego results, fall
    back to the first one, and skip the fzf picker.
    """
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

    info = animego.anime_info(url=anime["link"])
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
