import subprocess

def episode_watcher(source: str):
    url = 'https:' + source + '720.mp4'
    mpv_command = ["mpv", url]
    process = subprocess.Popen(mpv_command)
    return_code = process.wait()
