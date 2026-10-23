from kohai.app.schedule import get_schedule, get_today, get_updates

def run_schedule_list(entries):
    for e in entries:
        time = e["time"]
        prefix = f"{time}  " if time else ""
        total = e.get("total")
        suffix = f" (из {total})" if total else ""
        print(f"  {prefix}{e['title']} — эп. {e['episode']}{suffix}")

def run_schedule_all() -> None:
    data = get_schedule()
    for day, entries in data["schedule"].items():
        label = data["schedule_dates"].get(day, "")
        header = f"{day} ({label})" if label else day
        print(f"{header}:")
        run_schedule_list(entries)
        print()

def run_schedule_updates(entries) -> None:
    if not entries:
        print("No recent updates.")
        return

    for e in entries:
        time = (e.get("time") or "").strip()
        translation = e.get("translation") or ""
        episode = e.get("episode")

        prefix = f"{time}  " if time else ""
        suffix = f" ({translation})" if translation else ""

        if episode and episode != "None":
            # animego returns the string "None" for some entries
            ep_str = f" — эп. {episode}"
        else:
            ep_str = ""

        print(f"{prefix}{e['title']}{suffix}{ep_str}")

def run_schedule(args):
    if args.updates:
        # -u takes precedence over -t
        entries = get_updates()
        run_schedule_updates(entries)
        return

    if args.today:
        day, entries = get_today()
        if not entries:
            print("Nothing scheduled for today.")
            return
        print(f"{day}:")
        run_schedule_list(entries)
        return

    run_schedule_all()
