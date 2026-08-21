# HIVOLT PDP — release QA

## Verdict

> ## READY FOR HUMAN PREVIEW
>
> The theme code is complete, tested and deployed to the draft theme. It is
> **not** a recommendation to publish: publishing turns on commercial and
> policy decisions that only the owner can make, and on store data that does
> not exist yet. Both are itemised under *Remaining release blockers*.

---

## Build tested

| | |
|---|---|
| Branch | `claude/hivolt-store-admin-6e3q23` |
| Commit | `51c4732` — *PDP release gate: golden fixture, 113 assertions, browser QA, four defects fixed* |
| Pull request | #2 (draft, open, not merged) |
| Draft theme | `158653808872` — *HIVOLT v7 — DRAFT: PDP data layer*, role `UNPUBLISHED` |
| Live theme | `158570021096` — *HIVOLT v6*, role `MAIN`, **not touched** |
| Date | 2026-08-20 |

Reproduce the whole gate:

```
python3 site/parse-liquid.py site/theme-v7/snippets/*.liquid   # dialect parse
python3 site/check-liquid.py site/theme-v7/snippets/*.liquid   # house rules
python3 site/check-hivolt-pdp.py                               # release gate
python3 site/render-pdp-preview.py && python3 site/check-hivolt-browser.py
```

Each exits non-zero on failure.

---

## Automated coverage

`python3 site/check-hivolt-pdp.py` → **113/113 PASS**

| Area | Checks | What it proves |
|---|---:|---|
| T1 specs | 10 | Correct labels and values, correct omission, no empty row, whole block gone when empty, values escaped |
| T2 size guide | 16 | Trigger only with real data, header/row correctness, cm↔in conversion, decimals, unmeasured cells, dropped rows, basis copy, unit toggle, retracted copy stays gone |
| T3 swatches | 15 | Real swatch data renders, missing swatch falls back to text, no colour guessed from a name, sold-out in class and accessible name, one selection, theme JS hooks intact, ids unique and paired |
| G6 feed title | 7 | Metafield resolves, blank falls back, variant options appended, 150-char truncation, structured data still uses the storefront title |
| G7 identifiers | 19 | Every mode and every fallthrough, GTIN shape and length, variant override, no Shopify id or SKU promoted to an identifier |
| G8 structured data | 26 | Valid JSON, every node type, per-variant price/availability/URL, identifiers only where real, and the negative assertions |
| Degradation | 7 | All ten scenarios render, well-formed HTML, no duplicate id, no nested interactive, no placeholder, no empty cell, JSON parses |
| Liquid safety | 6 | Dialect parse, boolean-precedence lint, nil-guard shape, single script tag, no raw metafield in a style attribute |
| Nil guards | 6 | Regression locks for the four defects found this session |

### Scenarios exercised

| ID | Scenario | Expected |
|---|---|---|
| A | Fully populated | Everything renders |
| B | No specifications | Whole spec block absent |
| C | Specs, no size chart | Specs render; no trigger, no dialog |
| D | No swatch data on any value | Every value becomes a text button |
| E | One sold-out variant | Marked visually and in the accessible name |
| F | Declares `gtin`, no barcode | Falls through to `none` |
| G | No verified identifier at all | `identifier_exists=no`, no gtin, no mpn |
| H | Blank feed title | Falls back to the storefront title |
| I | Single-variant simple product | One offer, no `Default Title` in the offer name |
| J | Bare product — no description, image, brand or sku | Valid JSON, those properties simply absent |

The golden fixture is a 5-colour × 5-size matrix, 25 variants, with identifier
cases spread across it so one JSON-LD render exercises every resolution path.
It lives in `site/hivolt_pdp_fixtures.py`, contains no real product data, marks
every product `QA-FIXTURE`, and has no Shopify client — it cannot write to the
store.

---

## Browser matrix

`python3 site/check-hivolt-browser.py` → **174/174 PASS**

Chromium 1194, `device_scale_factor=2`, screenshots in `/tmp/hivolt-pdp-qa/shots`.

| Viewport | Overflow | Clipping | Tap targets | Dialog | Variant controls | axe | Result |
|---|---|---|---|---|---|---|---|
| 320px | none | none | ≥44px | open / focus in / trap / Esc / restore / close | arrows move, one selected, ring correct | 0 | PASS |
| 375px | none | none | ≥44px | pass | pass | 0 | PASS |
| 390px | none | none | ≥44px | pass | pass | 0 | PASS |
| 430px | none | none | ≥44px | pass | pass | 0 | PASS |
| 768px | none | none | ≥44px | pass | pass | 0 | PASS |
| 1024px | none | none | ≥44px | pass | pass | 0 | PASS |
| 1440px | none | none | ≥44px | pass | pass | 0 | PASS |

All ten scenario pages were additionally checked at 375px for horizontal
overflow and duplicate DOM ids — clean.

### Notable observations

- **320px size chart.** A chart wider than the dialog is unavoidable — a
  six-column chart will never fit a 320px phone. The container was already a
  scroller, but the third column was cut with nothing indicating more content.
  Fixed with a CSS-only scroll shadow that appears only while there is more
  table in that direction and disappears on a chart that fits.
- **Dialog header.** `.hv-sg__close` carries a `-10px` right margin, so the
  header's `scrollWidth` exceeds its `clientWidth` by 10px. Measured at 320px:
  the button spans 243–287 and the panel 19–301, so the overflow lands inside
  the panel's 24px padding. Nothing is cut off and both hit-tests land on the
  button. Recorded, not changed.
- **Unit toggle height.** The cm/inches segmented control is 40px, below the
  44px target used elsewhere. It is a secondary control inside an already-open
  dialog, so it is reported rather than failed. Worth raising to 44px if the
  owner wants a uniform minimum.

---

## Accessibility

Tooling: **axe-core 4.x** injected into the live page, WCAG 2.0/2.1 A and AA
rule sets, at all seven viewports with the dialog open. The scanner was checked
against a deliberately broken page first and correctly reported eight
violations there, so a zero on our pages is a real zero.

| Check | Result |
|---|---|
| axe-core WCAG 2.1 AA, 7 viewports | **0 violations** (`/tmp/hivolt-pdp-qa/axe-report.json`) |
| Control labels | Every swatch input has a `<label for>`; ids unique and paired |
| Dialog labelling | `aria-labelledby` points at the dialog's own `<h2>`; `aria-haspopup="dialog"` on the trigger |
| Keyboard access | Arrow keys move swatch selection; the chart region is `tabindex="0"` with an `aria-label` |
| Focus restoration | Escape and the close control both return focus to the trigger |
| Focus containment | No control behind the dialog can be focused while it is open |
| Visible focus | `:focus-visible` outlines on trigger, close, unit toggle, chip and text swatch |
| Sold-out accessible names | "Slate — Sold out"; available values carry no sold-out wording |
| Table semantics | `<caption>`, `<th scope="col">`, `<th scope="row">` |
| Heading structure | One `<h2>` per dialog, tied to its label |
| Colour contrast | Passed by axe. Volt yellow is used only as a swatch fill, never as text or as the sole state indicator |
| Duplicate ids | None, in any scenario, in source or in the DOM |
| Invalid ARIA | None reported |

### Defects found and fixed this session

1. Swatch option values were interpolated unescaped in both the chip's
   accessible name and the text fallback.
2. The unmeasured-cell dash carried its meaning in an `aria-label` on a bare
   `<span>`; moved to real visually-hidden text with the dash `aria-hidden`.
   *(fixed in the previous session, verified here)*
3. No scroll affordance on a horizontally scrollable chart at 320px.

### Legacy issues, out of scope

None surfaced. axe was run against the isolated HIVOLT components, not the full
Impulse theme, so this is not a whole-site accessibility statement. A full-page
scan is only possible once the theme can be previewed in a browser that can
reach the storefront — see *Recommended next task*.

---

## Structured data

Validated locally at the object level: the JSON-LD is parsed with a real JSON
parser and asserted property by property. No internet access was needed and
none was used, so the gate stays sufficient offline.

| Property | Result | Evidence |
|---|---|---|
| Organization | **PASS** | `name`, `url`, `@id`; `sameAs` carries only non-blank socials |
| Organization `logo` | **PASS** | Omitted when the favicon is unset; emitted only when ≥112px |
| WebSite | **PASS** | `publisher.@id` resolves to the Organization node |
| BreadcrumbList | **PASS** | Positions 1..n with no gaps; the collection step appears only when reached through one |
| Product | **PASS** | `name` equals the storefront title, never the feed title |
| Offers | **PASS** | 25 offers for 25 variants; 1 for the single-variant product |
| price | **PASS** | Per variant, from `variant.price`; both $69.00 and $74.00 tiers resolve |
| priceCurrency | **PASS** | From `cart.currency.iso_code`, so it follows the shopper's market |
| availability | **PASS** | Per variant; both InStock and OutOfStock present in one document |
| Offer URL | **PASS** | Exactly one `?`; a tracking-laden `product.url` is stripped first |
| GTIN | **PASS** | Present on exactly the 6 variants with a barcode; correct `gtin8/12/13/14` alias |
| MPN | **PASS** | Variant MPN beats product default; absent where the mode resolves to `none` |
| **AggregateRating** | **PASS — absent** | Asserted absent across all 10 scenarios |
| **Review / ratingValue / reviewCount** | **PASS — absent** | Asserted absent across all 10 scenarios |
| **priceValidUntil** | **PASS — absent** | Encodes a commitment nobody has made |
| **shippingDetails** | **PASS — absent** | Blocked on the shipping decision (P-3) |
| **hasMerchantReturnPolicy** | **PASS — absent** | Blocked on the returns decision (P-4) |
| **Fake GTIN / MPN** | **PASS — impossible** | No Shopify product or variant id may appear as an identifier; a SKU is never promoted to MPN |

Accuracy was preferred to completeness throughout. Nothing was added to raise
the property count.

---

## Graceful degradation

| Scenario | Result |
|---|---|
| A Fully populated | All components render |
| B No specifications | Spec block absent entirely — no heading, no empty rows |
| C Specs but no size chart | No trigger and no dialog; specs unaffected |
| D No swatch data | All values render as text buttons; no `background-color` emitted |
| E One sold-out variant | Struck-through chip, `data-available="false"`, "Sold out" in the accessible name |
| F Declares `gtin`, no barcode | Every variant resolves to `none` |
| G No identifier at all | `identifier_exists=no`; no `gtin`, no `mpn` anywhere in the document |
| H Blank feed title | Storefront title used; `source` reports `fallback` |
| I Single-variant product | One offer, no `Default Title` leakage into the offer name or feed title |
| J Bare minimum | Valid JSON; `description`, `image`, `brand`, `sku` simply absent |

Across all ten: no Liquid exception, no malformed HTML, no unparseable JSON-LD,
no duplicate id, no nested interactive element, no empty `<td>`/`<dd>`/`<li>`,
and no placeholder string (`lorem`, `TODO`, `undefined`, `N/A`, `TBD`).

---

## Code and deployment integrity

| Check | Result |
|---|---|
| Liquid dialect parse | 9/9 templates clean |
| House rules (`check-liquid.py`) | Clean — no banned urgency, rating or social-proof pattern |
| Boolean-precedence lint | Clean — no condensed guard reads a property it just null-checked |
| Metafield-vs-blank lint | Clean — every metafield resolved through `default` first |

### Theme files changed and redeployed

| File | Change | Size | MD5 |
|---|---|---:|---|
| `snippets/hivolt-identifier.liquid` | Product-level mode made reachable | 3923 | `37a7371c…` |
| `snippets/hivolt-size-guide.liquid` | Empty-note paragraph removed; half-sentence model line removed; note escaped | 7883 | `b8d1333e…` |
| `snippets/hivolt-swatches.liquid` | Option values escaped in both paths | 3621 | `a1e87529…` |
| `assets/hivolt-pdp.css` | Scroll affordance on the size chart | 9602 | `489afa7a…` |

**Hash verification: 15/15 files on draft theme `158653808872` are byte-identical
to `site/theme-v7/` in this repo.** Nothing was uploaded to `158570021096`; at
the time of writing MAIN's `updatedAt` is `2026-08-20T05:47:10Z`, before this
session's first write, and MAIN contains no `hivolt-*` file at all.

---

## Remaining release blockers

### 1. Theme code

**None.** Every gate is green and the deployed files match the repository.

### 2. Store data — blocks a useful preview, not the theme

Verified read-only on 2026-08-20:

| Blocker | Evidence | Consequence |
|---|---|---|
| **No size chart exists, and none can be created yet** | `metaobjects(type: "hivolt_size_chart")` returns 0 entries. Investigated 2026-08-20: no garment measurement exists anywhere for any draft polo — see *Real catalog integration* | The size guide correctly renders nothing on every product. **Blocking action: `docs/HIVOLT-POLO-MEASUREMENT-REQUEST.md`** — the supplier provides recommended body weight only, which is not a garment dimension. |
| **No `spec.*` values on any product** | All 3 draft products return 0 metafields in the `spec` namespace | The specification table correctly renders nothing. Same consequence. |
| **No barcodes** | Every variant sampled has `barcode: null`; `custom.mpn` unset | Every offer resolves to `identifier_exists=no`. Correct, but no product will carry a GTIN until a supplier provides one. |
| **Weight-based sizing on SKUs** | e.g. `HV-H01-NAVY-EURS60-70KG` | A size chart built on these needs a decision about what the size labels mean before measurements can be attached. |

None of these is fabricable. Each needs a supplier document or a measured
sample.

### 3. Policy and business decisions — owner only

See `docs/HIVOLT-POLICY-CORRECTIONS.md`, seven items, none applied. The ones
that gate publishing:

- **P-3** shipping policy says "United States only"; no fulfilment model agreed.
- **P-4** returns are US-only in writing, which conflicts with UK/EU statutory
  rights, and the page implies an Illinois warehouse that has not been agreed.
- **P-7** four discounts are active simultaneously against unapproved pricing.
- Product pricing, publication and channel activation remain owner decisions.

### 4. Unrelated live-site issues

See the next section.

---

## `/pages/fabric-weight-index`

### Verified condition, 2026-08-20, read-only

| Fact | Value | How verified |
|---|---|---|
| Page still published | `isPublished: true` | Admin API `pages(query:"handle:fabric-weight-index")` |
| Last modified | `2026-08-11T17:31:53Z` | Same — unchanged since before this work began |
| Products in the store | 0 active, 3 draft, 0 archived | `productsCount` by status |
| Sampled product handles from the page | 8 of 8 return `null` | `productByHandle` — the products are deleted, not archived |
| Redirects configured | 5+ exist, so the mechanism is in use | `urlRedirects` |

The page's own opening line still claims *"Every fabric weight HIVOLT sells, in
one table. 109 garments, from 91 to 380 g/m²."*

**The 109 figure was not independently recounted.** The storefront is
egress-blocked from this environment (`hivolt-usa.com` and the myshopify domain
both fail to connect) and Admin API responses cannot be piped into a local
parser from this session, so anchors could not be counted mechanically. What is
established without needing the exact count: the store contains three products,
all drafts, all polos, none of which appear on that page — so **every product
link on it is dead**, whatever the precise number.

A human with storefront access can get the exact figure with:

```
curl -s https://hivolt-usa.com/pages/fabric-weight-index \
  | grep -o '/products/[a-z0-9-]*' | sort -u | wc -l
```

### Severity

**Independent production incident. Not a release blocker for this theme.**

Reasoning:

- It is page content, stored at store level and shared by every theme.
  Publishing or not publishing `158653808872` neither causes nor fixes it.
- It is live and indexable right now, so it is more urgent than the draft theme
  in customer and SEO terms while being entirely separate from it.
- Its remediation is a content and redirect decision, which is owner territory.

### Remediation options, safest first

1. **Unpublish the page.** One field, instantly reversible, removes the
   soft-404 farm immediately. Loses whatever link equity the URL holds.
2. **Unpublish and add one redirect** `/pages/fabric-weight-index` →
   `/pages/materials-sustainability`. Preserves equity. Requires agreeing the
   target.
3. **Replace the body with an honest empty-state** — the index rebuilds itself
   from `spec.gsm` once real polos ship. Draft text is in
   `docs/HIVOLT-POLICY-CORRECTIONS.md` §P-1 option B.
4. **Per-product redirects.** *Not recommended.* 109 destinations would have to
   be guessed, and there is no polo that corresponds to a deleted legging.

### What was changed

**Nothing.** The page, its body, its published state and the redirect table were
read and not written.

---

## Real catalog integration

> ## REAL SIZE DATA: BLOCKED — AUTHORITATIVE MEASUREMENTS REQUIRED
>
> See `docs/HIVOLT-POLO-MEASUREMENT-REQUEST.md`.
>
> No `hivolt_size_chart` metaobject was created and no product metafield was
> written. There is no garment measurement to put in one.

Attempted 2026-08-20 against the product the release report named as the next
step.

### Product examined

| | |
|---|---|
| Title | HIVOLT Classic Cotton Polo — Men's Short Sleeve |
| Product ID | `gid://shopify/Product/9603121774824` |
| Handle | `hivolt-classic-cotton-polo-mens-short-sleeve` |
| Status | **DRAFT** — asserted before any write was considered |
| Variants | 20 (Colour 6 × Size 5, sparse) |
| Size option values | `EUR S 60-70kg`, `EUR M 70-80kg`, `EUR L 80-90kg`, `EUR XL 90-100kg`, `EUR XXL 100-105kg` |
| Colour option values | Navy, White, Light Blue, Dark Grey, Black, Army Green |
| `spec.size_chart` | `null` |
| `spec.*` metafields | 0 |

### Where measurement evidence was looked for

| Source | Result |
|---|---|
| Repository — all `.md` `.csv` `.tsv` `.json` `.txt` `.xlsx` `.pdf` | No garment measurement. The only hits for chest/shoulder/sleeve/flat are this project's own test fixtures and the retired fabric page. |
| Repository — `HV-H01`, supplier item id, `60-70kg` and equivalents | Hits only in our own documentation |
| Shopify product metafields (all namespaces) | `custom.supplier_source`, `custom.supplier_variant_map`, three `mm-google-shopping` feed fields, three Judge.me review stubs. No measurement. |
| Shopify Files | One video. No spec sheet, tech pack or measurement document. |
| Product media, 9 images | Hero, six colourways, two "detail". The two detail images could **not** be examined — `cdn.shopify.com` is egress-blocked from this environment. Flagged below. |
| Product description | Contains a supplier sizing table — **body weight only** (see below) |
| AutoDS research catalogue, by supplier item id | No record returned |
| Supplier listing direct | `aliexpress.com` egress-blocked |

### What the supplier actually provides

The product description carries the supplier's sizing table verbatim:

| Size label | Recommended body weight |
|---|---|
| EUR S | 60-70kg |
| EUR M | 70-80kg |
| EUR L | 80-90kg |
| EUR XL | 90-100kg |
| EUR XXL | 100-105kg |

That is the entire sizing dataset for this product. It contains **no chest, no
length, no shoulder, no sleeve — no garment dimension of any kind.**

A recommended wearer body weight cannot be converted into a garment
measurement. There is no formula, and inventing one is exactly the failure this
architecture was built to prevent.

### Evidence classification

| Candidate source | Class | Reason |
|---|---|---|
| Body-weight table on the Classic Cotton Polo | **Not a measurement source** | It is a fit recommendation, not a garment dimension |
| Anti-Wrinkle Polo "Length" column, 92–116 cm | **C — insufficient** | Label contradicts the values; see below |
| Slim-Fit Cotton Polo | **Not a measurement source** | Supplier states sizes with no measurements |

Nothing reached class A, and nothing reached a class B that could be trusted
without interpretation. Per the rule, **nothing was written.**

#### Why the one numeric source was rejected

The Anti-Wrinkle Polo (`9603123216616`) is the only draft product with numeric
garment data. It is internally consistent — all seven stated inch values match
their centimetre values to two decimal places — and it was still rejected:

- Labelled **Length**, but grades at a constant **4 cm per size**. Men's polo
  body length typically grades ~2 cm per size; 4 cm is chest-circumference
  grading.
- **92–116 cm** is outside the normal men's polo body-length range (~68–80 cm)
  and inside the normal chest-circumference range.
- The supplier states no measurement basis.

Publishing a column headed "Length" carrying what is probably a chest
circumference would put a wrong number in front of a customer. That is worse
than an absent size guide. It is also a different product from the one this
task targeted.

### Size-label semantics

**UNVERIFIED.**

HIVOLT's own product description states the kilogram range is a recommended
body weight, and the store's variant SKUs encode the same (`HV-H01-NAVY-EURS60-70KG`).
That description was transcribed from the supplier listing by an earlier
session, not from a specification document, and it could not be re-checked
against the supplier this session — AliExpress is egress-blocked and AutoDS
holds no record of the item.

So the internal evidence is consistent but self-referential. Whether `EUR`
denotes a European sizing standard, and whether an equivalent alpha size
exists, is unknown. The questions are in §6 of the measurement request.

**No variant option value was renamed.** `EUR S 60-70kg` remains exactly as
stored.

### Real-data pipeline verification

The fixture proves the components work. This proves the **real** relationship
behaves correctly with the data that genuinely exists today — a product with no
chart must produce no size guide, not a broken one.

Method: the Admin API read-back for product `9603121774824` was transformed
faithfully into the existing local render harness and rendered through the same
snippets the draft theme runs. **This is not a storefront preview** — the
storefront remains egress-blocked. Every input was read from Shopify in this
session.

**14/14 PASS**

| Check | Result |
|---|---|
| Size-guide trigger absent | PASS |
| Size-guide dialog absent | PASS |
| No placeholder table markup | PASS |
| Specification block absent | PASS |
| Colour option falls back to text buttons | PASS |
| No colour inferred from a value's name | PASS |
| All six real colourways render | PASS |
| All five real size labels render verbatim | PASS |
| Size labels not silently renamed to S/M/L | PASS |
| Structured data valid, Product node present | PASS |
| Offer count equals the real variant count (20) | PASS |
| Every offer OutOfStock, matching real inventory of 0 | PASS |
| No identifier invented for barcode-less variants | PASS |
| No rating or review markup | PASS |

### Missing-chart control

All three draft products currently have `spec.size_chart = null`, so the
control condition is the whole catalogue: no product renders a size-guide
trigger, a dialog or a placeholder table. When one chart is eventually attached
to one product, that product will opt in on its own without changing the others.

### Observations for the owner — reported, not changed

1. **Size options are stored out of order.** Shopify returns them as
   `EUR S`, `EUR M`, `EUR XL`, `EUR XXL`, `EUR L`. The size selector will
   render `L` after `XXL`. This is product data, not theme code, and changing
   variant option values was outside this session's authority.
2. **No option value carries swatch data.** All 11 values return
   `swatch: null`, so every colour renders as a text button. That is T3's
   designed fallback behaving correctly on real data, and it is the reason the
   fallback exists — but real swatches would present better.
3. **Two "detail" images could not be examined.** `cdn.shopify.com` is
   egress-blocked here. If either turns out to be a supplier sizing diagram it
   would change the answer for this product. Anyone with CDN access should open
   `hv-h01-detail-1.webp` and `hv-h01-detail-2.webp` before treating this as
   settled.

### Theme changes

**None.** The real data exposed no defect: the pipeline failed closed exactly as
designed. No file was uploaded to any theme this session, so the draft theme
remains byte-identical to `site/theme-v7/` as verified in the previous session.

---

## Safety confirmation

**Release-gate session (commit `51c4732`)**

- MAIN theme `158570021096` — **not written to, not published.** It carries no
  `hivolt-*` file and its `updatedAt` predates that session.
- Draft theme `158653808872` — 4 files updated, **role still `UNPUBLISHED`.**
- No production product, metafield definition, metaobject entry, page, policy,
  menu, redirect, collection or discount created, modified or deleted. Store
  access was read-only apart from the four draft-theme file writes.

**Real-catalog session (2026-08-20)**

- **Zero Shopify mutations of any kind.** Every call was a read. No metaobject
  was created; no product metafield was written; no theme file was uploaded.
- MAIN theme `158570021096` — role `MAIN`, `updatedAt` `2026-08-20T05:47:10Z`,
  unchanged.
- Draft theme `158653808872` — role `UNPUBLISHED`, `updatedAt`
  `2026-08-20T10:00:47Z`, unchanged since the previous session's last write.
- No product status, title, description, price, variant, option value, SKU,
  barcode, inventory or SEO field touched. `/pages/fabric-weight-index`
  untouched. Navigation, collections, redirects and policies untouched.
- PR #2 — **not merged.**

One thing worth recording rather than glossing over: product `9603121774824`
reports `updatedAt: 2026-08-20T22:17:33Z`, later than this session's first
read. No mutation was issued from here — every Shopify call this session was a
`graphql_query`, and the AutoDS call is documented read-only. A field-by-field
re-read confirms it: title, handle, vendor, description, status and variant
count are identical to the first read, and every metafield still carries its
original `updatedAt` of 06:33–06:37. The bump came from something outside this
session, most plausibly the installed Judge.me app. Nothing in scope changed.
