# HIVOLT — Google Commerce Readiness

Audited 2026-08-20 against the live store. **No ads launched, no campaigns
created, no spend, no Merchant Center activation, no product activation.**
This document is an assessment and a gate — not an execution.

---

## 0. Headline

HIVOLT is **NOT Merchant Center ready**, and the blockers are not feed
mechanics — they are **live content contradictions** that would fail Google's
misrepresentation review and mislead real customers today.

Three classes of problem, in severity order:

1. **Live policy text contradicts the current business** (category, GSM claim,
   international shipping) — false statements are on the site right now.
2. **100% of navigation leads to empty pages** — every menu link resolves to a
   collection with zero products.
3. Feed attributes are unbuildable until a real product exists.

---

## 1. Trust foundation audit

| Requirement | State | Note |
|---|---|---|
| Legal business name | **PRESENT** | HIVOLT |
| Business address | **PRESENT** | 10s225 Kaye Ln, Willowbrook, IL 60527, US |
| Phone | **PRESENT** | +1 914-650-2041 |
| Support email | **PRESENT** | support@hivolt-usa.com |
| Contact Information policy | **PRESENT** | Substantive, consistent |
| Privacy Policy | **PRESENT** | Shopify standard, EU/UK clauses included |
| Refund Policy | **PRESENT** | 60-day, detailed |
| Shipping Policy | **PRESENT** | Detailed — but see §2 |
| Terms of Service | **PRESENT** | Detailed — but see §2 |
| About / Our Mission | **PRESENT** | `/pages/about-us` |
| FAQ / Help Center | **PRESENT** | `/pages/faq` |
| Track Order | **PRESENT** | `/pages/track-order` |
| Accessibility statement | **PRESENT** | `/pages/accessibility` |
| Footer navigation | **PRESENT** | 4 menus wired |
| Unique professional homepage | **PARTIAL** | Structure sound; every product row is empty |
| Logical navigation | **BROKEN** | See §3 |
| Payment information | **OWNER INPUT REQUIRED** | Cannot verify Payments is active via API |

The trust *paperwork* is genuinely strong — better than most stores at this
stage. The problem is that it describes a different business.

---

## 2. POLICY CONTRADICTIONS — P0, live right now

> **Each item below now has a verbatim quote, a diagnosis, a drafted replacement
> and the owner question it turns on, in `HIVOLT-POLICY-CORRECTIONS.md`.**
> Nothing there has been applied — every one is a commercial or legal claim.

These are published, customer-facing statements that are **currently false or
will become false** under the polo / international strategy. Each is both a
Merchant Center misrepresentation risk and a consumer-trust problem.

| # | Where | Live text | Problem |
|---|---|---|---|
| **P0-1** | Terms of Service §1 | *"We sell technical activewear and gym apparel: tops, bottoms, **sports bras, leggings**, shorts, outerwear and matching sets."* | Describes the **deleted women's catalogue**. HIVOLT is now a men's polo brand. |
| **P0-2** | Terms of Service §1 | *"We **publish the fibre composition and fabric weight in grams per square metre** for each style, taken from the supplier specification sheet."* | **We cannot do this.** Zero of six polo candidates publish GSM. This is a live false claim about our own practice. |
| **P0-3** | Shipping Policy | *"HIVOLT ships within the United States only. **We do not ship internationally**"* | Directly contradicts the US/CA/UK/EU objective. Advertising in the UK while the shipping policy denies UK shipping is an automatic policy mismatch. |
| **P0-4** | Refund Policy | *"Returns are accepted from **United States addresses only**."* | Same contradiction; EU/UK consumers have statutory withdrawal rights. |
| **P0-5** | Contact Information | *"HIVOLT sells and ships within the **United States only**."* | Same. |
| **P0-6** | Shipping Policy | *"Orders are **dispatched from Illinois**"* and *"ship via USPS or UPS"* | Fulfilment partner for polos is undetermined. May be false on day one. |
| **P0-7** | `/pages/fabric-weight-index` | Page titled *"Every g/m² We Publish"* | Indexes GSM figures for deleted products; asserts a practice we cannot currently honour. |
| **P0-8** | `/pages/voltcore` | "Voltcore 2-Piece Set" landing page | Orphaned campaign page for a deleted product. |

> **These require OWNER approval to change** (policy + claims are explicitly in
> the owner lane). They are listed here, unedited, so the decision is visible.
> **Recommendation: P0-2 and P0-7 should be corrected before any traffic**, as
> they are false statements about HIVOLT's own practices rather than
> forward-looking positioning.

---

## 3. Destination / broken-link audit

Method: enumerated every menu item via Admin API and resolved each target
against live pages and collections. (Storefront HTTP crawling is unavailable —
egress policy blocks the domain — so this is a data-level resolution audit.)

| Destination class | Result |
|---|---|
| **Empty collection pages** | **11 of 11 main-menu links** resolve to collections with **0 products**: coats-jackets, knitwear, denim, dresses, leggings, sets, sports-bras, shorts, loungewear, outerwear-hoodies, and `all` (3 products, all DRAFT → renders empty) |
| **Broken page link** | `footer` menu → **`/pages/fabric-weight-index`** — page exists but is now factually stale (P0-7) |
| **Unpublished page referenced by theme** | **`/pages/size-chart` is `isPublished: false`** — the PDP size-chart block points at this handle, so the size guide will not render on any product page |
| **Orphaned landing page** | `/pages/voltcore` — product deleted |
| **Category mismatch** | Entire navigation is women's-activewear taxonomy on a men's polo brand |
| Policy links | All resolve correctly |
| Help/legal menus | All resolve correctly |

**Google impact:** a Shopping destination whose navigation is 100% empty pages
fails "unique, professional website" and "functional navigation" expectations.
This alone would jeopardise account review.

---

## 4. Product data model — feed attribute readiness

| Attribute | Source | Available today |
|---|---|---|
| Product ID / Variant ID | Shopify native | Yes (auto) |
| SKU | Shopify variant | Yes — `HV-H01-…` scheme proven |
| Brand | Shopify `vendor` | Yes — "HIVOLT" |
| Title / Description | Shopify native | Yes |
| Product type | Shopify `productType` | Yes — "Polo Shirt" |
| Google product category | **metafield / channel mapping** | **NOT SET** — needs `1604 Apparel & Accessories > Clothing > Shirts & Tops` |
| Color / Size | Variant options | Yes |
| Gender / Age group | `mm-google-shopping` metafields | Pattern proven (`male` / `adult`) |
| Material | **metafield** | **NOT SET** — needs T1 metafield schema |
| Pattern | metafield | NOT SET |
| Availability | Inventory | Yes (currently 0 — honest) |
| Condition | Static "new" | Trivial |
| Price / Compare-at | Shopify native | Price yes; **compare-at must never be fabricated** |
| **GTIN** | Variant `barcode` | **Resolved per variant, never assumed** — see §4a. No supplier has provided one yet; that is a fact about today's data, not a property of the brand |
| MPN | `mm-google-shopping.mpn` (variant) → `custom.mpn` (product) | Resolved per variant — §4a. **A HIVOLT SKU is not an MPN** unless the manufacturer issued it |
| Product / Image URLs | Shopify native | Yes |
| Shipping attributes | Delivery profiles | **US only** — see §5 |
| Market/country availability | Markets | **US only** — see §5 |

**Nothing here is invented.** GTIN absence is normal for own-brand apparel and
is declared, not fabricated.

---

## 4a. Unique product identifiers — configurable per SKU

Built 2026-08-20. `snippets/hivolt-identifier.liquid` in the draft theme.

The earlier version of this document said to send `identifier_exists: false`.
That was wrong as an architecture even though it is right as today's answer:
it hardcodes a temporary fact about the six candidate suppliers into the feed
logic, and it would keep sending `false` on the day a supplier does hand over a
barcode. Identifier handling is now **data, resolved per variant**.

### The three cases

| Mode | Condition | Feed sends | JSON-LD emits |
|---|---|---|---|
| `gtin` | Variant `barcode` holds 8, 12, 13 or 14 digits | `gtin`, `identifier_exists=yes` | `gtin` + `gtin{8,12,13,14}` |
| `brand_mpn` | No barcode, but `vendor` and a real MPN both exist | `brand`, `mpn`, `identifier_exists=yes` | `mpn` (brand is always emitted) |
| `none` | Neither | `identifier_exists=no` | nothing |

### Where the mode comes from

```
variant.metafields.custom.identifier_mode      (per-SKU override)
  → product.metafields.custom.identifier_mode   (family default)
    → 'auto'                                    (when both are blank)
```

Both metafields are constrained to `auto | gtin | brand_mpn | none`.

`auto` inspects the data and picks the highest case that is actually satisfied.
The explicit modes exist for the case the data cannot express — one colourway
carrying a supplier barcode while the rest do not, or a supplier number that
must not be published.

### The resolver verifies before it trusts

Declaring `gtin` on a product whose variants have no barcode does **not**
produce a GTIN. The resolver checks the value, finds nothing, and falls through
to `none`. The same is true of `brand_mpn` with no MPN stored. A mislabelled
product degrades to "no identifier", which is a correct statement, rather than
shipping a fabricated one.

A GTIN is validated on shape as well as presence: every digit is stripped and
the remainder must be empty, and the length must be 8, 12, 13 or 14. `HV-POLO-BLK-M`
in the barcode field resolves to `none`, not to a malformed GTIN.

### What is never used as an identifier

- Shopify variant IDs (`gid://shopify/ProductVariant/…` or the bare number).
- HIVOLT's own SKU scheme (`HV-P01-…`). A SKU is an internal stock code; an
  MPN is issued by whoever manufactured the item. They are only the same number
  if HIVOLT is the manufacturer of record, which is a decision, not a default.
- Any value generated to satisfy a validator.

### Verified by

`site/check-hivolt-pdp.py` — seven cases covering each mode, an invalid
barcode, a wrong-length barcode, a declared-but-unsupported mode, and a variant
override beating the product default.

---

## 5. Country readiness

| Market | Status | Blocking facts |
|---|---|---|
| **USA** | **BLOCKED** | Market enabled ✓, USD ✓, shipping zone ✓ (free, 8–14 days) ✓ — but **catalogue is empty** and **payments unverified**. No customer can complete an order. |
| **Canada** | **NOT CONFIGURED** | In the **disabled** International market. No CAD presentment, no shipping zone in General profile, no delivery estimate, no returns destination. |
| **UK** | **NOT CONFIGURED** | Same. Plus VAT registration status unknown, duties model undecided. |
| **EU** | **NOT CONFIGURED** | Same. Plus per-country currency (EUR/SEK/NOK/DKK/PLN/CZK), 14-day statutory withdrawal, cookie consent — none configured. |

**No country may be advertised until a real customer can complete an order
there.** Today that is true of zero countries.

---

## 6. Google & YouTube channel — observed state only

| Item | Observed |
|---|---|
| Channel installed | **Yes** — publication `Google & YouTube` exists (`gid://shopify/Publication/188349939944`) |
| Products synced | **0** — no product is published to it |
| Merchant Center account | Referenced in prior project notes as **5838274874**; **claim status unverified** — not confirmable via Shopify Admin API |
| Errors / warnings | Not visible through this API surface |

**No action taken** — no install, connect, activate or account-relationship
change, per instruction. Owner steps required: sign into Merchant Center,
confirm account claim and domain verification, review any standing policy
warnings.

---

## 7. Feed health checklist (pre-flight, before any activation)

- [ ] Every product has ≥1 image ≥800×800, accurate, unmanipulated
- [ ] Titles follow feed architecture (§8) without unsupported keywords
- [ ] Descriptions contain no claim absent from supplier spec
- [ ] Price in feed == price on landing page == price at checkout
- [ ] Availability in feed == real inventory
- [ ] Landing page returns 200, not an empty collection
- [ ] Google product category mapped
- [ ] Identifier mode resolves correctly per variant (§4a) — `identifier_exists=no` only where the resolver confirms there is nothing real to send
- [ ] Shipping in feed matches configured rates for that country
- [ ] Policy pages consistent with feed countries (**currently fails — §2**)
- [ ] Currency matches market presentment
- [ ] No product advertised into a country that cannot be shipped

---

## 8. Title architecture — storefront vs feed

Keep them **separate**. The premium PDP title stays clean; feed titles carry
search relevance.

| Surface | Pattern | Example |
|---|---|---|
| Storefront PDP | Brand + clean product name | `HIVOLT Classic Cotton Polo` |
| Feed | Brand + Type + verified attribute + colour | `HIVOLT Men's Cotton Polo Shirt — Short Sleeve — Navy` |

**Built 2026-08-20.** `custom.feed_title` (product, max 150 chars) holds the
feed title; `snippets/hivolt-feed-title.liquid` resolves it. Blank falls back to
the storefront title — a deliberate fallback, not a gap, since the storefront
title is itself a valid feed title. Passing a variant appends its options, which
is what an item-level row needs, and the result is truncated at Merchant
Center's 150-character limit so the words that survive are the ones we chose.

The feed title is used **only** in feeds. Structured data and the PDP both read
the storefront title, so the markup can never contradict what the shopper sees.

Consumer: Shopify's Google & YouTube channel has no title-override field, so
`custom.feed_title` is read by a Merchant Center **supplemental feed**, keyed on
item id. Any feed writer built later reads the same metafield rather than
re-deriving the rule.

**Every attribute in a feed title must be verified** — "performance", "stretch",
"moisture-wicking" may not appear unless the supplier spec states them.

---

## 9. Structured data

**Built 2026-08-20** in the draft theme:
`snippets/hivolt-structured-data.liquid`, rendered in `<head>` on every page.
The live theme has **no** structured data of any kind — this is net new.

| Type | Status | Note |
|---|---|---|
| Organization | Built | Name, url, `sameAs` from non-blank social settings. `logo` only when the favicon is ≥112 px, per Google's minimum |
| WebSite | Built | Publisher points at the Organization node |
| BreadcrumbList | Built | Product, collection, page and article. Includes the collection step only when the product was reached through one |
| Product | Built | Product pages only. Name, url, description, up to 8 images, brand from `vendor` |
| Offer | Built | **One Offer per variant**, each with its own url, sku, identifiers, price and availability |
| **Review / AggregateRating** | **PROHIBITED — no code path exists** | No real review data. A test asserts neither string can appear in the output |

Deliberately **not** emitted, each because it encodes a commitment nobody has
made: `priceValidUntil`, `shippingDetails`, `hasMerchantReturnPolicy`. They
belong here once shipping, duties and returns are settled per market (P-3, P-4
in `HIVOLT-POLICY-CORRECTIONS.md`), and not before.

Consistency is structural rather than promised: price, currency, availability,
title, variant and URL are read from the same Liquid drops the page renders
from, so the markup cannot drift from the visible page. Prices come from
`variant.price` and the currency from `cart.currency.iso_code`, which follow the
shopper's market automatically.

Where a GemPages template is active the Product node stands down, so a crawler
never gets two answers on one page.

**Verified by** `site/check-hivolt-pdp.py`: the output parses as JSON, the graph
contains exactly the expected node types, availability tracks each variant
independently, `gtin` appears only for a real barcode, and no rating or review
string is present.

---

## 10. GATE STATUS

**GATE A — PRODUCT:** 0/10. No approved product, supplier, samples, specs,
pricing, inventory or photography.

**GATE B — STORE:** 4/9. Policies ✓, contact ✓, About ✓, cart/checkout
architecture intact. Failing: PDP (no products), mobile QA (nothing to test),
payments unverified, **critical broken/empty destinations (§3)**.

**GATE C — OPERATIONS:** 0/7. No verified shipping for any country, no returns
path beyond US text, no fulfilment process, no tested lead time.

**GATE D — DATA:** 0/4. No feed, no conversion tracking verified, no purchase
value, no attribution.

**Overall: 4 of 30. Merchant Center activation is far out, and correctly so.**

---

## 11. What must happen before Merchant Center readiness

**Owner-gated (blocking):**
1. Approve sourcing path → real product, specs, samples, photography
2. Approve pricing
3. Confirm payments active
4. Provide fulfilment origin/carrier/cost/transit per country
5. Approve policy corrections in §2
6. Confirm Merchant Center account claim + domain verification

**Claude can do once (1) lands:** catalogue build, feed metafields, Google
category mapping, feed-title architecture, structured data, PDP completion,
collection re-architecture, mobile QA, performance and accessibility passes.

**Claude can do now (product-independent):** metafield schema, size-guide
system, swatch selector, PDP template, analytics layer, UTM preservation,
consent scaffold, structured-data templates — all on unpublished theme copies.
