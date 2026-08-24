# LEGACY-AUDIT.md

Legacy contamination sweep of every shop-level surface, per Track A §3.1.
**Nothing was deleted, changed, or created — this is read-only.** Classification
only: **keep · redirect · delete · needs owner decision**.

---

## §0 Method (per standing rule §1.3)

| | |
|---|---|
| **Read on** | 2026-08-24, live Shopify Admin GraphQL, this session |
| **Store** | HIVOLT · `hivolt-usa.com` · `f36zps-yd.myshopify.com` |
| **Surfaces swept** | URL redirects · pages · collections · menus · metafield definitions · metaobject definitions · files · locales · markets · shop policies · themes |
| **Counts are** | full enumerations, not samples, not extrapolations |
| **Second method** | every bucket total re-derived with `urlRedirectsCount(query:)` and reconciled against the row dump; both agree exactly (see §2.1) |
| **Not swept** | the 501 blog articles individually (`BLOG-AUDIT.md`); theme file internals (`AUDIT.md`) |
| **Falsifiable by** | re-running the same queries; any count that moves means the store changed under us |

---

## §1 Three findings that outrank the redirect table

### 1.1 🔴 The catalog is empty. Zero products.

```
productsCount           → 0
products(first: 5)      → []          (second method)
productVariantsCount    → 0           (third method)
```

All **fifteen** collections return `productsCount: 0`. Nothing to sell, nothing
for a PDP to render, nothing behind the fourteen redirects pointing at
`/collections/mens-golf-polos`. This is why Track B is blocked — and why this is
the **cheapest possible moment to clean up**: every metafield definition below has
zero values attached, so removing one destroys no data.

### 1.2 🔴 The shipping figures ruled out for reuse are live in three shop policies

The brand block said, verbatim:

> `REAL_SHIPPING_TIMES: <<DERIVE from supplier once selected — do not reuse the existing 2–4 / 8–14 figures>>`

Those exact figures are published right now in **shop policies**, which I had not
previously audited. Policies are not pages: they are linked from four footer menus,
served under `/policies/*`, and surfaced inside Shopify checkout.

| Policy | Claim | Class |
|---|---|---|
| Shipping | "dispatched … within 2-4 business days" | **UNSOURCED** |
| Shipping | "8-14 business days after dispatch" | **UNSOURCED** |
| Shipping | "ship via USPS or UPS depending on your address" | **UNSOURCED** |
| Shipping | "tracking link … within 24 hours of dispatch"; "24-48 hours for the first carrier scan" | **UNSOURCED** |
| Shipping | "not arrived within 14 business days … we will replace the order or refund it in full" | **UNSOURCED** |
| Terms §5 | "dispatched within 2-4 business days and delivered within 8-14 business days" | **UNSOURCED** |
| Contact | "dispatched in 2-4 business days and delivered in 8-14 business days" | **UNSOURCED** |
| Contact | "Response Time: Within one business day" | **UNSOURCED** |
| Refund | "We reply within one business day with a prepaid return label" | **UNSOURCED** |
| Refund | "Refunds … within 5-7 business days of your return reaching us" | **UNSOURCED — and contradicts the live Returns page** |
| Refund | "cancelled at no cost before they enter production … within 12 hours" | **UNSOURCED** |
| Refund | "Email … within 30 days of delivery with photographs" | **UNSOURCED** |

**The contradiction is the sharpest item.** The owner supplied *refund within 5
business days* and `/pages/returns-refunds` now says 5 — the Refund **policy** still
says **5-7**. Two numbers for the same promise are live simultaneously.

Three further defects in the same policies:

- **Terms §1** — *"HIVOLT is a single member limited liability company registered in
  Illinois"*, and **Contact** gives the registered business name as *"HIVOLT"*. The
  owner-supplied entity is **Dn Global Trading LLC**. A registered-entity claim that
  does not match the entity is the one error here with direct legal weight.
- **Terms §1** — *"We publish the fibre composition and fabric weight in grams per
  square metre for each style, taken from the supplier specification sheet."* With
  zero products and no supplier, this describes something that does not happen.
- **Terms §1** scopes the business as *"technical activewear and gym apparel"*, which
  no longer matches the women's-clothing brief.

**This is the fifth fabrication surface §1.8 told me to assume existed** — and the
largest, because policy text is legally operative and reaches checkout.
**Classified: needs owner decision**; §1.2 bars me from rewriting any of it.

### 1.3 🟠 Unpublishing `shipping-delivery` created four dead menu links — mine

Executing §2 this session set `/pages/shipping-delivery` to `isPublished: false`.
It is still linked from:

| Menu | Item |
|---|---|
| `footer` → Help | "Shipping & delivery" |
| `footer-help` | "Shipping & Delivery" |
| `footer-legal` | "Shipping & Delivery" |
| — plus | `/pages/versand-lieferung` redirect targets it |

The register predicted this cost and the instruction accepted it, so the unpublish
stands — but the links are live 404s today. **The fix is menu edits, not a
re-publish**: the page's figures are the ones ruled out for reuse. See §11.

---

## §2 URL redirects — all 331

### 2.1 Reconciliation

| Bucket | Count | Method |
|---|--:|---|
| **Total** | **331** | `urlRedirectsCount` |
| `/de*` | 242 | query count |
| ├ `/de/blogs/news*` | 170 | query count |
| ├ `/de/products*` | 51 | query count |
| ├ `/de/pages*` | 8 | query count |
| ├ `/de/collections*` | 8 | query count |
| ├ `/de/policies*` | 2 | query count |
| └ `/de`, `/de/cart`, `/depages/…` | 3 | remainder |
| **Non-`/de`** | **89** | 331 − 242 |
| ├ `/products*` | 46 | query count |
| ├ `/collections*` | 18 | query count |
| ├ `/pages*` | 14 | query count |
| ├ `/blogs*` | 4 | query count |
| └ root-level oddments | 7 | remainder |

Both remainders land exactly (3 and 7), and the named rows in the dump match them
one-for-one. **The table closes. No redirect is unaccounted for.**

### 2.2 🔴 Correction to `LOCALE-AUDIT.md`

`LOCALE-AUDIT.md` concluded that *"the German article corpus is not a live mirror
requiring parallel maintenance."*

**That conclusion was wrong.** There are **170** `/de/blogs/news/*` → `/blogs/news/*`
redirects: the German blog **was** a full mirror. What holds is the practical
effect — the mirror is **already fully redirect-covered**, so the prune needs no
separate German arm. Deleting an English article breaks its German redirect's
*target*; no German article needs deleting.

Method: 170 is a query count over the live redirect set, not an extrapolation.
Falsified if `urlRedirectsCount(query:"path:/de/blogs/news*")` returns anything else.

### 2.3 Classification

| # | Group | n | Class | Reasoning |
|---|---|--:|---|---|
| R1 | `/de/blogs/news/*` → `/blogs/news/*` | 170 | **keep, then remap in the prune** | Locale `de` is `published: false`, but these preserve link equity from a corpus that was indexed. Each one whose target gets deleted must be repointed, not orphaned. |
| R2 | `/de/products/*` → `/products/*` | 51 | **keep** | Zero cost, no conflict. Targets are already dead (no products), so they resolve to the catch-all. |
| R3 | `/de/{pages,collections,policies}/*` | 18 | **keep** | Same. |
| R4 | Six prior businesses → `/collections/all` or `/blogs/news` | 21 | **keep** | See §2.4. Cheapest possible handling of six dead catalogs. |
| R5 | → `/collections/mens-golf-polos` | 14 | **needs owner decision** | See §2.5. Points women's URLs at a men's collection. |
| R6 | Product-rename chains within the activewear catalog | ~30 | **keep** | Normal normalization history. |
| R7 | German page handles (`ueber-uns`, `impressum`, `widerrufsbelehrung`, `versand-lieferung`) | 4 | **keep** | `versand-lieferung` now targets an unpublished page — fold into the §1.3 fix. |
| R8 | Broken or stale targets | 4 | **delete or repoint** | See §2.6. |
| R9 | Marketing short links (`/tiktok`, `/tt`, `/s/9c9bcd`, `/about`) | 4 | **keep** | Functional. `/tiktok` and `/tt` point at `/collections/sets`, currently empty. |
| R10 | `/google6945ed5c46bc40d8.html` → verification page | 1 | **keep** | Search Console ownership token. Deleting it can drop verification. |

### 2.4 Six prior businesses, confirmed by redirect evidence

The 21 redirects to `/collections/all` and `/blogs/news` are the fossil record of
what this store was before HIVOLT activewear:

| Business | Evidence |
|---|---|
| **Perfume** — Roxelis / Auria | `roxelis-original`, `roxelis-jasmine`, `roxelis-paris`, `roxelis-build-your-own-bundle`, `auria-pheromone-roll-on`; scent collections `original-scent`, `jasmine-scent`, `paris-scent`, `sweet-peaches-scent`, `complete-collection` |
| **Supplements** — HIVOLT Collagen | `hivolt-collagen-peptides`, `-1`, `hivolt-collagen-power-bundle`, `hivolt-starter-kit` |
| **Children's games** — Focus Foxes | `focus-foxes-print-play-…`, `focus-foxes-ultimate-bundle-…`, `/pages/about-focus-foxes` |
| **Watches** — Auralux | `auralux-wake-silent-alarm-watch`, `/collections/wake-up-better`, `/pages/100-day-wake-up-guarantee` |
| **Bags** — Auralux / Hilvolt Vault | `auralux-vault-anti-theft-sling-bag`, `hilvolt-vault-…`, `/collections/carry-smarter` |
| **Wellness** | `the-calm-reset-toolkit` |
| **Apparel (German-market)** | `/collections/damen`, `/collections/herren`, `/pages/ueber-uns`, `/pages/impressum` |

Seven distinct prior positionings, not six. All correctly parked. **Keep.**
Note `/pages/30-day-risk-free-guarantee` and `/pages/100-day-wake-up-guarantee` both
redirect to `/pages/60-day-love-it-guarantee` — three guarantee lengths in this
store's history.

### 2.5 🟠 The fourteen `mens-golf-polos` redirects

`/collections/mens-golf-polos` is titled *"The Polo Collection"* and holds **zero
products**. Fourteen redirects point into it, including these, which are wrong on
their face for a women's store:

| Path | Problem |
|---|---|
| `/products/voltcore-2-piece-set-twist-front-bra-flare-leggings` | A **women's** two-piece set → a **men's** collection |
| `/products/womens-slim-fit-quarter-zip-polo-shirt` | Women's → men's |
| `/collections/damen` | German for **women** → men's collection |
| `/products/amelia-linen-shift-dress` | A dress → men's polos |
| `/pages/voltcore` | The Voltcore page → men's polos |
| `/collections/complete-collection` + 4 scent collections | Perfume → men's polos |

Two of these are also **two-hop chains**: `/de/products/womens-slim-fit-quarter-zip-polo-shirt`
→ `/products/womens-slim-fit-quarter-zip-polo-shirt` → `/collections/mens-golf-polos`.

**Needs owner decision.** The correct target depends on what replaces the polo
collection in the women's IA — a Track B question. Repointing now would mean
inventing a destination.

### 2.6 Broken or stale — the only rows I would delete

| Path | Target | Defect | Class |
|---|---|---|---|
| `/depages/60-day-love-it-guarantee` | `/pages/60-day-love-it-guarantee` | Malformed source — `/de` + `pages` with no slash. Unreachable by any real link. | **delete** |
| `/collections/tennis-amp-court` | `/collections/tennis-and-court` | **Target does not exist.** Not among the fifteen collections. Redirect to a 404. | **repoint or delete** |
| `/de/collections/bottoms` | `/collections/bottoms` | **Target does not exist.** | **repoint or delete** |
| `/collections/new-arrivals` | `/collections/drop-04-voltcore` | **Target does not exist.** | **repoint or delete** |
| `/favicon.ico`, `/favicon.png` | `…/hivolt-logo.png?v=1785381663` | Points at the **deprecated** logo, superseded by `hivolt-badge.png`. Favicon is set in theme settings anyway. | **delete** |

Also `/de/collections/drop-04-voltcore.atom` (dead RSS feed for a collection that
does not exist) and `/de/collections/mens-activewear` → `/collections/mens-activewear`,
which itself redirects onward to `mens-golf-polos` — a third two-hop chain.

### 2.7 An unidentified SEO app left a signature

At least **34 redirect targets carry a `#seotid…` URL fragment** — e.g.
`/pages/size-guide#seotidkmjYiO2jB`. That is an app's tracking marker written into
redirect targets, not something a human types.

**Method note:** 34 is a floor, not a total. The Admin API's redirect query filter
does not index URL fragments — `urlRedirectsCount(query:"target:*seotid*")` returns
**0**, which is a filter limitation, not a real count. 34 is the number I counted in
the returned rows. **The true total is ≥34 and I cannot derive it by query.**

A fourth unidentified integration alongside those in `APP-CONFLICTS.md`. The
fragments are harmless to visitors (browsers ignore an unmatched fragment) but mean
an app had write access to redirects. **Keep; investigate ownership.**

---

## §3 Pages — all 18

| Handle | Title | Pub | Class |
|---|---|:--:|---|
| `about-us` | Our Mission | ✅ | keep — rewrite queued (§3.3) |
| `faq` | Help Center | ✅ | keep — expand to 18+ |
| `contact-us` | Contact Us | ✅ | keep |
| `returns-refunds` | Returns & Refunds | ✅ | keep — **provisional**, see CLAIMS-REGISTER |
| `terms-of-service` | Terms of Service | ✅ | **needs owner decision** — entity-name defect |
| `accessibility` | Accessibility Statement | ✅ | keep |
| `track-order` | Track Your Order | ✅ | keep |
| `materials-sustainability` | Materials & Specifications | ✅ | **needs owner decision** — describes a spec regime with zero products |
| `60-day-love-it-guarantee` | 60-Day Love-It Guarantee | ✅ | keep — owner-confirmed |
| `data-sharing-opt-out` | Your Privacy Choices | ✅ | keep — Shopify-required |
| `google-site-verification` | Google Site Verification | ✅ | keep — deleting can drop Search Console |
| `size-guide` | **Size Guide — Men's Polos** | ✅ | 🟠 **needs owner decision** — a men's polo size guide, published, linked from **five** menus, in a women's store |
| `shipping-delivery` | Shipping & Delivery | ❌ | unpublished this session — **menu links must follow** (§1.3) |
| `voltcore` | Voltcore 2-Piece Set | ❌ | keep unpublished — **redirect conflict**, see §3.1 |
| `fabric-weight-index` | Fabric Weight Index | ❌ | keep unpublished — **redirect conflict** |
| `size-chart` | Size Chart | ❌ | keep unpublished — **redirect conflict** |
| `size-guide-women` | Size Guide — Women | ❌ | keep unpublished — fabricated measurements, CLAIMS row 1 |
| `size-guide-men` | Size Guide — Men | ❌ | keep unpublished — fabricated measurements, CLAIMS row 2 |

### 3.1 🟠 Three redirect ↔ page handle collisions

A Shopify URL redirect only fires on a **404**. These three handles have *both* a
redirect and a real page:

| Handle | Redirect exists | Page exists | Behaviour today | If the page is ever published |
|---|---|---|---|---|
| `size-chart` | → `/pages/size-guide` | unpublished | redirect fires | **redirect silently stops firing** |
| `fabric-weight-index` | → `/pages/materials-sustainability` | unpublished | redirect fires | redirect silently stops firing |
| `voltcore` | → `/collections/mens-golf-polos` | unpublished | redirect fires | redirect silently stops firing |

A latent trap: publishing any of those three pages silently changes routing
elsewhere, with no warning and no error. **Flag before any publish.**

### 3.2 The published men's polo size guide

`/pages/size-guide` is titled *"Size Guide — Men's Polos"*, is **published**, and is
linked from `main-menu`, `footer` → Specs, `footer-shop`, `footer-about` and
`footer-help`, plus the `/pages/fit-quiz` redirect. In a women's store with zero
products, the most-linked sizing page is a men's polo chart.

**It is also the house standard** (§1.6) and must not be deleted — see §10.

---

## §4 Collections — all 15

Every one returns `productsCount: 0`.

| Handle | Title | Rule | Class |
|---|---|---|---|
| `all` | All Products | price > 0 AND tag ≠ `order-protection` | keep |
| `womens-activewear` | Women's Activewear | tag = `womens` | keep |
| `tops` · `shorts` · `leggings` · `sports-bras` · `sets` · `dresses` · `loungewear` · `coats-jackets` · `knitwear` · `denim` · `outerwear-hoodies` | — | title-contains rules | keep |
| `mens-golf-polos` | **The Polo Collection** | manual, empty | 🟠 **needs owner decision** — 14 redirects point here; men's, in a women's store |
| `long-sleeve-golf-polos` | **The Championship Capsule** | manual, empty | 🟠 **needs owner decision** — same |

**Referenced but non-existent:** `/collections/bottoms`, `/collections/tennis-and-court`,
`/collections/drop-04-voltcore`, `/collections/mens-activewear`. Each is a redirect
target with nothing behind it (§2.6).

Flag for Track B: `leggings` excludes titles containing "Set" and `sets` requires
it, so **product naming decides collection membership**. Fragile, not broken.
**Keep, revisit at catalog load.**

---

## §5 Menus — all 9

| Handle | Title | Items | Class |
|---|---|--:|---|
| `main-menu` | Main menu | 4 | 🟠 **needs owner decision** — every item is polo-era: The Polo Collection · The Championship Capsule · Materials · Sizing |
| `footer` | Footer menu | 4 groups, nested | keep — **fix 1 dead link** |
| `footer-shop` | Shop | 4 | **delete candidate** — duplicates `footer` → Shop |
| `footer-about` | About & Help | 8 | **delete candidate** — duplicates `footer` |
| `footer-help` | Help | 6 | **delete candidate** — duplicates `footer` → Help; **1 dead link** |
| `footer-legal` | Legal | 6 | **delete candidate** — duplicates `footer` → Company; **1 dead link** |
| `customer-account-main-menu` | Customer account main menu | **0** | 🟠 **empty** — an unconfigured setting under the zero-empty-sections requirement |
| `hivolt-draft-main` | HIVOLT draft — main | 3 | delete — build scaffolding |
| `hivolt-draft-shop` | Shop | 2 | delete — build scaffolding |

Five footer menus is the clearest structural mess on the store. Only `footer` is
nested; the other four are flat duplicates from an earlier theme. Which the *live*
theme references must be read from its settings before any deletion — **do not
delete on the strength of this table alone.** `customer-account-main-menu` being
empty is a direct hit against *"zero unconfigured settings anywhere."*

---

## §6 Metafield definitions — 38

Zero products means **every one of these has zero values attached**. Cleanup here
is free right now and will not be later.

### 6.1 🟠 German-language definitions still present — 5

| Owner | Namespace.key | Name | Class |
|---|---|---|---|
| PRODUCT | `custom.groessentabelle` | Größentabelle (cm) | **delete** |
| PRODUCT | `custom.fit_note` | Passform-Hinweis (Model) | **delete** |
| PRODUCT | `custom.faq_passform` | FAQ — Passform | **delete** |
| PRODUCT | `custom.faq_material` | FAQ — Material & Pflege | **delete** |
| SHOP | `custom.cart_carrier` | Warenkorb — Versand-Carrier | **delete** |

The German artefacts Track A asked for. Definitions only — no data is lost.

### 6.2 🔴 `custom.compare_at_price_text`

A free-text field whose only function is to put arbitrary text beside a compare-at
price — the mechanism for exactly the deceptive compare-at pricing §1.1 prohibits.
Empty today. **Delete**, or at minimum never populate it.

### 6.3 `spec.*` — 20 definitions, the PDP data layer

**Polo-specific, no use in a women's line:** `collar`, `placket`, `cuff`, `knit`
→ **needs owner decision** (delete, or keep for a future men's line).

**Carry forward:** `gsm`, `composition`, `rise`, `inseam`, `gusset`, `opacity`,
`care`, `fit`, `hem`, `finish`, `origin`, `model_height_cm`, `model_wears_size`,
`benefits`, `size_chart` → **keep**. `opacity` and `gusset` in particular are
directly on-brief for leggings.

### 6.4 App-owned

| Namespace | Owner | Class |
|---|---|---|
| `mm-google-shopping.*` (gender, age_group, custom_product) | Google/Meta feed app | keep — feed depends on them |
| `mm_google_shopping_extension.merchant_id` = `5838274874` | same | keep — real Merchant Center ID |
| `mm_google_shopping_extension.show_store_widget_app_embed_block` | same | keep |
| `shopify.*` (fabric, age-group, target-gender) | Shopify standard taxonomy | keep |
| `hivolt.lede` | this build | keep |
| `custom.mpn`, `custom.feed_title`, `custom.identifier_mode` | feed support | keep |

A live Merchant Center ID is on file, which raises the stakes on the
Merchant-Center image and claims rules recorded in `ASSUMPTIONS.md`.

---

## §7 Metaobject definitions — 4

| Type | Entries | Class |
|---|--:|---|
| `hivolt_size_chart` | **0** | keep — schema is sound (`measurement_basis`, `source_unit`, `source_reference`); the §1.6 shape |
| `shopify--fabric` | 0 | keep |
| `shopify--age-group` | 1 | keep |
| `shopify--target-gender` | 2 | keep |

Stated plainly: the fabricated size-chart measurements are **not** in metaobjects —
`hivolt_size_chart` is empty. They exist only in the two unpublished pages. The
clean structure survived; only the invented numbers were the problem.

---

## §8 Files — 150

| Group | n | Class |
|---|--:|---|
| **Roxelis / Auria perfume** — product shots, scent variants, how-to, comparison pair, logo, 2 favicons | ~25 | **delete** — a dead business |
| **Roxelis / Auria `.liquid` section source** — `auria-home`, `auria-product-page`, `roxelis-cologne`, `roxelis-cart`, `auria-layout`, `product.cologne.json`, 14 iterative copies | ~20 | **delete** — theme source for a dead business, stored as files |
| **`ugc 1`–`ugc 12`** | 12 | 🔴 **delete** — twelve images labelled "UGC" for a perfume business with no customers. Generated stand-ins for user content. Directly against §1.1. |
| **YUBBEX theme zips v1.0.1–v1.0.5** | 5 | **delete** — a theme unrelated to Impulse |
| **`hivolt-ig-*`** — 9 garments × on-model/product/detail | 27 | **needs owner decision** — the AI-generated product imagery class; Merchant Center misrepresentation risk |
| **`campaign-*`, `br-*`, `hv-slide*`, `g1`–`g8`** | ~28 | **needs owner decision** — same class |
| **Brand films / clips** — `hivolt-spec`, `-ask`, `-opacity`, `-ladder`, `-weights`, `-sets`, `-returns`, `hv-factory`, `hv-shipping`, `hv-mens`, `hv-yoga`, `hv-voltcore`, `hivolt-sheet`, 3 videos | ~16 | **needs owner decision** — `hv-factory` depicts a factory HIVOLT does not operate |
| **Screenshots** — 2 × `ChatGPT_Image_*`, `inventory_export_1-Google-Sheets-*` | 3 | **delete** — working detritus |
| **Deprecated logo** — `hivolt-logo.png` + `_dcdc2bdb` copy, `hivolt-mark-square`, `hivolt-favicon`, `hivolt-favicon-hv` | 5 | **needs owner decision** — `hivolt-logo.png` is still the target of both favicon redirects (§2.6) |
| **Current brand** — `hivolt-badge.png`, `hivolt-lockup-dark.png` | 2 | **keep** — referenced by dev theme settings |
| Product hero webp — `hv-w09-hero`, `hv-p04-hero` | 2 | needs owner decision |

### 8.1 Correction to the build record

The repo record states **four** brand files were uploaded. Only **two** are in
Shopify Files:

```
files(query:"filename:hivolt-lockup*") → hivolt-lockup-dark.png   (1 result)
```

`hivolt-lockup-light.png` and `hivolt-lockup.png` **are not on the store.**

Functionally harmless — dev `settings_data.json` references `hivolt-lockup-dark.png`
and `hivolt-badge.png`, both of which exist — but the record overstated what landed,
and a light-background lockup must be uploaded before any light-ground layout uses one.

---

## §9 Locales, markets, themes

| | |
|---|---|
| `en` | primary, published |
| `de` | **`published: false`** — matches `LOCALE-AUDIT.md` |
| Market: United States | enabled |
| Market: International | **disabled** |

Locale `de` unpublished is why 242 German redirects cost nothing today, and why the
170-redirect blog mirror is dormant rather than live.

**Themes — read live this session, role never inferred:**

| Theme | Name | Role |
|---|---|---|
| `158743363816` | Impulse | **MAIN** |
| `158753652968` | IMPULSE-REBUILD-2026-08-24 | UNPUBLISHED ← build target |
| `158753849576` | Copy of Impulse | UNPUBLISHED |

Three themes, and for the first time in this engagement **every name is role-neutral
or role-accurate**. The dev target is confirmed unpublished before any further write.

---

## §10 The house standard (standing rule §1.6)

`/pages/size-guide` states:

> *"We have not converted, estimated, or averaged any number on this page."*

Every figure traces to a supplier statement; where one was unavailable, the gap is
named rather than filled. That is the standard for every page this build produces:

1. **Every figure traces to a named source** — owner, supplier document, store
   configuration, or published standard.
2. **Gaps are named, not filled.** An absent measurement is written as absent.
3. **Nothing is converted, estimated, averaged, or interpolated silently.** If a
   number is derived, the derivation is stated.
4. **The provenance statement is published on the page**, not kept in a repo file.
   The reader can check the claim about the claims.
5. **A page that cannot meet 1–4 ships unpublished** with `[[NEEDS: …]]` markers
   and a row in `CLAIMS-REGISTER.md`.

`hivolt_size_chart`'s field schema — `measurement_basis`, `source_unit`,
`source_reference` — is this standard expressed as data. Future size charts should
be built on it rather than as free HTML.

---

## §11 Actions, by who can take them

### Executable now, no owner input, no deletion
1. Repoint/remove the four dead-target redirects (§2.6) — blocked only on a destination, which for `tennis-and-court` and `bottoms` is an IA question.
2. Fix the four dead menu links to `/pages/shipping-delivery` (§1.3).
3. Populate `customer-account-main-menu` (§5).

### Needs owner decision — do not act
4. **Shop policies (§1.2)** — the 2–4 / 8–14 figures, the 5 vs 5-7 refund contradiction, and the "HIVOLT is a single member LLC" entity claim vs **Dn Global Trading LLC**. I may not rewrite any of it under §1.2.
5. The fourteen `mens-golf-polos` redirects and the two polo collections (§2.5, §4).
6. `/pages/size-guide` — a published men's polo guide as the store's most-linked sizing page (§3.2).
7. The ~75 AI-generated image and video files (§8).
8. The four polo-specific `spec.*` definitions (§6.3).

### Safe to delete once authorized — zero data loss
9. 5 German metafield definitions (§6.1) · `custom.compare_at_price_text` (§6.2) · ~60 dead-business files including the 12 "UGC" images and 5 YUBBEX zips (§8) · `hivolt-draft-*` menus (§5) · the malformed `/depages/…` redirect (§2.6).

### Gate on
10. The four duplicate footer menus — **read the live theme's settings first** (§5).

---

## §12 Verdict on the blog prune (§3.2)

The prune is **not blocked** by this sweep, but the sweep changed one of its inputs:

- The German arm **does not need building** — 170 redirects already exist pointing at
  the English articles. Deleting an English article means repointing **two** things:
  the article's own redirect and the `/de/` redirect targeting it.
- **No redirect conflicts in the `/blogs/news/*` namespace** beyond the four perfume
  articles already parked at the blog index.
- The three redirect↔page collisions (§3.1) are **outside** the blog namespace.

Step 1 — pull all 331 redirects — is **complete and reconciled**. Step 2, the
deletion map, can be built without further reads.

*Read-only sweep. No shop-level resource was created, modified, or deleted.*
