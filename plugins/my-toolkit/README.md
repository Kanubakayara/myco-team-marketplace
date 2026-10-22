# my-toolkit

## Purpose

Набір інструментів Claude Code для сервісу myco-ai (Python, FastAPI, полегшена Clean Architecture).
Головний біль, який він закриває: кожен новий ендпоінт — це той самий наскрізний зріз через ~9 файлів
(domain → порт → адаптер → use case → роутер + схема → wiring → три тест-файли → документація),
який вручну проходиться 5–7 однотипними prompts і ламається на дрібницях. Плагін зводить зріз
до трьох команд, звіряє поля зовнішнього API до коду і не пускає в git порушення dependency rule
та червоні тести.

## Install

З marketplace команди (public GitHub):

```text
/plugin marketplace add Kanubakayara/myco-team-marketplace
/plugin install my-toolkit@myco-team
```

Для всієї команди — зі scope `project`, щоб запис потрапив у `.claude/settings.json` проєкту:

```bash
claude plugin install my-toolkit@myco-team --scope project
```

Локальна перевірка без встановлення: `claude --plugin-dir ./my-toolkit`.

Потрібно: `uv`, `jq`, віртуальне оточення проєкту `.venv` (`make install`).

## Commands

| Команда | Що робить | Приклад |
|---|---|---|
| `/my-toolkit:scaffold-adapter` | Новий адаптер у `recognition/infrastructure` під domain-порт: адаптер, unit-тест, експорт, wiring у `main.py` | `/my-toolkit:scaffold-adapter fixture_cover_reader CoverReader з JSON-фікстури за sha256 фото` |
| `/my-toolkit:feature-plan` | План наскрізного зрізу по шарах + допущення + однорядник live probe джерела; коду не пише | `/my-toolkit:feature-plan GET /api/v1/igdb-games/{id}/editions — видання гри з IGDB` |
| `/my-toolkit:feature-build` | Після підтвердженого плану — усі шари, wiring і три тест-файли за один прохід, `make lint && make test` до зеленого | `/my-toolkit:feature-build` |
| `/my-toolkit:feature-ship` | Два рядки документації, lint + тести, коміт з позначкою плагіна, рядок у `LOG.md`; не пушить | `/my-toolkit:feature-ship` |

`feature-*` — це skills (`skills/feature-*/SKILL.md`), що викликаються як slash-команди.
`feature-build` і `feature-ship` — лише явним викликом (`disable-model-invocation`): одна пише код, друга комітить.

## Skills

| Skill | Тригери |
|---|---|
| `feature-plan` | «хочу ендпоінт …», «нова фіча …», новий GET тієї ж форми, що `GET /api/v1/igdb-games/{id}` |
| `feature-build` | Тільки явно, після підтвердженого `/feature-plan` |
| `feature-ship` | Тільки явно, коли зібрану фічу треба закомітити |
| `debug-recognition` | Обкладинку впізнано неправильно: `not_recognized`, не та гра, не та консоль, немає обкладинки; «чому не впізнало», «почему не распозналось». Лише читання, правила збігу не змінює |

## Hooks

| Подія | Matcher | Умова | Що робить |
|---|---|---|---|
| `PreToolUse` | `Write\|Edit\|MultiEdit` | Правка `*.py` у `src/` додає імпорт | `hooks/check_bc_imports.py` блокує (exit 2) імпорт, заборонений контрактами `[tool.importlinter]` з `pyproject.toml` |
| `PreToolUse` | `Bash` | Команда містить `git commit` | `hooks/commit_gate.sh` запускає `make lint` і `make test`; червоне — коміт заблоковано (exit 2), хвіст помилки повертається Claude |
| `PostToolUse` | `Write\|Edit` | Змінено `*.py` | `ruff format` + `ruff check --fix`; помилки, що лишилися (напр. F821), повертаються Claude |

Усі хуки працюють лише локально, мережевих викликів немає.
