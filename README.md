# myco-team-marketplace

## Що це

Marketplace плагінів Claude Code для команди платформи myco. Звичайне git-репо: маніфест
`.claude-plugin/marketplace.json` у корені, плагіни — у `plugins/<name>/`. Релізи — git-теги
`<plugin>@<version>`, версії — semver.

## Як додати у Claude Code

```text
/plugin marketplace add Kanubakayara/myco-team-marketplace
/plugin install my-toolkit@myco-team
```

Щоб marketplace пропонувався автоматично всім, хто клонує проєкт, додайте в `.claude/settings.json`
цього проєкту:

```json
{
  "extraKnownMarketplaces": {
    "myco-team": {
      "source": { "source": "github", "repo": "Kanubakayara/myco-team-marketplace" }
    }
  }
}
```

Оновлення: `/plugin marketplace update myco-team`, потім `/plugin update my-toolkit@myco-team`.

## Список плагінів

| Плагін | Версія | Що робить |
|---|---|---|
| [`my-toolkit`](plugins/my-toolkit/README.md) | 2.0.0 | myco-ai: наскрізна фіча за три команди (`feature-plan` / `-build` / `-ship`), scaffold адаптерів, діагностика розпізнавання, хуки dependency rule, ruff і commit gate |

## Супровідники

| Зона | Хто |
|---|---|
| Увесь репо, `plugins/my-toolkit/` | @Kanubakayara |

Маршрут review — у [`.github/CODEOWNERS`](.github/CODEOWNERS).

## Як контриб'ютити

1. Гілка від `main`, плагін у `plugins/<name>/` з `.claude-plugin/plugin.json` і `README.md`.
2. Запис у `plugins[]` маніфесту: `name`, `source: ./plugins/<name>`, `description`, `version`,
   `category`, `tags`, `strict: true`.
3. `version` у `plugin.json` і в `marketplace.json` — однакова (CI це перевіряє).
   Breaking change — лише major bump.
4. Запис у [`CHANGELOG.md`](CHANGELOG.md) (Keep a Changelog, секція `### Breaking` зверху).
5. Локально: `claude plugin validate --strict .` і `claude plugin validate --strict ./plugins/<name>`.
6. PR → зелений CI + approve від CODEOWNERS → merge → тег `git tag -a <name>@<version>` і `git push --tags`.

## Контакти

- Питання та пропозиції — GitHub Issues цього репо.
- Вразливості — лише за процедурою з [`SECURITY.md`](SECURITY.md), не в публічних issues.
- Розсилка супровідників: freezonexhome@gmail.com
