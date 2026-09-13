from kohai.api.kodik import episodes_info

def source_selector(query):
    results = []
    for q in query:
        source = q['source']

        if source == 'animego': # Selection in animego don't working now
            display = f"{q.get('or_title', '')} - {q.get('title', 'Unknown')} ({q.get('year', 'N/A')})"
            
            results.append((display, {
                'title': q.get('title', 'Unknown'),
                'or_title': q.get('or_title', 'Unknown'),
                'year': q.get('year', 'N/A'),
                'source': 'animego',
                'available': False,
            })) 
            
        elif source == 'kodik':
            title = q['title']
            year = q['year']
            shikimori_id = q['shikimori_id']
            kinopoisk_id = q['kinopoisk_id']
            imdb_data = q['imdb_id']
            imdb_id = None
            if imdb_data is not None:
                imdb_id = imdb_data[2:]
            worldart_animation = q['worldart_link']
            worldart_id = None
            if worldart_animation is not None:
                worldart_id = worldart_animation.rsplit("=", 1)[-1]
            link = q['link']
            episodes = episodes_info(link)
            series_count, translations = episodes['series_count'], episodes['translations']
            display = f"{title} ({year}) - episodes: {series_count}"
            results.append((display, {
                'title': title,
                'year': year,
                'shikimori_id': shikimori_id,
                'kinopoisk_id': kinopoisk_id,
                'imdb_id': imdb_id,
                'worldart_id': worldart_id,
                'series_count': series_count,
                'translations': translations,
            }))
    return results

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

def translate_selector(translations):
    options = []
    for t in translations:
        display = f"{t.get('name')} (type: {t.get('type')})"
        options.append((display, {
            'id': t.get('id'),
            'type': t.get('type'),
            'name': t.get('name'),
            'series_range': t.get('series_range'),
        }))
    return options

def episode_selector(series_range):
    if not series_range:
        return []
    return [str(e) for e in range(series_range[0], series_range[1] + 1)]
