import subprocess
from kohai.exceptions import KohaiError

def play(url: str, args: tuple[str, ...] = ("--save-position-on-quit",)) -> None:
    try:
        print("Loading video, please wait...")
        subprocess.run(["mpv", *args, url])
    except FileNotFoundError:
        raise KohaiError("mpv not found.") from None
