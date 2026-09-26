from kohai.app.clients import kodik
from kohai.app.anisearch import anisearch
from kohai.app.history import add_to_history
from kohai.app.picker import pick
from kohai.app.player import play

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
    return kodik.get_link(
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
    return pick(items, lambda i: f"{i.get('title', 'Unknown')} - {i.get('original_title', '')}".strip(" -"))

def aniselector(atitle: str, quality: str | None = None, original_title: str | None = None):
    """Resolve a title and launch mpv.

    If original_title is provided (e.g. from bmark watch), skip animego
    search and go straight to kodik. Otherwise, search animego and let
    the user pick the exact title.

    If quality is provided (e.g. from the -q flag), skip the quality
    prompt.
    """
    if original_title: 
        query, title = original_title, atitle
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

    candidates = kodik.search(query)
    if not candidates:
        print("Nothing found in kodik.")
        return
    item = pick(candidates, lambda c: f"{c.get('title', 'Unknown')} ({c.get('year', 'N/A')})")
    if not item:
        return

    normalize_ids(item)
    info = kodik.get_info_from_embed("https:" + item['link'])
    if not info:
        return

    translation = pick(info["translations"], lambda t: f"{t.get('name')} (type: {t.get('type')})")
    if not translation:
        return

    series_range = translation.get('series_range')
    if not series_range:
        return
    episode = pick(list(range(series_range[0], series_range[1] + 1)), fmt=str)
    if episode is None:
        return

    if quality is None:
        quality = pick(["360", "480", "720"])
        if not quality:
            return

    link = resolve_episode_links(item, episode, translation['id'])
    if not link:
        print("No link.")
        return

    url = 'https:' + link[0] + quality + '.mp4'
    if play(url):
        add_to_history(title=title, episode=episode, translation=translation.get("name"),
                       translation_id=translation.get("id"), quality=quality, url=url)
