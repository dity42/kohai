from anime_parsers_ru import KodikParser, AnimegoParser

from kohai.utils.parse_results import _first_parser_results, _second_parser_results

def anisearch(atitle: str):
    try: 
        parser = KodikParser()
        query = parser.search(title=atitle, limit=None, strict=True, only_anime=False, include_material_data=False)
        return _first_parser_results(query)
    except: 
        parser = AnimegoParser()
        query = parser.search(query=atitle)
        return _second_parser_results(query)
