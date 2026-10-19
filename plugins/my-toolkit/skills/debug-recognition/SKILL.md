---
name: debug-recognition
description: Diagnose why a cover photo was recognized wrong in myco-ai. Use when POST /api/v1/recognitions or the demo page returned not_recognized, igdb_candidates or catalog_candidates instead of found, picked the wrong game, wrong console or no cover, or when the user asks "чому не впізнало", "почему не распозналось", "не та гра", "не та консоль", "немає обкладинки". Read-only triage of the pipeline stages; does not change matching rules.
allowed-tools: Read, Grep, Bash(uv run *)
---

# Діагностика розпізнавання

Мета — назвати **етап**, на якому результат розійшовся з очікуваним, і **причину**.
Код і правила збігу не міняємо: лише діагноз і пропозиція, що правити.

Конвеєр — `src/myco_ai/recognition/application/identify_game.py`:

```text
consoles() → CoverReader.read → find_console → catalog.search + is_exact_title → GameSource.search → статус
```

## Checklist

- [ ] **1. Зібрати вхід.** Попроси JSON-відповідь ендпоінта (поля `status`, `cover`, `console`,
      `catalog_games`, `igdb_games`) і що людина *очікувала* (назва, консоль). Без відповіді — не вгадувати.
- [ ] **2. Етап «читання обкладинки».** Подивись `cover`:
  - `title` або `platform` порожні → статус `not_recognized` ще до пошуку. Причина — фото
    (відблиск, кут, обрізано), а не матчинг. Далі не йти.
  - `edition` заповнене («Game of the Year», «Deluxe»)? Запам'ятай — див. gotcha 1.
- [ ] **3. Етап «консоль».** `console` = null при заповненому `cover.platform` → `find_console`
      не знайшов консоль у каталозі myco. Порівняй надруковане з назвами/alias консолей (gotcha 3).
- [ ] **4. Етап «каталог myco».** Статус `catalog_candidates` або `igdb_candidates`:
  - перевір, чи гра є в каталозі **саме для цієї консолі** — фільтр `console.id in g.console_ids`;
  - порівняй `normalize(назва в каталозі)` з `normalize(title + edition)` — це строгий збіг;
  - чи знаходить myco гру за найдовшим словом `title` (gotcha 2).
- [ ] **5. Етап «IGDB».** Якщо кандидатів IGDB немає або вони дивні — запусти пошук руками:

      uv run --env-file .env python scripts/igdb_search.py "<title + edition з cover>"

      Порожньо → IGDB не знає такої назви; 401 → gotcha 6.
- [ ] **6. Обкладинка.** `found`, але в грі і `cover_url`, і `igdb_cover_url` порожні → `igdb_cover_for` (gotcha 4).
- [ ] **7. Висновок.** Один абзац: етап → причина → що робити (переробити фото / додати гру
      чи консоль у каталог myco / змінити правило в `domain/matching.py` — останнє лише після
      згоди людини, з unit-тестом у `tests/unit/test_matching.py`).

## Gotchas

1. **Строгий збіг з edition.** `is_exact_title` порівнює каталог із `title + edition`. Claude
   прочитав «Game of the Year Edition», а в каталозі просто «Alien: Isolation» → не `found`, а
   `catalog_candidates`. Це навмисно (сумнів = немає збігу), не баг.
2. **Пошук у каталозі — за найдовшим словом.** myco шукає SQL `LIKE`, а обкладинка губить
   пунктуацію каталогу («Mass Effect Andromeda» проти «Mass Effect: Andromeda»), тому
   `catalog_query` віддає лише найдовше слово назви. myco повертає до 20 ігор на сторінку:
   якщо слово надто поширене, потрібна гра може не потрапити в першу сторінку.
3. **Консоль.** Ключ консолі: `playstation` → `ps`, далі точний збіг або **найдовший префікс**.
   «PS4 Pro» знайде «PS4»; надруковане «PlayStation VR» може зачепити не ту консоль.
4. **Немає обкладинки — навмисно.** `igdb_cover_for` повертає `None`, якщо підходять дві різні
   обкладинки IGDB (та сама назва, рік збігся або невідомий). Обкладинка йде в каталог myco,
   тож краще жодної, ніж чужа.
5. **`FixtureMissError`** у тестах/evaluation: фікстура ключується sha256 фото. Пересохранення,
   зрізаний EXIF чи пересилка через месенджер змінюють хеш — потрібен *той самий* файл.
6. **IGDB 401.** Twitch-токен живе ~60 днів; адаптер оновлює його **один раз** на 401. Якщо 401
   повторюється — невірні `IGDB_CLIENT_ID` / `IGDB_CLIENT_SECRET`, а не протухлий токен.
7. **401 від самого ендпоінта** — це токен myco користувача: `consoles()` іде першим, щоб не
   витрачати Claude на невалідний токен. До розпізнавання справа не дійшла.

## Не робити

- Не читати `.env` (заборонено в `.claude/settings.json`) — назви змінних є в `main.py`.
- Не викликати Claude vision для «перевірки» — це коштує токенів; дані обкладинки вже є у відповіді.
- Не пропонувати «найближчий кандидат на око» як відповідь — правило контексту `recognition`.
