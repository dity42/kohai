def _first_parser_results(query): 
    return [
        {
            'title': anime.get('title', 'Unknown'),
            'year': anime.get('year', 'N/A'),
            'shikimori_id': anime.get('shikimori_id'),
            'link': anime.get('link'),
            'source': 'kodik',
        }
        for anime in query
    ]

def _second_parser_results(query):
    return [
        {
            'title': anime.get('title', 'Unknown'),
            'or_title': anime.get('original_title', 'Unknown'),
            'year': anime.get('year', 'N/A'),
            'link': anime.get('link'),
            'id': anime.get('id'),
            'source': 'animego'
        }
        for anime in query
    ]
