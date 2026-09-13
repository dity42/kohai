from pyfzf import FzfPrompt

from kohai.api.anisearch import anisearch
from kohai.actions.links import resolve_episode_links
from kohai.actions.watch import episode_watcher
from kohai.utils.builders import source_selector, translate_selector, episode_selector

fzf = FzfPrompt()

def aniselector():
    anime_name = input("Type anime name: ")
    query = anisearch(anime_name)

    options = source_selector(query)
    if not options:
        print("Nothing found.")
        return


    display_map = {display: data for display, data in options}
    selected = fzf.prompt(list(display_map.keys()))
    if not selected:
        return

    for selected_display in selected:
        item = display_map.get(selected_display)
        if not item:
            continue
        
        if item.get('available') is False:
            print(f"{item.get('or_title', item.get('title'))} — unavailable")
            continue

        translate_options = dict(translate_selector(item['translations']))
        select_translate = fzf.prompt(list(translate_options))
        if not select_translate:
            continue

        for selected_translate in select_translate:
            translate_data = translate_options.get(selected_translate)
            if not translate_data:
                continue

            episodes = episode_selector(translate_data['series_range'])
            select_episode = fzf.prompt(episodes)
            if not select_episode:
                continue

            for ep in select_episode:
                links = resolve_episode_links(item, ep, translate_data['id'])
                if links:
                    episode_watcher(links[0])
