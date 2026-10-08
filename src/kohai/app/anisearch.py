from kohai.app.clients import get_animego

def anisearch(atitle: str):
    """Search animego, return list of raw results (dicts)."""
    return get_animego().search(atitle)
