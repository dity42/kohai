from kohai.app.clients import get_animego

def get_current_season() -> list[dict]:
    """Return anime from the current season."""
    return get_animego().get_anime_from_current_season()
