from kohai.exceptions import KohaiError
from kohai.app.season import get_current_season
from kohai.app.aniselector import aniselector
from .common import resolve_index

def _season_entries(limit: int | None) -> list[dict] | None:
    entries = get_current_season()
    if not entries:
        raise KohaiError("Nothing found.")
    if limit is not None and limit <= 0:
        raise KohaiError("Limit must be greater than 0.")
    return entries[:limit] if limit else entries

def run_season_list(limit: int | None) -> None:
    entries = _season_entries(limit)
    if not entries:
        return
    for i, a in enumerate(entries, start=1):
        title = a.get("title") or "Unknown"
        other = a.get("other_title")
        score = a.get("score")
        line = f"{i}. {title}"
        if other:
            line += f" ({other})"
        if score:
            line += f" — {score}"
        print(line)

def run_season_watch(index: str | None, quality: str | None = None, episode: int | None = None) -> None:
    entries = get_current_season()
    if not entries:
        raise KohaiError("Nothing found.")
    idx = resolve_index(index, entries, fmt=lambda a: f"{a.get('title')} ({a.get('other_title')}) — {a.get('score')}")
    if idx is None:
        return
    entry = entries[idx]
    aniselector(
        entry["title"],
        quality=quality,
        original_title=entry.get("other_title"),
        episode=episode,
    )

def run_season(args) -> None:
    action = getattr(args, "season_action", None)
    if action == "watch":
        run_season_watch(args.index, args.quality, args.episode)
        return
    run_season_list(args.limit)
