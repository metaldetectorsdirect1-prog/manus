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
| **GTIN** | **Supplier** | **NOT AVAILABLE** — marketplace suppliers provide none. Own-brand goods legitimately have no GTIN; use `identifier_exists: false` rather than inventing one |
| MPN | Own SKU can serve | Yes |
| Product / Image URLs | Shopify native | Yes |
| Shipping attributes | Delivery profiles | **US only** — see §5 |
| Market/country availability | Markets | **US only** — see §5 |

**Nothing here is invented.** GTIN absence is normal for own-brand apparel and
is declared, not fabricated.

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
- [ ] `identifier_exists: false` where no GTIN exists
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

Implementation: a `custom.feed_title` metafield overriding the channel title,
so advertising relevance never degrades the storefront. **Every attribute in a
feed title must be verified** — "performance", "stretch", "moisture-wicking"
may not appear unless the supplier spec states them.

---

## 9. Structured data

| Type | Status | Note |
|---|---|---|
| Product | To implement | Must match visible price/availability exactly |
| Offer | To implement | Currency + availability from live data |
| BreadcrumbList | To implement | Theme has breadcrumbs enabled |
| Organization | To implement | Name, logo, contact, address all available |
| **Review / AggregateRating** | **PROHIBITED** | No real review data exists. Emitting it would be fabricated markup. |

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
