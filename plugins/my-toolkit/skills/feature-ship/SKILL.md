---
name: feature-ship
description: Ship a built myco-ai feature — update ARCHITECTURE.md and .claude/rules/recognition.md, run lint and tests, commit, and record the commit in LOG.md. Use only when the user asks to commit a feature built with /feature-build.
disable-model-invocation: true
allowed-tools: Read, Edit, Bash(make lint), Bash(make test), Bash(git status*), Bash(git diff*), Bash(git add*), Bash(git commit*), Bash(git log*), Bash(date*)
---

# Коміт фічі

1. **Документація** (українською, по одному рядку, без «полотна»):
   - `ARCHITECTURE.md`, таблиця «Де яка логіка живе»: новий use case у рядку application,
     новий ендпоінт у рядку presentation;
   - `.claude/rules/recognition.md`: метод порту в «Порти», use case у «Use case»,
     ендпоінт у «Демо (presentation)» — метод, шлях, авторизація, коди відповіді.
2. **Перевірка** — `make lint && make test`. Червоне → не комітити, показати помилку.
3. **Коміт** — `git add` лише файли фічі (src, tests, два документи; **не** `LOG.md`).
   Повідомлення: `feat(recognition): <METHOD> <path> <що повертає>`, тіло — 2–3 рядки «навіщо».
   Якщо фічу зроблено командами цього плагіна — рядок
   `Created with my-toolkit: /feature-plan, /feature-build, /feature-ship`.
   Наприкінці — `Co-Authored-By`, якщо його вимагає system reminder сесії.
4. **LOG.md** (гілки `feature-*`): рядок у «Коміти» — час, короткий hash, subject,
   метрика (тести passed / хвилин від старту фічі); заповнити час до зеленого тесту, якщо порожній.
   Окремий коміт `docs(log): <фіча> metrics`.
5. **Не пушити.** Запитати людину про push і PR.
