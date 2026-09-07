from anime_parsers_ru import KodikParser, AnimegoParser

PARSER1 = KodikParser()
PARSER2 = AnimegoParser()

def anisearch(atitle: str):
    try: 
        query = PARSER1.search(title=atitle, limit=None, strict=True, only_anime=False, include_material_data=False)
    except: 
        query = PARSER2.search(query=atitle)

    result = []

    for anime in query:
        title = anime.get('title', 'Unknown')
        year = anime.get('year', 'N/A')
        shikimori_id = anime.get('shikimori_id')
        additional = anime.get('additional_data', {})
        last_ep = additional.get('last_episode', 0)

        info = {
            'title': title,
            'year': year,
            'last_episode': last_ep,
            'shikimori_id': shikimori_id, 
        }
        result.append(info)
    return result
