from functools import lru_cache

from anime_parsers_ru import AnimegoParser, KodikParser
from kohai.app.token import KodikToken

@lru_cache()
def get_animego() -> AnimegoParser:
    return AnimegoParser()

@lru_cache()
def get_kodik() -> KodikParser:
    return KodikParser(token=KodikToken.get(), validate_token=False)
