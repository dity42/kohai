from anime_parsers_ru import KodikParser

parser = KodikParser()

def episode_picker(anime_name: str):
    info = parser.search(anime_name, limit=1, strict=True, only_anime=True)
    return info[0]['additional_data']['last_episode']
