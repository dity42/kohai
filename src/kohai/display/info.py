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

        additional = anime.get('additional_data', {})
        last_ep = additional.get('last_episode', 0)

        info = {
            'title': title,
            'year': year,
            'last_episode': last_ep
        }
        result.append(info)

    for anime in result:
        title = anime.get('title', 'Unknown')
        year = anime.get('year', 'N/A')
        last_ep = anime.get('last_episode', 0)
        print(f"{title} ({year}) - episodes: {last_ep}")

def aninfo():
    PARSER1.get_link(
        id="61169", 
        id_type="shikimori",
        seria_num=10,
        translation_id="0"
    )
