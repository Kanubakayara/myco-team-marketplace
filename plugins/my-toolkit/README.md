# my-toolkit

## Purpose

Набір інструментів Claude Code для сервісу myco-ai (Python, FastAPI, полегшена Clean Architecture).
Допомагає додавати адаптери в `recognition/infrastructure`, розбирати невдалі розпізнавання
обкладинок і не дає порушити dependency rule або стиль коду під час правок.

## Install

З marketplace:

```text
/plugin install my-toolkit --marketplace Kanubakayara/myco-team-marketplace
```

Локальна перевірка без встановлення:

```bash
claude --plugin-dir ./plugins/my-toolkit
```

Для всієї команди — встановити зі scope `project`, щоб запис потрапив у `.claude/settings.json`:

```bash
claude plugin install my-toolkit --scope project
```

Потрібно: `uv`, `jq`, віртуальне оточення проєкту `.venv` (`make install`).

## Commands

| Команда | Що робить |
|---|---|
| `/my-toolkit:scaffold-adapter` | Новий адаптер у `recognition/infrastructure` під domain-порт: адаптер, unit-тест, експорт, wiring у `main.py` |
| `/my-toolkit:hello <ім'я>` | Привітання українською у двох реченнях (перевірка, що плагін підключився) |

## Skills

| Skill | Коли спрацьовує |
|---|---|
| `/my-toolkit:debug-recognition` | Обкладинку впізнано неправильно: `not_recognized`, не та гра, не та консоль, немає обкладинки. Діагностика етапів конвеєра лише читанням, правила збігу не змінює |

## Hooks

| Подія | Matcher | Що робить |
|---|---|---|
| `PreToolUse` | `Write\|Edit\|MultiEdit` | `hooks/check_bc_imports.py` блокує правку, яка додає імпорт, заборонений контрактами `[tool.importlinter]` з `pyproject.toml` (exit 2) |
| `PostToolUse` | `Write\|Edit` | Для `*.py`: `ruff format` + `ruff check --fix`; помилки, які лишилися, повертаються Claude |

Обидва хуки працюють лише локально, мережевих викликів немає.
