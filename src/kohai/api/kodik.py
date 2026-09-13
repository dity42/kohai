from anime_parsers_ru import KodikParser

parser = KodikParser()

def episode_picker(id: str, id_type:str, seria_num: int, t_id: str):
    return parser.get_link(
        id=id, 
        id_type=id_type,
        seria_num=seria_num,
        translation_id=t_id,
    )

def episodes_info(part: str):
    url = "https:" + part
    return parser.get_info_from_embed(url)
