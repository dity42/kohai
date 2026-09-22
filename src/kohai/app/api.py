from anime_parsers_ru import AnimegoParser

def anisearch(atitle: str):
    """Search animego, return list of raw results (dicts)."""
    return AnimegoParser().search(atitle)
