from anime_parsers_ru import KodikParser, AnimegoParser
import subprocess

from kohai.actions.search import anisearch

PARSER1 = KodikParser()
PARSER2 = AnimegoParser()

def episode_picker(id: str, seria_num: int, t_id: str):
    return PARSER1.get_link(
        id=id, 
        id_type="shikimori",
        seria_num=seria_num,
        translation_id=t_id,
    )

def episode_watcher(source: str):
    url = 'https:' + source + '720.mp4'
    mpv_command = ["mpv", url]
    process = subprocess.Popen(mpv_command)
    return_code = process.wait()

def episodes_info(part: str):
    url = "https:" + part
    return PARSER1.get_info_from_embed(url)
