from collections.abc import Callable, Sequence
from typing import TypeVar

from pyfzf import FzfPrompt

T = TypeVar("T")

_fzf = FzfPrompt()

def pick(items: Sequence[T], fmt: Callable[[T], str] = str) -> T | None:
    """Pick one item via fzf. Skips fzf for 0/1 items, returns None on Esc."""
    if not items:
        return None
    if len(items) == 1:
        return items[0]

    labels = [fmt(i) for i in items]
    picked = _fzf.prompt(labels)
    if not picked:
        return None

    # dict(zip(labels, items)) fixes the duplicate-label bug of items[labels.index(p[0])]
    return dict(zip(labels, items)).get(picked[0])
