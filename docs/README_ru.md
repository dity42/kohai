<p align="center">
  <a href="../README.md">English</a> &nbsp;|&nbsp; <b>Русский</b>
</p>

# kohai

CLI-инструмент для поиска, выбора и просмотра аниме из терминала.
Поиск через **animego**, потоковое видео из **kodik**, воспроизведение в **mpv**.

## Возможности
- Поиск аниме по названию и запуск воспроизведения в `mpv`
- Интерактивный выбор через `fzf` — тайтл, перевод, эпизод, качество
- Выбор качества (`360` / `480` / `720`) и прямой переход к эпизоду флагом `-e`
- История просмотров: `history`, `history watch` (повтор), `history clear`
- Закладки: `bmark add` / `rm` / `watch` / `info` / `clear`
- Информация об аниме в виде таблиц `rich`
- Расписание выхода серий: `schedule`, `-t/--today`, `-u/--updates`
- Аниме текущего сезона: `season`, `season watch`
- Токен kodik кешируется локально; данные хранятся в пользовательской директории (`platformdirs`)

## Требования
- **Python 3.14+**
- `mpv`
- `fzf` (нужен для `pyfzf`).

## Установка
С помощью uv tool:
```bash
uv tool install git+https://github.com/dity42/kohai
```

Из исходников (с помощью git + uv):
```bash
git clone https://github.com/dity42/kohai
cd kohai
uv sync
uv run kohai --help
```

Добавление в .local/bin (опционально):
```bash
uv tool install .
kohai --help
```

## Планы
- [ ] Флаг -k/--kodik — пропустить animego и искать напрямую в kodik
- [ ] Тесты (pytest) и CI
- [ ] Линтинг и проверка типов (ruff, mypy)
- [ ] Разбить cli/commands.py на модули по командам
- [ ] Настраиваемый плеер (аргументы mpv / альтернативные плееры)
- [ ] Автозавершение команды по Tab

## Используемый стек
- Python 3.14
- argparse — CLI
- rich — вывод в терминал
- pyfzf + fzf — интерактивный выбор
- mpv — воспроизведение
- anime-parsers-ru — парсеры animego и kodik
- requests — HTTP
- platformdirs — директория данных
- uv / uv_build — сборка и упаковка

## Лицензия
MIT
