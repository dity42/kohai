from anime_parsers_ru.parser_kodik_async import KodikParser
from pyfzf import FzfPrompt
import subprocess

from kohai.app.api import anisearch
from kohai.app.history import add_to_history

fzf = FzfPrompt()

# All pick_* helpers return None on cancel (Esc) and skip fzf
# automatically when there is only one option.

def get_item_source(item: dict) -> tuple[str, str] | None:
    """Return (id, source_type) for kodik.

    Priority: shikimori -> kinopoisk -> imdb -> worldart.
    Kodik accepts any of these, but shikimori is the most precise.
    """
    id_sources = [
        ('shikimori_id', 'shikimori'),
        ('kinopoisk_id', 'kinopoisk'),
        ('imdb_id', 'imdb'),
        ('worldart_id', 'worldart'),
    ]
    for key, source in id_sources:
        value = item.get(key)
        if value is not None:
            return value, source
    return None

def resolve_episode_links(item: dict, episode: int, translation_id: str):
    """Fetch direct episode links from kodik."""
    source = get_item_source(item)
    if source is None:
        return None
    id_value, id_type = source
    return KodikParser().get_link(
        id=id_value, 
        id_type=id_type,
        seria_num=int(episode),
        translation_id=translation_id,
    )

def normalize_ids(item: dict) -> dict:
    """Normalize ids to the format kodik expects.

    imdb comes as 'tt1234567' — kodik wants '1234567'.
    worldart_id is extracted from worldart_link (not present in item).
    """
    imdb = item.get('imdb_id')
    if imdb and isinstance(imdb, str) and imdb.startswith('tt'):
        item['imdb_id'] = imdb[2:]

    worldart_link = item.get('worldart_link')
    if worldart_link:
        item['worldart_id'] = worldart_link.rsplit("=", 1)[-1]

    return item

def pick_anime(items):
    if not items:
        return None 

    if len(items) == 1:
        return items[0]

    display =  [
        f"{i.get('title', 'Unknown')} - {i.get('original_title', '')}".strip(" -") 
        for i in items
    ]
    picked = fzf.prompt(display)
    if not picked:
        return None 
    return items[display.index(picked[0])]

def pick_title(candidates):
    if not candidates:
        return None

    if len(candidates) == 1:
        return candidates[0]

    display = [
        f"{c.get('title', 'Unknown')} ({c.get('year', 'N/A')})"
        for c in candidates
    ]
    picked = fzf.prompt(display)
    if not picked:
        return None
    return candidates[display.index(picked[0])]

def pick_translation(translations):
    if not translations: 
        return None

    if len(translations) == 1:
        return translations[0]

    display = [f"{t.get('name')} (type: {t.get('type')})" for t in translations]
    picked = fzf.prompt(display)
    if not picked:
        return None
    return translations[display.index(picked[0])]

def pick_episode(series_range):
    if not series_range:
        return None

    episodes = list(range(series_range[0], series_range[1] + 1))
    if len(episodes) == 1:
        return episodes[0]

    display = [str(e) for e in episodes]
    picked = fzf.prompt(display)
    if not picked:
        return None
    return int(picked[0])

def pick_quality():
    qualities = ["360", "480", "720"]
    picked = fzf.prompt(qualities)
    if not picked:
        return None
    return picked[0]

def aniselector(atitle: str, quality: str | None = None, original_title: str | None = None):
    """Resolve a title and launch mpv.

    If original_title is provided (e.g. from bmark watch), skip animego
    search and go straight to kodik. Otherwise, search animego and let
    the user pick the exact title.

    If quality is provided (e.g. from the -q flag), skip the quality
    prompt.
    """
    if original_title: 
        # caller already knows the exact title (e.g. from bmark watch)
        query = original_title
        title = atitle
    else:
        items = anisearch(atitle)
        if not items: 
            print("Nothing found.")
            return
        anime = pick_anime(items)
        if not anime:
            return
        query = anime.get('original_title') or anime['title']
        title = anime.get('title') or query

    candidates = KodikParser().search(query)
    if not candidates:
        print("Nothing found in kodik.")
        return

    if len(candidates) == 1:
        item = candidates[0]
    else: 
        item = pick_title(candidates)
        if not item:
            return

    normalize_ids(item)
    info = KodikParser().get_info_from_embed("https:" + item['link'])
    translations = info['translations']

    translation = pick_translation(translations)
    if not translation:
        return

    series_range = translation.get('series_range')
    episode = pick_episode(series_range)
    if episode is None:
        return

    if quality is None:
        quality = pick_quality()
        if not quality:
            return

    link = resolve_episode_links(item, episode, translation['id'])
    if not link:
        print("No link.")
        return

    url = 'https:' + link[0] + quality + '.mp4'
    try:
        subprocess.run(["mpv", "--save-position-on-quit", url])
    except FileNotFoundError:
        print("mpv not found.")
        return

    # record to history only after mpv launched successfully
    add_to_history(
        title=title,
        episode=episode,
        translation=translation.get('name'),
        translation_id=translation.get('id'),
        quality=quality,
        url=url
    )
