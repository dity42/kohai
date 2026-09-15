from anime_parsers_ru import AnimegoParser

def anisearch(atitle: str):
    return AnimegoParser().search(atitle)
