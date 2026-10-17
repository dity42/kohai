<p align="center">
  <b>English</b> &nbsp;|&nbsp; <a href="./docs/README_ru.md">Русский</a>
</p>

# kohai

CLI tool for searching, picking, and watching anime from the terminal.
Searches via **animego**, streams from **kodik**, plays in **mpv**.

## Features
- Search anime by title and launch playback in `mpv`
- Interactive fuzzy picking with `fzf` — title, translation, episode, quality
- Choose quality (`360` / `480` / `720`) and jump straight to an episode with `-e`
- Watch history: `history`, `history watch` (replay), `history clear`
- Bookmarks: `bmark add` / `rm` / `watch` / `info` / `clear`
- Anime info rendered in rich tables
- Weekly airing schedule: `schedule`, `-t/--today`, `-u/--updates`
- Current-season listing: `season`, `season watch`
- Kodik token cached locally; data stored in the platform user data dir

## Requirements
- **Python 3.14+**
- `mpv`
- `fzf` (needed by `pyfzf`).

## Installation
Via uv tool:
```bash
uv tool install git+https://github.com/dity42/kohai
```

Manual (via git + uv):
```bash
git clone https://github.com/dity42/kohai
cd kohai
uv sync
uv run kohai --help
```

Add in .local/bin (optional):
```bash
uv tool install .
kohai --help
```

## TODO
- [ ] -k/--kodik flag to skip animego and search kodik directly
- [ ] Test suite (pytest) and CI
- [ ] Linting and type checking (ruff, mypy)
- [ ] Split cli/commands.py into per-command modules
- [ ] Configurable player (mpv args / alternative players)
- [ ] Tab autocomplete

## Used stack
- Python 3.14
- argparse — CLI
- rich — terminal output
- pyfzf + fzf — fuzzy picking
- mpv — playback
- anime-parsers-ru — animego & kodik parsers
- requests — HTTP
- platformdirs — data directory
- uv / uv_build — packaging

## License
MIT
