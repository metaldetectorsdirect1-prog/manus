# HIVOLT — CRO Roadmap

## The honest sequencing

CRO multiplies traffic. Multiplying zero gives zero. The current funnel —
~801 sessions/14d, 693 direct/bot, 0 purchases — means **conversion work
cannot be measured, let alone validated**, until two things exist:

1. A catalogue (currently 0 products)
2. Real shopper traffic

This roadmap is therefore ordered by *dependency*, not by expected lift.

## Phase 0 — Make selling possible (P0)

| Item | Type | Owner |
|---|---|---|
| Build polo catalogue with real supplier imagery | CODE | Claude |
| Confirm payments active + live test order | PLATFORM | **OWNER** |
| International shipping rates for CA/UK/EU | PLATFORM | **OWNER** (data) → Claude (config) |
| Enable International market (after rates) | PLATFORM | Claude |

## Phase 1 — Make the PDP sell (P1)

The PDP is the salesman (§9). Against the directive's above-the-fold hierarchy,
build in this order: gallery → title → price → colour swatches → size selector
→ size guide → fit guidance → ATC → delivery estimate → returns reassurance.

| Item | Note |
|---|---|
| Colour swatch selector with variant image switching | Polo colour is the primary choice |
| Size selector + dual-unit size chart (in/cm) | EU shoppers must not decode a US-only chart (§11) |
| Mobile sticky ATC | Must not show a CTA before required variants are chosen (§17) |
| Delivery estimate by market | Only from real shipping config — never invented (§36) |
| Returns clarity incl. EU/UK difference | 60-day US promise ≠ EU statutory 14-day |

## Phase 2 — AOV (P1)

Bundle engine (2/3/5), mix-and-match pack builder, cart cross-sell
("Complete Your Rotation"), free-shipping threshold modelling. **All pricing
authoritative server/platform-side** — never client-calculated (§14).

## Phase 3 — Measurement & retention (P1)

Analytics schema implementation, UTM preservation, email capture, Klaviyo-class
retention flows. Document what is external; never fake an integration (§27).

## Phase 4 — International & experiments (P2/P3)

Localization, country selector, hreflang for genuinely translated locales only,
then the experiment backlog once traffic supports significance.

## CRO scorecard — to apply per page once live

Clarity · Relevance · Trust · Desire · Friction · Anxiety · Action (§68)
