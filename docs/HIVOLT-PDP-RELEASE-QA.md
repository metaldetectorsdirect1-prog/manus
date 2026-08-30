# HIVOLT PDP — release QA

> ## Production-state update — 2026-08-21
>
> **Theme `158653808872` was subsequently published and is now `MAIN`.**
> Theme `158570021096` is now `UNPUBLISHED`.
>
> Statements below that describe `158653808872` as a draft, or `158570021096`
> as MAIN, were **true when those tests were run** and are preserved as written.
> They are a record of the conditions each session worked under, not current
> instructions.
>
> **Both themes were also renamed on 2026-08-22** — `158653808872` to "HIVOLT
> v7 — Production Baseline — PDP Data Layer" and `158482727144` to "HIVOLT v35 —
> Returns Copy Correction". Theme names quoted anywhere below are the names in
> use when those sessions ran. Match themes by ID, not by name.
>
> For current state see `docs/HIVOLT-CURRENT-STATE.md`, and re-query Shopify
> before acting on either.

## Verdict

> ## THEME IS LIVE — PRODUCTS ARE NOT
>
> **Updated 2026-08-22.** The owner published theme v7 (`158653808872`) on
> 2026-08-21, so the PDP data layer described below is on the live storefront.
> It was verified byte-identical to tested source: 10/10 `hivolt-*` files match
> `site/theme-v7/` by MD5.
>
> The three HIVOLT polos remain **`DRAFT`** and are not publicly reachable.
> Publishing them still turns on commercial and policy decisions only the owner
> can make, and on product data that does not exist yet — itemised under
> *Remaining release blockers* and under *Real catalog — `spec.*` population*.
>
> The original verdict for the code itself, unchanged: **complete and tested.**

---

## Build tested

| | |
|---|---|
| Branch | `claude/hivolt-store-admin-6e3q23` |
| Commit | `51c4732` — *PDP release gate: golden fixture, 113 assertions, browser QA, four defects fixed* |
| Pull request | #2 (draft, open, not merged) |
| Draft theme | `158653808872` — *HIVOLT v7 — DRAFT: PDP data layer*, role `UNPUBLISHED` **on 2026-08-20. This theme is now `MAIN` — see the note at the top.** |
| Live theme | `158570021096` — *HIVOLT v6*, role `MAIN`, **not touched. Now `UNPUBLISHED`.** |
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
3. **Two "detail" images could not be examined.** See *Detail-media evidence
   attempt* below — a second session exhausted every available retrieval path
   and the images remain unread.

### Theme changes

**None.** The real data exposed no defect: the pipeline failed closed exactly as
designed. No file was uploaded to any theme this session, so the draft theme
remains byte-identical to `site/theme-v7/` as verified in the previous session.

---

## Detail-media evidence attempt — 2026-08-21

The previous session flagged the two `detail` images on the Classic Cotton Polo
as the highest-priority remaining evidence: if either is a supplier sizing
diagram, the product is not blocked. A dedicated session went after them.

**Outcome: neither image could be inspected. They remain unread, and the
product remains blocked.** Zero Shopify mutations were made.

### Retrieval attempts

| # | Path | Result |
|---|---|---|
| 1 | Local repository and full filesystem search | No copy exists. The images were never downloaded — the products were created by handing supplier URLs to Shopify's server-side fetcher, so the bytes went supplier → Shopify without passing through here. |
| 2 | Shopify Admin API media query | Returns metadata only — id, alt, dimensions, MIME type, CDN URL. The Admin API exposes no pixel data for a `MediaImage`. |
| 3 | `curl` with the proxy CA bundle | `CONNECT tunnel failed, response 403` |
| 4 | First-party `WebFetch` | `EGRESS_BLOCKED — cdn.shopify.com` |
| 5 | Chromium via Playwright | `net::ERR_TUNNEL_CONNECTION_FAILED` — the browser uses the same proxy |
| 6 | AutoDS connector (MCP traffic bypasses the allowlist) | No record of supplier item `1005002281827487`; a title search returned ten unrelated products, none matching the supplier colour codes `PL208` / `PL205` / `AX-511` |
| 7 | Shopify Admin authenticated browser | Not available — no Admin session or credentials in this environment |

The egress proxy recorded the denial itself:

```
{"kind": "connect_rejected",
 "detail": "gateway answered 403 to CONNECT (policy denial or upstream failure)",
 "host": "cdn.shopify.com:443"}
```

`/root/.ccr/README.md` is explicit about this class: *"The destination host is
not allowed by your organization's egress policy for this session. Do not retry
or route around it — report the blocked host."* No bypass, mirror or
third-party copy was used.

### Evidence note

| | |
|---|---|
| `hv-h01-detail-1.webp` | `gid://shopify/MediaImage/40334801469672`, 1000×1000 webp, READY. **Inspected: NO.** Contents unknown. Sizing evidence: undetermined. |
| `hv-h01-detail-2.webp` | `gid://shopify/MediaImage/40334801502440`, 1000×1000 webp, READY. **Inspected: NO.** Contents unknown. Sizing evidence: undetermined. |

**Nothing is claimed about what these images contain.** They may hold a
supplier size chart or they may be product close-ups. The only honest statement
is that this environment cannot read them.

One weak signal, recorded as a signal and not as evidence: both are 1000×1000,
the same square format as the hero and the six colourway shots, and the session
that created this product transcribed the supplier's sizing into the product
description as body-weight-only. Had a measurement chart been in the supplier's
media set, that session would plausibly have transcribed measurements too. That
is an inference about a past session's behaviour, not a fact about the pixels,
and it does not close the question.

### What this changes

Nothing about the blocked status, and nothing about the required next action.
The product still has no garment measurement, `spec.size_chart` is still
`null`, and no `hivolt_size_chart` entry exists.

It does change who can resolve it: **a human with normal Shopify Admin access
can settle this in about a minute** by opening the two images in the product's
media gallery. That check now sits ahead of sending the supplier request,
because if either image is a measurement chart the request may be unnecessary.

### T2 confirmed still correctly empty

The real-data pipeline verification was re-run against the current live state:
**14/14 PASS** — no size-guide trigger, no dialog, no placeholder table, no
spec block, while still emitting valid structured data with 20 offers, all
correctly `OutOfStock` and no invented identifier.

Release gate re-run unchanged: **113/113**, Liquid parse **9/9**. No theme file
was modified or deployed.

---

## Real catalog — Size option ordering

> ## BLOCKED — SAFE OPTION VALUE REORDER NOT AVAILABLE
>
> `productOptionsReorder` reports success and performs no write on this store
> through this access path. Attempted twice, both documented argument forms.
> **Nothing was changed and nothing was damaged.**

Attempted 2026-08-21 against the observation logged in *Real catalog
integration*: the Size option values are stored out of sequence.

### Product

| | |
|---|---|
| Title | HIVOLT Classic Cotton Polo — Men's Short Sleeve |
| Product ID | `gid://shopify/Product/9603121774824` |
| Status | `DRAFT` — asserted before and after |
| Variants | 20 |
| Size option | `gid://shopify/ProductOption/12296794800360`, position 2 |

### Before, and still

| # | Stored order | Target order |
|---|---|---|
| 1 | `EUR S 60-70kg` | `EUR S 60-70kg` |
| 2 | `EUR M 70-80kg` | `EUR M 70-80kg` |
| 3 | `EUR XL 90-100kg` | **`EUR L 80-90kg`** |
| 4 | `EUR XXL 100-105kg` | `EUR XL 90-100kg` |
| 5 | **`EUR L 80-90kg`** | `EUR XXL 100-105kg` |

The target order is derived only from the literal kilogram ranges already in
the labels — `60-70 → 70-80 → 80-90 → 90-100 → 100-105`. It does not depend on
knowing what `EUR` means, and no label was read as an alpha size.

Two independent facts corroborate that `EUR L 80-90kg` is the single displaced
value:

- The option-value IDs are sequential in the correct order — `…617192` (S),
  `…649960` (M), `…682728` (L), `…715496` (XL), `…748264` (XXL), a constant
  32768 step. The values were **created** in the right sequence; only the
  stored display order is wrong.
- The **variant** ordering is already correct. Within Light Blue the variants
  run S, M, L, XL, XXL. Only the `Size` option's `optionValues` array carries
  the wrong sequence — and that array is what Liquid renders the selector from.

### What was attempted

| # | Operation | Identification | userErrors | Effect |
|---|---|---|---|---|
| 1 | `productOptionsReorder` | Both options and all values by `id` | `[]` | **None** |
| 2 | `productOptionsReorder` | Both options and all values by `name` (the form in Shopify's own example) | `[]` | **None** |

Both calls pinned **both** options explicitly — Color first with its six values
in current order, Size second with the corrected five — because the
documentation states that input order sets option positions, so passing Size
alone would have demoted Color to position 1.

`product.updatedAt` remained `2026-08-20T22:17:33Z` across both attempts. A
write bumps that timestamp, so no write occurred.

`ProductOptionValue` exposes no `position` field — array order *is* the display
order — so the unchanged array is conclusive rather than a reading artefact.
Shopify's documentation page truncates mid-sentence at "Note: The" in every API
version indexed, so any caveat it carries could not be read.

After two no-op attempts of the officially documented operation, work stopped.
No alternative strategy was tried: rebuilding variants, deleting and recreating
the option, temporary renames and clone-and-replace are all excluded, because
every one of them risks the variant matrix to fix a display-order cosmetic.

### Forensic diff — 20/20 preserved

Programmatic comparison of the pre-mutation baseline against the post-attempt
read-back. **Zero integrity failures.**

| Assertion | Result |
|---|---|
| Variant count 20 → 20 | PASS |
| Variant GID set identical | PASS |
| `GID → SKU` for all 20 | PASS |
| `GID → Colour` for all 20 | PASS |
| `GID → Size` for all 20 | PASS |
| `GID → price` for all 20 | PASS |
| `GID → compare-at price` (all null) | PASS |
| `GID → barcode` (all null) | PASS |
| `GID → inventory item ID` for all 20 | PASS |
| `GID → inventory quantity / policy` | PASS |
| `GID → media` for all 20 | PASS |
| Colour value order unchanged | PASS |
| Size option id and position unchanged | PASS |
| Product id/title/handle/vendor/type/status/updatedAt | PASS |
| `spec.size_chart` still `null` | PASS |
| `hivolt_size_chart` count still 0 | PASS |
| No unrelated metafield touched (all still `06:33`–`06:37`) | PASS |

### Render verification — 13/13

The post-attempt Admin read-back was fed through the real-data render harness
(local; the storefront remains egress-blocked):

- The selector renders Shopify's stored order **verbatim** — `S, M, XL, XXL, L`
- No duplicate controls, no missing value, no renamed label
- Colour order unchanged; T3 text fallback still active
- T2 absent — no trigger, no dialog, no placeholder chart
- Structured data valid, 20 offers, all `OutOfStock`, no invented identifier

**This confirms the theme is correct.** It consumes Shopify's canonical option
order faithfully, so the defect lives entirely in the product data. No Liquid
change was made and none is warranted — compensating for bad data in the theme
would hide the defect on every other product.

Regression gates unchanged: release gate **113/113**, Liquid parse **9/9**,
house rules clean, no theme file modified or deployed.

### Smallest human action

In Shopify Admin → **Products** → *HIVOLT Classic Cotton Polo — Men's Short
Sleeve* → the **Variants** section → the **Size** option → drag
`EUR L 80-90kg` above `EUR XL 90-100kg`. The Admin UI reorders option values
directly and preserves variants. Renaming nothing, adding nothing.

Worth recording alongside the project's other verification traps: **a Shopify
mutation can return `userErrors: []` and still do nothing.** `themeFilesUpsert`
was already known to report success either way; `productOptionsReorder` behaves
the same. Read the resource back and check `updatedAt` — an empty error list is
not evidence of a write.

---

## Real catalog — `spec.*` population (2026-08-22)

**Result: 2 of 17 fields written. 15 deliberately left blank.**

The full audit trail is `docs/HIVOLT-PRODUCT-DATA-PROVENANCE.md`. This section
is the release-facing summary.

### Theme roles have changed since the last session — read this first

The pass began by verifying the two assertions every previous session closed
with. Both are now **false**, and not because of anything done here:

| Theme | Name | Role now | `updatedAt` |
|-------|------|----------|-------------|
| `158570021096` | HIVOLT v6 — PUBLISH ME: logo in header | **`UNPUBLISHED`** | `2026-08-21T04:10:55Z` |
| `158653808872` | HIVOLT v7 — DRAFT: PDP data layer | **`MAIN`** | `2026-08-21T04:11:02Z` |

The seven-second gap between those two timestamps is the signature of a publish
operation: the old live theme is unpublished and the new one takes the role in
the same transaction. **The owner published theme v7 on 2026-08-21.** The PDP
data layer built in the previous sessions is therefore live, not draft.

That is the owner's call and it is a reasonable one — but it changes what the
words "MAIN" and "draft" mean everywhere above this section, so it is recorded
here rather than left for someone to trip over.

Before writing anything, the newly-live theme was checked against tested source:
**10/10 `hivolt-*` files byte-identical to `site/theme-v7/` by MD5.** What went
live is what was tested.

The `spec.*` writes below remain safe under the same reasoning that governed
every earlier session, but for a different reason than before: it is no longer
that the theme is unpublished, it is that **the product itself is still
`DRAFT`** and therefore not publicly reachable.

### What was written

| Field | Value | Class | Source |
|-------|-------|-------|--------|
| `spec.composition` | `100% Cotton` | **B** | Supplier attribute `Material: 100% Cotton` on source item `1005002281827487` |
| `spec.fit` | `Regular` | **B** | Supplier attribute `Type: regular` on the same item |

Class B means the supplier states it for this exact item but nobody has checked
it against a garment label or a tech pack. Both carry a pre-publish verification
item; `100% Cotton` in particular is a regulated claim under 16 CFR Part 303 and
must be read off the physical label before this product goes live.

### What was deliberately left blank, and why

Fifteen fields. The three that were tempting and wrong:

- **`spec.knit`** — the supplier says `Craft of weaving: Knit`. That is the
  *class* (knit rather than woven), not the *structure* the field asks for
  (Pique, Interlock, Single jersey). Writing `Knit` there would read as a
  specification while carrying no information.
- **`spec.care`** — the sentence *"Machine wash cold. Do not bleach or tumble
  dry."* appears byte-identically on all three draft polos, including the
  **polyester** one. Identical care text across cotton and polyester is copy
  pasted three times, not three labels transcribed.
- **`spec.benefits`** — the supplier's `Feature: Anti-Pilling` has no GSM, no
  pilling grade and no test standard behind it. The field's own definition
  requires each line to be checkable against a number on the same page.

The remaining twelve — `gsm`, `collar`, `placket`, `cuff`, `hem`, `finish`,
`seams`, `opacity`, `origin`, `model_height_cm`, `model_wears_size`,
`size_chart` — have no source at all.

### Verification

`userErrors: []` was treated as meaningless, per the project rule. Evidence of
persistence:

- independent re-query returns both values with `updatedAt 2026-08-22T02:35:09Z`;
- the product's `updatedAt` moved `2026-08-20T22:17:33Z` → `2026-08-22T02:35:11Z`
  — the movement `productOptionsReorder` never produced;
- all fifteen C-class fields read back `null`;
- the 20-variant matrix, captured before and after and compared field by field,
  is byte-identical (`md5 27c1e249fd97a9e0b19e223189f0eb04`);
- both sibling draft polos are untouched, `updatedAt` unmoved, no `spec.*`.

`python3 site/check-hivolt-real-product.py` → **21/21 PASS.** It renders the
real snippets against a drop transcribed from the read-back and asserts that
the fifteen blanks produce no row, no empty cell, no dash and no placeholder —
with `Pique`, `Anti-Pilling` and `Machine wash` named explicitly in the
forbidden list.

Both halves of that gate were mutation-tested rather than trusted. Injecting a
fabricated `spec.knit = "Pique"` drops it to **17/21** with four assertions
naming the fault; binding a valid chart makes the size guide emit 655 and 1,818
characters, proving the empty render comes from the guard rather than from a
harness incapable of emitting anything.

### Still unresolved, tracked separately

- **Size option display order remains wrong** — `S → M → XL → XXL → L`. Not
  touched by this pass. `productOptionsReorder` is not to be retried; see the
  section above. Needs a manual drag in the Shopify admin.
- **No size chart exists.** `spec.size_chart` is `null` and there are still 0
  `hivolt_size_chart` metaobjects, because no garment measurement exists for
  this product from any source.
- **The two detail images remain unread.**

### Gate status at close of this pass

| Gate | Result |
|---|---|
| `site/parse-liquid.py` | 32/33 — see note |
| `site/check-liquid.py` | PASS |
| `site/check-hivolt-pdp.py` | **113/113 PASS** |
| `site/check-hivolt-real-product.py` | **21/21 PASS** |

The one parse failure is `site/theme/article.liquid`, which uses `offset` as a
variable name. `offset` and `limit` are ordinary identifiers in Shopify Liquid
but reserved words in python-liquid, so this is a limitation of the local
harness rather than a defect in the file. It is pre-existing, the file is
untouched by this pass, and it belongs to the v6 theme. **All 9 liquid files in
`site/theme-v7/` — the theme that is now live — parse cleanly.**

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

**Size-ordering session (2026-08-21)**

- Two `productOptionsReorder` calls were issued against product
  `9603121774824`. Both were **no-ops**: `userErrors: []`, `updatedAt`
  unchanged, forensic diff clean on every field. No other mutation of any kind.
- MAIN `158570021096` — role `MAIN`, `updatedAt 2026-08-20T05:47:10Z`, unchanged.
- Draft `158653808872` — role `UNPUBLISHED`, `updatedAt 2026-08-20T10:00:47Z`,
  unchanged. Not published. No theme file uploaded.
- No variant created or deleted; no variant ID, SKU, barcode, price,
  compare-at, inventory or media association changed; no option or option value
  renamed; no kilogram range edited; no Colour value touched.
- No size chart created, no measurement invented, `spec.*` still empty.
- No policy, navigation, collection, redirect or page touched.
  `/pages/fabric-weight-index` untouched.

**Detail-media evidence session (2026-08-21)**

- **Zero Shopify mutations.** Every Shopify call was a `graphql_query`; the one
  AutoDS call is documented read-only. No metaobject created, no metafield
  written, no theme file uploaded.
- MAIN `158570021096` — role `MAIN`, `updatedAt 2026-08-20T05:47:10Z`, unchanged.
- Draft `158653808872` — role `UNPUBLISHED`, `updatedAt 2026-08-20T10:00:47Z`,
  unchanged. Not published.
- Target product — `updatedAt 2026-08-20T22:17:33Z`, identical to the previous
  session's closing read, so no external write occurred in between. Status
  still `DRAFT`; `spec.size_chart` still `null`; 0 `hivolt_size_chart` entries.
- No product status, title, description, price, variant, option value, order,
  SKU, barcode, inventory, swatch or SEO field touched. No policy, navigation,
  collection, redirect or page touched. `/pages/fabric-weight-index` untouched.
- The egress policy denial on `cdn.shopify.com` was reported, not circumvented.
  No proxy bypass, mirror or third-party image copy was used.

One thing worth recording rather than glossing over: product `9603121774824`
reports `updatedAt: 2026-08-20T22:17:33Z`, later than this session's first
read. No mutation was issued from here — every Shopify call this session was a
`graphql_query`, and the AutoDS call is documented read-only. A field-by-field
re-read confirms it: title, handle, vendor, description, status and variant
count are identical to the first read, and every metafield still carries its
original `updatedAt` of 06:33–06:37. The bump came from something outside this
session, most plausibly the installed Judge.me app. Nothing in scope changed.

**`spec.*` population session (2026-08-22)**

- **Two Shopify mutations, both in one `metafieldsSet` call**, both against
  product `9603121774824`: `spec.composition` and `spec.fit`. Nothing else was
  written in this session by any means.
- Product status — `DRAFT` before, `DRAFT` after. **Not published.**
- Variant matrix — 20 variants before and after, identical ids, SKUs, prices,
  barcodes, inventory quantities and selected options. No variant created,
  deleted or renamed.
- Options — `Color` and `Size` unchanged in name, id, position and value order.
  No option value renamed. No kilogram range edited. `productOptionsReorder`
  **not called.**
- `spec.size_chart` still `null`; **0** `hivolt_size_chart` metaobjects. No size
  chart created and no measurement invented.
- Sibling drafts `hivolt-slim-fit-cotton-polo-mens-long-sleeve` and
  `hivolt-anti-wrinkle-polo-mens-long-sleeve` — `updatedAt` unmoved, no
  `spec.*` written.
- No theme file uploaded, and no theme published or unpublished by this session.
  The v6→v7 role swap recorded above happened on 2026-08-21, before this
  session opened, and was made by the owner.
- No policy, navigation, collection, redirect, page, market, shipping or payment
  setting touched. `/pages/fabric-weight-index` untouched.
- No price, inventory, SKU or barcode changed anywhere in the catalogue.
- PR #2 — **not merged.**
