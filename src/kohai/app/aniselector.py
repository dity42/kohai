from anime_parsers_ru.parser_kodik_async import KodikParser
from pyfzf import FzfPrompt
import subprocess

from kohai.app.api import anisearch
from kohai.app.history import add_to_history

fzf = FzfPrompt()

def get_item_source(item: dict) -> tuple[str, str] | None:
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

    display =  [
        f"{i.get('title', 'Unknown')} - {i.get('original_title', '')}".strip(" -") 
        for i in items
    ]
    picked = fzf.prompt(display)
    if not picked:
        return None 
    return items[display.index(picked[0])]

def pick_translation(translations):
    display = [f"{t.get('name')} (type: {t.get('type')})" for t in translations]
    picked = fzf.prompt(display)
    if not picked:
        return None
    return translations[display.index(picked[0])]

def pick_episode(series_range):
    if not series_range:
        return None
    episodes = [str(e) for e in range(series_range[0], series_range[1] + 1)]
    picked = fzf.prompt(episodes)
    if not picked:
        return None
    return int(picked[0])

def pick_quality():
    qualities = ["360", "480", "720"]
    picked = fzf.prompt(qualities)
    if not picked:
        return None
    return picked[0]

def aniselector(atitle: str, quality: str | None = None):
    items = anisearch(atitle)
    if not items: 
        print("Nothing found.")
        return

    anime = pick_anime(items)
    if not anime:
        return

    query = anime.get('original_title') or anime['title']
    candidate = KodikParser().search(query, limit=1)
    if not candidate:
        print("Nothing found.")
        return

    item = candidate[0]
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

    add_to_history(
        title=anime.get('title') or query,
        episode=episode,
        translation=translation.get('name'),
        translation_id=translation.get('id'),
        quality=quality,
        url=url
    )
