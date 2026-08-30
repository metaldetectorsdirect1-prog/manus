# Live theme audit — 2026-08-30

## Target identification

Role read from Shopify's `role` field, not from the theme name or the prompt.

| Theme | ID | Role |
|---|---|---|
| HIVOLT — Nova Rebuild + Meta domain verification | `158911561960` | **MAIN** |
| HIVOLT — landing v2 dense (Claude, draft) | `158911987944` | UNPUBLISHED |

Adjudicated with `site/check-hivolt-theme-target.py --report`, exit 0.

The MAIN theme's `updatedAt` was `09:36:47Z`, seconds before the audit query.
A concurrent writer is active on this store.

## Finding 1 — six collection handles on the live homepage do not exist

`collectionByHandle` returns **null** for six handles the live homepage links to.

| Handle used live | Exists | Correct handle | Products |
|---|---|---|---|
| `dresses` | no | `dresses-1` | 149 |
| `knitwear` | no | `knitwear-sweaters` | 122 |
| `coats-jackets` | no | `womens-coats-jackets` | 153 |
| `denim` | no | `jeans-bottoms` | 117 |
| `tops` | no | `tops-blouses` | 74 |
| `loungewear` | no | `loungewear-sleep` | 61 |

Consequence on the live storefront:

- all three "Shop by category" tiles are dead links
- three of four Explore tiles are dead links
- the hero's second CTA is dead
- the Dress Edit banner's only CTA is dead
- the "Knitwear We Love" rail points at a non-existent collection

The replacement handles suggest the originals were deleted and recreated; the
new ones took suffixed handles and the homepage was never repointed.

**Correction (same day).** This table first recorded `loungewear` as having no
replacement. That was drawn from an exact-handle lookup only. A full collection
listing shows `loungewear-sleep` — "Loungewear & Sleep", 61 products. Every one
of the nine broken links has a correct target.

### Exact fix per broken link on theme `158911561960`

Confirmed on the live storefront: the "Knitwear We Love" rail renders empty.

| Section on homepage | Setting | Points at (missing) | Choose |
|---|---|---|---|
| Knitwear We Love | Collection | `knitwear` | **Knitwear & Sweaters** |
| Shop by category — Knitwear tile | Link | `knitwear` | **Knitwear & Sweaters** |
| Shop by category — Dresses tile | Link | `dresses` | **Dresses** |
| Shop by category — Outerwear tile | Link | `coats-jackets` | **Coats & Jackets** |
| Hero — second button | Link | `dresses` | **Dresses** |
| The Dress Edit banner — CTA | Link | `dresses` | **Dresses** |
| Explore — Denim tile | Link | `denim` | **Jeans & Trousers** |
| Explore — Tops tile | Link | `tops` | **Tops & Blouses** |
| Explore — Loungewear tile | Link | `loungewear` | **Loungewear & Sleep** |

Unaffected and working: the New This Week rail (`new-arrivals`, 1,618) and the
Explore Matching Sets tile (`sets`, 66).

The draft theme had inherited four of the same broken handles in its category
tiles and hero. That was introduced when the draft was built here, and is fixed.

## Finding 2 — announcement bar contradicts the refund policy

Live announcement block `a1`: *"60 days to return or exchange"*.

The published refund policy states: **"We do not process direct exchanges."**

The storefront promises a service the policy explicitly refuses. Corrected on
the draft to *"60 days to return. Free return label, full refund."*, which
matches the policy exactly.

## Finding 3 — production carries the unenriched Organization schema

`sections/hivolt-schema.liquid` on MAIN is 2,668 bytes: `name`, `url`, `email`
and a conditional logo. The enriched 3,371-byte version — `legalName`,
`telephone`, `PostalAddress`, `ContactPoint`, `areaServed` — exists only on the
draft. Since `settings.logo` is empty, the live Organization has no logo either.

## Finding 4 — identity and brand assets absent

From `config/settings_data.json` on MAIN:

| Setting | Value |
|---|---|
| `favicon` | `""` |
| `logo` (header) | `""` |
| `social_facebook_link` | `""` |
| `social_instagram_link` | `""` |
| `social_tiktok_link` | `""` |
| `social_pinterest_link` | `""` |
| `social_youtube_link` | `""` |

The footer renders three menus plus a newsletter, with payment icons and
copyright on. There is **no identity block** — no address, phone or email
visible anywhere on the storefront, though all three exist in the shop record
and in the policies.

## Finding 5 — the policies are complete, and better than assumed

An earlier note in this repo recorded the policy rewrites as blocked. That is
stale. All five policies are published and substantive:

- **Refund** — 60 days from delivery, sale items included, free prepaid label,
  no restocking fee, refund to original payment method in 5-7 business days,
  no exchanges.
- **Shipping** — free, no minimum, dispatch 2-4 business days, delivery 8-14
  after dispatch, 10-18 end to end. Discloses plainly that orders are
  dispatched by an overseas manufacturing partner rather than a US warehouse.
- **Contact** — email, phone, registered address, response within one business
  day, Mon-Fri 9am-5pm US Central.
- **Terms** — Illinois LLC, governing law, no subscriptions.

The `write_legal_policies` scope is still absent, so these cannot be edited
from here — but they do not need editing.

## Finding 6 — the Terms describe a different business

The Terms of Service state HIVOLT sells *"technical activewear and gym apparel:
tops, bottoms, sports bras, leggings, shorts, outerwear and matching sets"* and
that fibre composition and GSM fabric weight are published for each style.

The live catalogue is general fashion — dresses, coats, men's shirts, boots —
and most products carry no published fabric specification. The Terms and the
catalogue describe two different stores. Owner decision: narrow the catalogue
or update the Terms.

## Production writes are blocked at the connector

The Shopify MCP connector permits `themeFilesUpsert` on unpublished themes
only; writes targeting the live/MAIN theme are refused. Nothing was applied to
`158911561960`, and no theme was published or unpublished as a workaround.

Verified after the work: MAIN is still `158911561960`, still role `MAIN`, and
its `updatedAt` is unchanged at `09:36:47Z`.

## Applied to the draft `158911987944` (UNPUBLISHED)

| File | Before | After | Change |
|---|---|---|---|
| `templates/index.json` | 7,076 b | 7,094 b | 4 broken handles repaired; delivery window restored |
| `sections/header-group.json` | 1,451 b | 938 b | exchange promise removed |
| `sections/hivolt-schema.liquid` | 3,371 b | 3,371 b | unchanged — collateral check |

The delivery-window restoration corrects a regression introduced here: the
draft's brand story had dropped the live theme's *"arrives in 10-18 business
days"* disclosure. It is back, and matches the shipping policy.

Verified by independent read-back after the mutations returned — `userErrors:
[]` was not treated as evidence. Every rail handle re-checked against
`collectionByHandle`; all ten resolve and carry products. Draft role still
`UNPUBLISHED`.

## Smallest human action

Publish theme `158911987944` from Shopify admin (Online Store → Themes).
That is the only step this session cannot perform.

Still owner-side afterwards, all blocked on assets or data not held here:
favicon image, header logo, social profile URLs, footer identity block.
