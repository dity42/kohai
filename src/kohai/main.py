from pyfzf import FzfPrompt
import re

from kohai.actions.search import anisearch
from kohai.actions.episodes import episode_picker, episode_watcher

fzf = FzfPrompt()

def main() -> None:
    anime_name = str(input("Type anime name: "))
    query = anisearch(anime_name)

    fzf_options = []
    for q in query:
        title = q['title']
        year = q['year']
        last_ep = q['last_episode']
        shikimori_id = q['shikimori_id']
        display = f"{title} ({year}) - episodes: {last_ep}, shikimori: {shikimori_id}"
        fzf_options.append(display)

    selected = fzf.prompt(fzf_options)

    if selected:
        for item in selected:
            pattern = r"episodes: (\d+), shikimori: (\d+)"
            match = re.search(pattern, item)

            if match:
                last_episode = int(match.group(1))
                shikimori_id = str(match.group(2))
                print(f"Selected: {item}")
                print(f"Last: {last_episode}")
                print(f"Shiki: {shikimori_id}")
    
                episodes = [e for e in range(1, last_episode+1)]
                select_episode = fzf.prompt(episodes)
                if select_episode:
                    for se in select_episode:
                        url = episode_picker(shikimori_id, se)[0]
                        episode_watcher(url)

if __name__ == "__main__":
    main()
