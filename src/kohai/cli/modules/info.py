from .common import console, Table, box
from kohai.exceptions import KohaiError
from kohai.app.anisearch import anisearch
from kohai.app.clients import get_animego
from kohai.app.aniselector import pick_anime

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
        raise KohaiError("Nothing found.")

    if skip_pick:
        exact = [i for i in items if i.get("title") == query]
        anime = exact[0] if exact else items[0]
    else:
        anime = pick_anime(items)
        if not anime:
            return

    info = get_animego().anime_info(url=anime["link"])
    if not info:
        raise KohaiError("No info available.")

    print_info(info)
