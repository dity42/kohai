from kohai.api.kodik import episodes_info

def source_selector(query):
    results = []
    for q in query:
        source = q['source']

        if source == 'animego': # Selection in animego don't working now
            display = f"{q.get('or_title', '')} - {q.get('title', 'Unknown')} ({q.get('year', 'N/A')})"
            
            results.append((display, {
                'title': q.get('title', 'Unknown'),
                'year': q.get('year', 'N/A'),
                'source': 'animego',
                'available': False,
            })) 
            
        elif source == 'kodik':
            title = q['title']
            year = q['year']
            shikimori_id = q['shikimori_id']
            link = q['link']
            episodes = episodes_info(link)
            series_count, translations = episodes['series_count'], episodes['translations']
            display = f"{title} ({year}) - episodes: {series_count}"
            results.append((display, {
                'title': title,
                'year': year,
                'shikimori_id': shikimori_id,
                'series_count': series_count,
                'translations': translations,
            }))
    return results

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
