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

---

# Investigation — 2026-08-24 (§2)

Asked to find what else writes to this store. `appInstallations` and `scriptTags`
are both **scope-denied**, so apps were identified indirectly.

## Apps evidenced by sales channels

Seven publications exist. Three are Shopify-native; four are third-party:

| Publication | Note |
|---|---|
| Online Store · Point of Sale · Shop | Shopify native |
| **Manus** | An app holding a sales channel. Unexplained — never mentioned in this project |
| **Facebook & Instagram** | Meta channel |
| **AfterShip for TikTok** | AfterShip |
| **Google & YouTube** | Google channel |

## Apps evidenced by metafield namespaces

| Namespace | App |
|---|---|
| `mm-google-shopping` (product) + `mm_google_shopping_extension` (shop, holds `merchant_id`) | Simprosys / MM Google Shopping |
| `shopify` (`fabric`, `age-group`, `target-gender`) | Shopify standard taxonomy |
| `custom`, `spec`, `hivolt` | Created by this project |
| `judgeme` (seen on deleted products) | Judge.me reviews |

### 🔴 German-language remnants

Three product metafield definitions are in German:

- `custom.groessentabelle` — "size chart"
- `custom.faq_passform` — "fit"
- `custom.faq_material` — "material"

Corroborated by traffic: **`/collections/damen`** ("ladies") drew 6 search
sessions in 90 days. A German-market configuration existed on this store. The
schema remnants survive. E15.

## Tapstitch — investigated as instructed

| | |
|---|---|
| Evidence | A delivery profile named `Tapstitch: Special Line` |
| Default profile? | **No.** The default `General profile` has one zone: United States |
| **Variants assigned** | **0** |
| Zones | ~71 single-country zones (Algeria, Argentina, Australia, Austria, Bahrain, Belgium, Bermuda, Bulgaria, Canada, Chile, China, Colombia…) |
| Sales channel | **None** — Tapstitch holds no publication |
| Metafield namespace | **None found** |
| Webhooks | Query returns empty — but webhook visibility is app-scoped, so this proves nothing |

**Assessment: the integration is inert, not active.** Zero variants are assigned
to its profile, so it currently governs no shipping for anything. A prior repo
note records it reactivating deactivated US rates on resync, so it is installed
rather than removed.

**On the SUPPLIER slot:** Tapstitch is print-on-demand. If it were adopted, POD
changes delivery and returns materially — per-item production time before
dispatch, and made-to-order items are conventionally excluded from
change-of-mind returns, which would conflict with the 60-day commitment already
published. **Not assumed to be the supplier. No delivery copy written from it.**

## Unexplained theme

`158753849576` "Copy of Impulse", UNPUBLISHED, created `2026-08-24T09:19:32Z` —
between this session's dev-theme creation (09:14:24) and its first settings push
(09:22:44). `updatedAt` is 17 seconds after creation, consistent with a
duplication completing and nothing since. **Not created by this session. Not
written to.**

## GemPages — fourth check

Still unverifiable. `appInstallations` scope-denied. No GemPages write to any
theme since the original install burst. `locales/en.default.json` still untouched
by me.

## What this adds up to

At least **eight** third-party integrations have or had write access to this
store, across at least **four unrelated commercial categories** (apparel,
perfume, children's games, supplements) and **two languages**. The theme is the
newest thing here; everything else carries sediment from previous businesses.
