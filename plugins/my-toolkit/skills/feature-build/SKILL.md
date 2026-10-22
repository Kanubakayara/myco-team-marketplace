---
name: feature-build
description: Build a confirmed /feature-plan in myco-ai in one pass — all layers, wiring and the three unit-test files — and loop make lint && make test until green. Use only after the user confirmed a plan from /feature-plan.
disable-model-invocation: true
allowed-tools: Read, Write, Edit, Grep, Glob, Bash(make lint), Bash(make test), Bash(date*)
---

# Збірка наскрізної фічі за підтвердженим планом

Без підтвердженого плану (`/feature-plan`) у розмові — зупинись і запропонуй спершу його.

## Як писати файли

- PostToolUse-hook запускає `ruff check --fix` після **кожної** правки. Імпорт, доданий окремою
  правкою раніше за використання, він видалить як невикористаний, а використання до імпорту дасть F821.
  Тому: **новий файл і будь-який файл, де змінюються імпорти, — `Write` цілком**.
  `Edit` — лише для правок без нових імпортів.
- Факти — лише з джерела (поля з live probe). Немає в джерелі → `None` / порожній tuple.
- Коментар — лише «чому», без історії змін.

## Порядок (один прохід, без зупинок між шарами)

1. **domain** — frozen dataclass у `models.py`; метод порту в `ports.py`. Тільки stdlib.
2. **infrastructure** — метод адаптера через спільний `_query` (retry на 401 вже там);
   розбір рядка в окремій `_to_<entity>`; хелпери `_names`, `_release_date`, `_cover_url` — перевикористати.
3. **application** — `application/<verb>_<entity>.py`: спершу `self._catalog.consoles()`
   (перевірка токена myco), потім порт. Один публічний метод `execute`.
4. **presentation** — схема `<Entity>Out(_FromDomain)` у `schemas.py`; окремий файл роутера
   `presentation/api/<resource>.py` з `create_<resource>_router(make_use_case)`:
   `bearer_token` → use case → `CatalogUnauthorized` = 401, `None` = 404.
5. **main.py** — `make_<use_case>(token)` через `catalog_for(token)` і спільний `igdb`; `include_router`.
6. **tests/unit/** — три файли за шаблонами еталона:
   - адаптер: `httpx.MockTransport`; мапінг повного рядка, порожні поля, порожня відповідь, текст запиту;
   - use case: fake-порти; результат, порожній результат, відхилений токен не доходить до джерела;
   - роутер: `TestClient` + fake use case; 200 (точний JSON), 404, 401 без токена, 401 від myco, 422.
7. **Перевірка** — `make lint && make test`. Червоне → виправ і повтори, максимум 3 кола;
   далі — зупинись і покажи помилку.

## Наприкінці

- Коротко: які файли, скільки тестів (було → стало), час (`date +%H:%M`).
- Дай людині **один** однорядник live-перевірки нового методу адаптера з префіксом `!`
  (як у `/feature-plan`, але виклик публічного методу). Наступний крок — `/feature-ship`.
