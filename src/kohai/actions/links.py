from kohai.utils.builders import get_item_source
from kohai.api.kodik import episode_picker

def resolve_episode_links(item: dict, episode: int, translation_id: str):
    source = get_item_source(item)
    if source is None:
        return None
    id_value, id_type = source
    return episode_picker(id_value, id_type, int(episode), translation_id)
