from kohai.exceptions import KohaiError
from rich.console import Console
from rich.table import Table
from rich import box

from kohai.app.picker import pick

console = Console()

def resolve_index(arg: str | None, items, fmt) -> int | None:
    if arg is None:
        picked = pick(list(enumerate(items)), fmt=lambda t: fmt(t[1]))
        return picked[0] if picked is not None else None
    try:
        n = int(arg)
    except ValueError:
        raise KohaiError(f"Invalid index: {arg}") from None
    if n < 1 or n > len(items):
        raise KohaiError(f"No entry number {n} ({len(items)} available).")
    return n - 1
