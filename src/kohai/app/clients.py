from anime_parsers_ru import AnimegoParser, KodikParser
from kohai.app.token import KodikToken

animego = AnimegoParser()
kodik = KodikParser(token=KodikToken.get(), validate_token=False)
