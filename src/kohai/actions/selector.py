from pyfzf import FzfPrompt

from kohai.actions.search import anisearch
from kohai.actions.episodes import episode_picker, episode_watcher

fzf = FzfPrompt()

def anime_selector():
    anime_name = str(input("Type anime name: "))
    query = anisearch(anime_name)

    
    anime_map = {}
    fzf_options = []


    for q in query:
        title = q['title']
        year = q['year']
        last_ep = q['last_episode']
        shikimori_id = q['shikimori_id']
        display = f"{title} ({year}) - episodes: {last_ep}"
        fzf_options.append(display)

        anime_map[display] = {
            'title': title,
            'year': year,
            'last_episode': last_ep,
            'shikimori_id': shikimori_id,
        }

    selected = fzf.prompt(fzf_options)

    if selected:
        for selected_display in selected:
            if selected_display in anime_map:
                item = anime_map[selected_display]
                last_episode = item['last_episode']
                shikimori_id = item['shikimori_id']

                print(f"Selected: {item}")
                print(f"Last: {last_episode}")
                print(f"Shiki: {shikimori_id}")
    
                episodes = list(range(1, last_episode+1))
                select_episode = fzf.prompt(episodes)
                if select_episode:
                    for se in select_episode:
                        url = episode_picker(shikimori_id, se)[0]
                        episode_watcher(url)

