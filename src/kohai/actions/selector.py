from pyfzf import FzfPrompt

from kohai.actions.search import anisearch
from kohai.actions.episodes import episode_picker, episode_watcher, episodes_info

fzf = FzfPrompt()

def anime_selector():
    anime_name = str(input("Type anime name: "))
    query = anisearch(anime_name)

    anime_map = {}
    fzf_options = []

    for q in query:
        source = q['source']

        if source == 'animego':
            display = f"{q.get('or_title', '')} - {q.get('title', 'Unknown')} ({q.get('year', 'N/A')})"
            fzf_options.append(display)
            
            anime_map[display] = {
                'title': q.get('title', 'Unknown'),
                'year': q.get('year', 'N/A'),
                'source': 'animego',
                'available': False,
            }
            continue
            
        elif source == 'kodik':
            title = q['title']
            year = q['year']
            shikimori_id = q['shikimori_id']
            link = q['link']
            episodes = episodes_info(link)
            series_count = episodes['series_count']
            translations = episodes['translations']
            display = f"{title} ({year}) - episodes: {series_count}"
            fzf_options.append(display)

            anime_map[display] = {
                'title': title,
                'year': year,
                'shikimori_id': shikimori_id,
                'series_count': series_count,
                'translations': translations,
            }

    selected = fzf.prompt(fzf_options)

    if selected:
        for selected_display in selected:
            if selected_display in anime_map:
                item = anime_map[selected_display]
                series = item['series_count']
                translations = item['translations']
                shikimori_id = item['shikimori_id']

                print(f"Selected: {item}")
                print(f"Series: {series}")
                print(f"Shiki: {shikimori_id}")

                translate_list = []
                translate_data = {}
                for translate in translations:
                    t_id = translate.get('id')
                    t_type = translate.get('type')
                    name = translate.get('name')
                    series_range = translate.get('series_range')
                    display = f"{name} (type: {t_type})"
                    translate_list.append(display)
                    translate_data[display] = {
                        'id': t_id, 
                        'type': t_type,
                        'name': name,
                        'series_range': series_range
                    }
                select_translate = fzf.prompt(translate_list) 

                if select_translate:
                    for selected_display in select_translate:
                        data = translate_data.get(selected_display)
                        if data:
                            series_range = data['series_range']
                            translate_id = data['id']
                            if series_range:
                                episodes = list(range(series_range[0], series_range[1] + 1))
                                select_episode = fzf.prompt([e for e in episodes])
                                if select_episode:
                                    for ep in select_episode:
                                        url = episode_picker(shikimori_id, ep, translate_id)[0] # get link from tuple
                                        episode_watcher(url)
