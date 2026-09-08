from anime_parsers_ru import KodikParser, AnimegoParser

PARSER1 = KodikParser()
PARSER2 = AnimegoParser()

def anisearch(atitle: str):
    try: 
        query = PARSER1.search(title=atitle, limit=None, strict=True, only_anime=False, include_material_data=False)
        return _first_parser_results(query)
    except: 
        query = PARSER2.search(query=atitle)
        return _second_parser_results(query)

def _first_parser_results(query): 
    result = []
    for anime in query:
        title = anime.get('title', 'Unknown')
        year = anime.get('year', 'N/A')
        shikimori_id = anime.get('shikimori_id')
        link = anime.get('link')
        info = {
            'title': title,
            'year': year,
            'shikimori_id': shikimori_id,
            'link': link,
        }
        result.append(info)
    return result

def _second_parser_results(query):
    result = []
    for anime in query:
        title = anime.get('title', 'Unknown')
        year = anime.get('year', 'N/A')
        id = anime.get('id')
        info = {
            'title': title,
            'year': year,
            'last_episode': None,
            'shikimori_id': None,
        }
        result.append(info)
    return result
