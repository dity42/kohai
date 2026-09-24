import subprocess

def play(url: str, args: tuple[str, ...] = ("--save-position-on-quit",)) -> bool:
    try:
        subprocess.run(["mpv", *args, url])
        return True
    except FileNotFoundError:
        print("mpv not found.")
        return False
