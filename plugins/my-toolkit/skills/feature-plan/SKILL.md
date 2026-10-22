---
name: feature-plan
description: Plan a new vertical slice in myco-ai (domain dataclass → port → adapter → use case → GET endpoint + schema → tests) before any code. Use when the user asks for a new endpoint or feature of the same shape as GET /api/v1/igdb-games/{id}, e.g. "хочу ендпоінт ...", "нова фіча ...", "/feature-plan". Produces a plan by layers, assumptions and a live probe of the source; writes no code.
argument-hint: <що має повертати ендпоінт і навіщо>
allowed-tools: Read, Grep, Glob, Bash(git status*), Bash(git switch*), Bash(git log*), Bash(date*)
---

# План наскрізної фічі

Запит: `$ARGUMENTS`. Якщо з нього незрозуміло, **що** повертає ендпоінт і **з якого джерела**
(IGDB / каталог myco) — спитай одним питанням і зупинись.

Еталон форми — фіча `GET /api/v1/igdb-games/{id}` (коміт `6dcf995`). Прочитай ці файли, перш ніж
планувати, і повтори їхню форму, а не вигадуй нову:

| Шар | Еталон |
|---|---|
| domain | `domain/models.py` (`GameDetails`), `domain/ports.py` (`GameSource.details`) |
| infrastructure | `infrastructure/igdb/game_source.py` (`details`, `_query`, `_to_details`) |
| application | `application/get_igdb_game.py` |
| presentation | `presentation/api/igdb_games.py`, `presentation/api/schemas.py`, `presentation/api/auth.py` |
| wiring | `main.py` (`make_get_igdb_game`, `include_router`) |
| tests | `tests/unit/test_igdb_game_details.py`, `test_get_igdb_game.py`, `test_igdb_games_router.py` |

Усі шляхи — від `src/myco_ai/recognition/`, крім `main.py` і `tests/`.

## Кроки

1. **Гілка.** Якщо поточна гілка `main` — запропонуй `feature-N/<slug>` і створи її після «так».
   У гілках `feature-*` веди `LOG.md` за правилом з `CLAUDE.md` (цей prompt — перший рядок).
2. **План по шарах** — таблиця «шар → файл → нове / змінене → що саме». Нова сутність, поле
   чи метод порту — позначити явно: за правилом 8 `CLAUDE.md` це питання до людини.
3. **Live probe джерела.** Назви полів зовнішнього API не вгадуємо. Дай людині **один**
   однорядник із префіксом `!` (`.env` Claude недоступний), який друкує сирий JSON джерела, напр.:
   `! uv run python -c "import httpx, json; from myco_ai.main import Settings; from myco_ai.recognition.infrastructure.igdb import IgdbGameSource; s = Settings(); print(json.dumps(IgdbGameSource(s.igdb_client_id, s.igdb_client_secret, httpx.Client(timeout=30))._query('fields ...; where ...;'), indent=1)[:3000])"`
4. **Допущення** — нумерований список, 3–6 пунктів: авторизація (за замовчуванням — як в еталоні:
   токен myco через `catalog.consoles()`), 404 / порожній результат, що не робимо.

Зупинись і чекай підтвердження плану й виводу probe. Код не пиши — це `/feature-build`.
