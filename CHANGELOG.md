# Changelog

Формат — [Keep a Changelog](https://keepachangelog.com/uk/1.1.0/), версії — [SemVer](https://semver.org/).
Записи групуються за плагіном; секція `### Breaking` завжди перша.

## my-toolkit

### [1.0.0] — 2026-10-19

#### Added

- `/my-toolkit:scaffold-adapter` — новий адаптер у `recognition/infrastructure` під domain-порт.
- `/my-toolkit:hello` — перевірка, що плагін підключився.
- Skill `debug-recognition` — діагностика невдалого розпізнавання обкладинки.
- Хук `PreToolUse`: блокує імпорти, заборонені контрактами import-linter.
- Хук `PostToolUse`: `ruff format` + `ruff check --fix` для `*.py`.
