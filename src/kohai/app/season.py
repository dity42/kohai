from kohai.app.clients import animego

def get_current_season() -> list[dict]:
    """Return anime from the current season."""
    return animego.get_anime_from_current_season()
