# HIVOLT — Operations Handover

Store: `hivolt-usa.com` · `f36zps-yd.myshopify.com` · Shopify Advanced · US-only
Date: 2026-08-05

---

## 1. The finding that mattered

**The store could not take money, and had never been able to.**

Zero orders in its entire history despite 3,140 sessions and 23 sessions reaching
checkout. The cause was not marketing, pricing, or SEO:

> The delivery profile holding **500 of 504 variants** (`Tapstitch: Special Line`)
> had **no location assigned to its location group**. Shopify computes shipping
> rates by matching the order's origin location to a location group inside the
> product's delivery profile. With an empty group, no rate could be computed —
> so checkout dead-ended at the shipping step with
> *"no shipping rates available for your address."*

Only the 4 Voltcore variants sat on the correctly-configured `General profile`.

**Fixed.** Location `10s225 Kaye Ln` assigned to the Tapstitch location group.

**Verified** with four live `draftOrderCalculate` runs against the real rate engine:

| Test cart | Subtotal | Rate returned |
|---|---|---|
| Flare Leggings → New York, NY | $54 | FREE US Shipping $0.00 |
| 2× Gym Tee → Mountain View, CA | $68 | FREE US Shipping $0.00 |
| Voltcore Set → Chicago, IL | $79 | FREE Tracked Shipping $0.00 |
| Soccer Jersey → Austin, TX | $38 | FREE US Shipping $0.00 |

---

## 2. Second defect: the free-shipping promise was false

98 product pages and 11 collection pages promised "Free US shipping." In reality
only the 4 Voltcore variants got it; the other 500 were quoted $3.40–$22 by weight.

**Fixed.** A `FREE US Shipping (8-14 business days)` rate at $0.00, no minimum,
added to the Tapstitch profile's United States Zone. The paid `Special Line`
tiers were left active as a fallback so US checkout can never lose all rates.

---

## 3. Everything changed, verified

| Area | Before | After |
|---|---|---|
| Active products | 98 | **110** |
| Draft products | 12 | **0** |
| Products in no gender collection | 15 | **0** |
| Products in no category collection | 18 | **0** |
| Active products out of stock | 1 | **0** |
| Meta descriptions that were size-chart dumps | 80 | **0** |
| Featured collection (homepage row) | 1 product | **13** |
| Google Search Console verification | broken (404) | **published** |
| US shipping | unquotable | **free, verified** |

Catalogue work:
- 110/110 SEO titles and meta descriptions hand-written, all under 155 chars
- 16 keyword-hostile titles rewritten ("Elevate Your Workout with Our Women's
  Cropped Sports Bra" → "Women's Cropped Sports Bra"). Handles unchanged, so no
  broken links and no redirects needed.
- 18 products retagged into the collection taxonomy (`mens`/`womens`/`tops`/
  `bottoms`/`outerwear`/`training`/`yoga`)
- Voltcore set: inventory tracking enabled, policy `CONTINUE`, 4,000 units

Discounts (all `combinesWith: false` — one code per order, no stacking):

| Code | Offer | Note |
|---|---|---|
| `VOLT20` | 20% off | Created this session. Campaign/launch code. |
| `WELCOME10` | 10% off | Pre-existing |
| `COMEBACK10` | 10% off | Pre-existing, abandoned-cart recovery |

Both "first order" codes had `appliesOncePerCustomer: false` — infinitely
reusable despite their stated purpose. **Corrected to `true`** on `VOLT20` and
`WELCOME10`. Zero risk applied, since no order has ever been placed.

---

## 4. Hero product: Voltcore 2-Piece Set ($79)

Page rebuilt on the structure that is demonstrably scaling in this category
(hook → named mechanism → outcome → proof → offer):

- Hook: *"Everyone asks where the set is from. Nobody guesses it's two pieces."*
- Mechanism: **"The 220 GSM difference"** — most leggings sit at 180–200 g/m²;
  this is 220, which is why it stays opaque through a deep squat
- Proof: the supplier specification, unedited
- SEO title: `Voltcore 2-Piece Set — Squat-Proof 220 GSM | HIVOLT`

Every claim is defensible: the fabric weight is real, the single-fabric match is
real, the $10.98 bundle saving is real.

---

## 5. Competitive intelligence (Meta ad library, live)

### Cellumove — 2,365 active ads across 2 pages, ~$187M total reach
Sells leggings as a **medical device**. Hook set:

| Angle | Copy |
|---|---|
| Cellulite | "Say goodbye to cellulite… difference in just 1 week" |
| Varicose veins | "Medical-grade legging restores blood flow… no surgery needed" |
| Lipedema | "Designed for women with Lipedema: supports lymphatic flow" |
| Heavy legs | "Do you suffer from 'Heavy Leg Syndrome'?" |
| Weight loss | "On a weight-loss journey?" |
| Chafing | "Chafing shouldn't ruin your day" |

Every ad: **BOGO free** + *"⭐⭐⭐⭐⭐ Approved by over 25,000 women worldwide."*
Advertorial funnels and fake-editorial front pages ("Womens Health Insider",
"Women's Wellness Lab").

**Do not copy this.** These are health-efficacy claims about a garment — FTC
substantiation territory in the US, potentially FDA device rules, and the
fastest route to a permanent Meta ad-account ban. Their EU-only targeting is
not a coincidence.

### Thrivin Gymwear — page-farm across 5+ pages, ~$260M total reach
Legitimate apparel marketing. **This is the model.**

| Angle | Copy |
|---|---|
| Skeptic testimonial | "I didn't believe the hype. Then I put them on." |
| Named mechanism | "Our advanced ribbing technology lifts, shapes, enhances" |
| Body outcome | "Tiny waist. Big glutes. Long legs. That's the whole point." |
| Scarcity | "Final restock. Final units. No second drop." |
| Bundle | "Mix or match any three, save 15%" |

Note: runs unbranded front pages ("Real gym talk", "Charming Chaps") pointing at
the same domain.

### Geography signal
**Every top-scaling leggings ad targets EU/UK, not the US.** Main audience
countries: DE, GB, GR, IT, IE. Zero US-primary scalers in the top ten. The US
market decision is defensible but it is the harder, more saturated one.

---

## 6. Why organic traffic is dead

130 organic sessions in 90 days against 500 blog articles and 110 products.
This is not an execution problem — the on-page work is now clean. It is a
**domain reputation problem.**

The redirect table shows this domain has hosted at least eight unrelated
businesses: collagen supplements, pheromone perfume (4 scents), a silent alarm
watch, an anti-theft sling bag, children's math/reading printables, linen
dresses, a wellness toolkit, and a German-market store.

Worse, the old URLs were repointed across topics:

```
/collections/jasmine-scent       → /collections/tops
/collections/paris-scent         → /collections/bottoms
/collections/sweet-peaches-scent → /collections/outerwear-hoodies
```

Topically irrelevant redirects are treated as soft-404s and discounted. Done
systematically, the pattern reads as laundering equity between unrelated niches.

The 500 blog articles are genuinely well-written (direct answers, real fabric
specs, comparison tables, valid `FAQPage` schema, deliberate internal linking).
But 15 of them were published inside an 8-minute window, so all 500 landed in
bulk on a zero-authority domain.

**Do not publish more articles.** Verify indexation in Search Console first.
That report decides whether organic on this domain is salvageable or a write-off.

---

## 7. Open — requires action outside the Admin API

### Blocked on the owner
1. **Place a real card order.** Shipping now quotes correctly and
   `setupRequired: false` indicates payments are configured, but the gateway
   itself is the one link never exercised.
2. **Search Console** — re-verify (the page is now live), submit
   `https://hivolt-usa.com/sitemap.xml`, read Pages → Indexing.
3. **AutoDS** — authorize in claude.ai connector settings.
4. **TikTok Shop** — OAuth in the AfterShip Feed portal. Once connected, all 110
   products can be pushed and managed programmatically.
5. **Arcads** — create a product in the Arcads web app. Scripts and actor are
   staged; generation is blocked only by `PRODUCT_SELECTION_REQUIRED`.

### Theme edits (live-theme writes are denied over API)
6. **No Product structured data.** `templates/product.liquid` and
   `snippets/gp-head.liquid` contain no `ld+json`. Blog articles emit schema;
   product pages emit none. Paste `theme/product-structured-data.liquid`.
7. **No Organization/WebSite entity.** Paste
   `theme/organization-structured-data.liquid` before `</head>`.
8. **Returns policy contradicts itself.** `templates/product.liquid` hardcodes
   "30-day returns, unworn" while the store publishes a **60-Day Love-It
   Guarantee** page. The rebuilt hero description correctly says 60 days, so
   that page now contradicts its own template. Two-string fix.

### Judgement calls left open deliberately
9. **Pricing inconsistency.** The 12 newly-published products are priced $39.99
   while the rest of the catalogue uses round numbers ($34/$38/$42/$54/$69).
   Not changed — pricing is a margin decision requiring cost basis.
10. **`VOLT20` margin.** 20% off with free shipping and no minimum means a $34
    tee nets $27.20 with shipping absorbed. Deliberate: with zero orders ever,
    maximum incentive and minimum friction is the right trade for the first
    sale. Revisit once orders are flowing.

---

## 8. Honest assessment

At an AOV near $55, $100,000 is roughly 1,800 orders — about 90,000–170,000
qualified sessions at realistic conversion rates. Current qualified traffic is
effectively zero.

That number is not reachable urgently, and not reachable at all without either
paid acquisition or a marketplace with built-in demand (TikTok Shop plus its
affiliate programme is the only realistic no-ad-spend path at that scale).

The single most valuable thing that happened here is that the store can now
accept an order. It could not before. No amount of traffic, SEO, or creative
would have produced a single dollar while shipping rates were unquotable.

Sequence from here: **verify checkout → first sale from any source → one channel
worked hard → then scale.** Stop pivoting products; the pivots are what burned
the domain.
