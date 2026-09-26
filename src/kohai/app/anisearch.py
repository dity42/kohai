from kohai.app.clients import animego

def anisearch(atitle: str):
    """Search animego, return list of raw results (dicts)."""
    return animego.search(atitle)
