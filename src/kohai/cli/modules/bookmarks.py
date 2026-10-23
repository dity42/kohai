from kohai.exceptions import KohaiError
from kohai.app.bookmarks import load_bookmarks, add_bookmark, is_bookmarked, remove_bookmark, save_bookmarks
from kohai.app.aniselector import aniselector, pick_anime
from kohai.app.anisearch import anisearch
from .common import resolve_index
from .info import run_info

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
        raise KohaiError("Nothing found.")

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
        raise KohaiError("No bookmarks yet.")
    idx = resolve_index(index, bookmarks, lambda b: b["title"])
    if idx is None:
        return
    removed = bookmarks[idx]["title"]
    remove_bookmark(idx)
    print(f"Removed: {removed}")

def run_bmark_watch(index: str | None, quality=None, episode: int | None = None) -> None:
    bookmarks = load_bookmarks()
    if not bookmarks:
        raise KohaiError("No bookmarks yet.")
    idx = resolve_index(index, bookmarks, lambda b: b["title"])
    if idx is None:
        return
    entry = bookmarks[idx]
    aniselector(
        entry["title"],
        quality=quality,
        original_title=entry.get("original_title"),
        episode=episode,
    )

def run_bmark_info(index: str | None) -> None:
    bookmarks = load_bookmarks()
    if not bookmarks:
        raise KohaiError("No bookmarks yet.")
    idx = resolve_index(index, bookmarks, lambda b: b["title"])
    if idx is None:
        return
    run_info(bookmarks[idx]["title"], skip_pick=True)

def run_bmark_clear():
    bookmarks = load_bookmarks()
    if not bookmarks:
        print("No bookmarks yet.")
        return

    if len(bookmarks) >= 5:
        answer = input(f"Clear {len(bookmarks)} bmarks? [y/N]: ").strip().lower()
        if answer not in ("y", "yes"):
            print("Canceled.")
            return

    save_bookmarks([])
    print("Bookmarks cleared.")

def run_bmark(args) -> None:
    action = getattr(args, "bmark_action", None)
    if action == "add":
        run_bmark_add(args.query)
        return

    if action == "rm":
        run_bmark_rm(args.index)
        return

    if action == "watch":
        run_bmark_watch(args.index, args.quality, args.episode)
        return

    if action == "info":
        run_bmark_info(args.index)
        return

    if action == "clear":
        run_bmark_clear()
        return

    run_bmark_list()
