from anime_parsers_ru import KodikParser, AnimegoParser
import subprocess

PARSER1 = KodikParser()
PARSER2 = AnimegoParser()

def episode_picker(id: str, seria_num: int):
    return PARSER1.get_link(
        id=id, 
        id_type="shikimori",
        seria_num=seria_num,
        translation_id="0"
    )

def episode_watcher(source: str):
    url = 'https:' + source + '720.mp4'
    mpv_command = ["mpv", url]
    process = subprocess.Popen(mpv_command)
    return_code = process.wait()
