# Fashion Nova — site-wide audit beyond the homepage — 2026-08-30

The first audit (`FASHION-NOVA-BENCHMARK.md`) covered homepage, product card,
collection page and PDP. This one covers what it didn't: navigation taxonomy,
footer architecture, and all ten support/policy/company pages.

## 0. How this was measured

Rendered in the Higgsfield sandbox with Playwright + headless Chromium; egress
to fashionnova.com is blocked from this environment. Two passes: one over
home / collection / PDP / cart / search, one over the ten footer destinations.
9 of 10 trust pages returned; the sitemap returned but with no H1.

**Reliability note.** The homepage pass reported 43 images and 2 sections
against 169 and 9 in the first audit, and returned an empty announcement bar.
That capture fired before their client-side rendering settled — treat the
homepage image/section counts here as unreliable and use the first audit's.
The link inventories, PDP data and trust-page data below are sound.

## 1. Navigation taxonomy — 25 top-level destinations

```
Divisions   WOMEN · PLUS+CURVE · MEN · KIDS · SPORT / NEW SPORT / NEWSPORT
Categories  NEW IN · CLOTHING · DRESSES · TOPS · BOTTOMS · JEANS · JUMPSUITS
            MATCHING SETS · JACKETS & SWEATERS · SHOES · ACCESSORIES
            LINGERIE & SLEEP · GRAPHICS
Merch       SALE · NOVADEALS · NOVA LUXE · FORMAL SHOP · HALLOWEEN
```

Three shelves in one bar: who you are, what the garment is, and why you're
buying. The seasonal shelf (HALLOWEEN, FORMAL SHOP) is where merchandising
happens without touching the permanent taxonomy.

## 2. Footer — 20 destinations, four columns

Columns are `Help · Company · Quick Links · LEGAL`.

| Column | Destinations |
|---|---|
| Help | Help Center, Contact Us, Track Order, Shipping Info, Returns, Size Guide |
| Company | About, Careers, Stores, Blog, Want to Collab? |
| Quick Links | Gift Cards, Check Gift Card Balance, Sitemap |
| Legal | Privacy Policy, Terms of Service, Promo T&Cs, CA Supply Chains Act |

## 3. The ten pages, measured

| Page | Words | Accordions | H1 |
|---|---:|---:|---|
| Help Center | 1,500 | 23 | "Hi, how can we help?" |
| Sitemap (HTML) | 3,455 | — | *(none)* |
| Refunds, Credits, Exchanges | 875 | 15 | "Refunds, Credits, and Exchanges" |
| About | 669 | — | *(none)* |
| Shipping options | 620 | 9 | "Shipping options, prices, and times" |
| CA Supply Chains Act | 535 | — | "California Transparency in Supply Chains Act" |
| Size Guide | 500 | 7 | "SIZE GUIDES" |
| Careers | 405 | 20 | "JOIN THE FN FAMILY." |
| Track Order | 286 | 7 | "TRACK MY ORDER" |
| Locations | 282 | — | "New retail projects are in the works." |

### 3.1 The Help Center is a hub, not a contact form

23 accordions, FAQ segmented into `Order Issues · Gift Cards · Payments ·
Discount Codes · Policies`, opening with self-serve. The support strategy is
deflection by answering, not by hiding.

### 3.2 Track Order needs no login

A standalone page taking an order number alone. Removes the single most common
support ticket and reassures before purchase, not only after.

### 3.3 Response times are published as numbers

Measured across the pages: **within 24 hours**, **within 3 days**, **within 10
business days**. Specific and falsifiable. Shipping states a same-day cutoff at
**12pm PT**.

### 3.4 Reviews are real infrastructure, honestly displayed

The PDP captured carries 24 reviews with `Filter By Rating`, `Sort By Highest
Rated`, per-review `Helpful (n)` voting, `See all 24 reviews` and `Load More`.
The PDP in the first audit carried "No reviews yet". Same system, told the
truth in both directions.

### 3.5 They admit a limit on a page they kept anyway

The Locations page exists and its H1 says new retail projects are in the works.
A company page for stores they do not yet have, saying so. That is the single
most transferable move on the site.

## 4. Where they are weak — and HIVOLT is not

Measured across all nine pages that returned:

- **No phone number anywhere on the site.**
- **No physical address anywhere on the site.**
- The only address found is `donotreply@fashionnova.com`.
- Returns are **30 days, store credit**.

HIVOLT has a real legal entity, a street address and a working phone number,
and already offers **60 days, free prepaid label, money back — not credit**.
Every one of those is better than the benchmark, and none of them is currently
visible on the storefront.

This inverts the usual advice. On support accessibility, do not copy Fashion
Nova — beat them. A brand their size can route everyone through a help centre.
A new store cannot, and should not want to.

## 5. What to apply, ranked by trust value ÷ cost

| # | Apply | HIVOLT today | Effort |
|---:|---|---|---|
| 1 | Footer identity block: entity, address, phone, email | in schema only, invisible | trivial |
| 2 | Published response-time number | none | trivial |
| 3 | Track Order page (Shopify has this natively) | none | small |
| 4 | Help Centre hub with topic-segmented FAQ | none | medium |
| 5 | Size Guide, segmented by garment type | none | medium |
| 6 | Shipping page with a stated cutoff time | none | small |
| 7 | HTML sitemap page | none | small |
| 8 | Occasion facet on collections | none | medium |
| 9 | Persistent category sub-nav | none | medium |
| 10 | Honest review widget — including "No reviews yet" | none | medium |

## 6. What to refuse

- **Store-credit-only returns.** HIVOLT's terms are better; keep them.
- **A faceless contact route.** `donotreply@` is a big-brand privilege.
- **"Comp. Value" strike-through pricing** without genuine sales history.
- **A Careers page** for a company that is not hiring. The value of theirs is
  that the open positions are real.

## 7. What this audit does not establish

Cart and search captured poorly — the cart was empty so no payment strip
rendered, and `/search?q=` returned homepage content, so their search UX is
unmeasured. Mobile behaviour, checkout, and account pages were not visited.
No claim is made here about their conversion rate, traffic or revenue.
