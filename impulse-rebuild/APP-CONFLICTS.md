# APP-CONFLICTS.md

Apps with write access to theme files. §4.5 requires these paused for the build
or they will overwrite it.

## GemPages — CONFIRMED WRITER, ACTIVE

Five files it owns on the published theme:

| File | Modified |
|---|---|
| `layout/theme.gempages.blank.liquid` | `23:17:34Z` |
| `layout/theme.gempages.footer.liquid` | `23:17:34Z` |
| `layout/theme.gempages.header.liquid` | `23:17:34Z` |
| `assets/gp-global.css` (68 KB) | `23:17:33Z` |
| `sections/gp-variant-selected.liquid` | `23:17:37Z` |

The base Impulse install finished at `23:17:01Z`. **Every GemPages file is
stamped 32–36 seconds later**, so GemPages wrote into the theme immediately
after install and is live now.

**Action required before Phase 3:** pause GemPages, or scope it away from the
rebuild theme. Any homepage or template work will otherwise be overwritten.

A prior repo note also records GemPages owning most of
`locales/en.default.json` — that file is stamped `23:17:36Z`, consistent with
GemPages, not the base install. **Do not push `locales/en.default.json`.**

## Judge.me — previously present, now unverified

Earlier product records carried `judgeme.badge`, `judgeme.widget` and
`judgeme.review_widget_data` metafields. With zero products remaining, its
current state cannot be confirmed. Relevant to §9.6 (review section wired but
empty-state designed) once products exist.
