# Changelog

Формат — [Keep a Changelog](https://keepachangelog.com/uk/1.1.0/), версії — [SemVer](https://semver.org/).
Записи групуються за плагіном; секція `### Breaking` завжди перша.

## my-toolkit

### [2.0.0] — 2026-10-22

#### Breaking

- Видалено `/my-toolkit:hello` — до проєкту не стосувалась.

#### Added

- Skill `feature-plan` — план наскрізного зрізу по шарах, допущення, live probe джерела до коду.
- Skill `feature-build` — усі шари, wiring і три тест-файли за один прохід до зелених `make lint && make test`.
- Skill `feature-ship` — документація, lint + тести, коміт з позначкою плагіна, рядок у `LOG.md`.
- Хук `PreToolUse` (`Bash`): `git commit` блокується, поки `make lint` або `make test` червоні.
- `LICENSE` (MIT).

#### Changed

- README плагіна: секції Purpose / Install / Commands / Skills / Hooks.

### [1.0.0] — 2026-10-19

#### Added

- `/my-toolkit:scaffold-adapter` — новий адаптер у `recognition/infrastructure` під domain-порт.
- `/my-toolkit:hello` — перевірка, що плагін підключився.
- Skill `debug-recognition` — діагностика невдалого розпізнавання обкладинки.
- Хук `PreToolUse`: блокує імпорти, заборонені контрактами import-linter.
- Хук `PostToolUse`: `ruff format` + `ruff check --fix` для `*.py`.
