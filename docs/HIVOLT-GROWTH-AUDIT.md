# HIVOLT — Growth Audit (2026-08-20)

Audit of the **actual** implementation against the Master Directive
(premium polo DTC, US/CA/UK/EU, $500K/month north star).
Every row below was verified against the live Shopify Admin API or the
repository on 2026-08-20 — no assumptions carried over from prior docs.

## Directive inputs that do not exist

Three paths named in the brief were checked and are **absent**:

| Referenced | Status | Consequence |
|---|---|---|
| `/docs/research/ecommerce-reference.txt` | **Does not exist.** `docs/` contains only `google-ads-playbook.md`, `youtube-training-series.md`, `cloud-network-allowlist.md` | §6 (APPLY/TEST/EXTERNAL/NOT-APPLICABLE classification) cannot be performed. Paste the reference or commit it to that path. |
| `/assets/brand/hivolt-logo.png` | **Does not exist.** Brand assets live at `site/impulse/hivolt-logo.png` (+ `-mark-square`, `-favicon`) | §4 "use the supplied logo as authoritative" cannot be honoured against a supplied file; the existing asset is used and preserved. |
| `CLAUDE.md` "gap analysis + $500K architecture" | `CLAUDE.md` exists but is the **Ruflo/claude-flow tooling config** — it contains no HIVOLT growth spec | The pasted Master Directive is treated as the authoritative spec instead. |

## P0 — revenue-critical

| Area | Current state (verified) | Problem | Revenue impact | Recommended change |
|---|---|---|---|---|
| **Catalogue** | `productsCount = 0` | Store sells nothing. All 95 products were deleted 2026-08-19 on owner instruction. Every collection is empty; homepage product rows render theme placeholders | **Total.** Revenue is structurally $0 until a catalogue exists | Build the polo catalogue (research running). Category is now polos, not women's activewear |
| **International market** | Market `International` (`gid://…/Market/34075607272`) is **`enabled: false`** | **Canada and every European target market cannot buy.** The market holds GB, FR, IT, ES, NL, BE, CH, IE, PL, PT, CZ, SE, NO, DK, FI, CA, AU — i.e. all of Tier 1 Canada + all of Tier 2 | Caps addressable demand at the US only — removes the majority of the directive's stated TAM | Enable the market **after** international shipping rates exist (see next row). Enabling first produces a dead checkout |
| **International shipping** | `General profile` has exactly **one zone: United States**, one rate: *FREE Tracked Shipping (8–14 business days)* @ $0.00 | New products default to General profile. With the International market enabled but no non-US zone, EU/CA shoppers reach checkout and get **"no shipping rates available"** — a hard purchase blocker | Converts an enabled market into an abandoned checkout | Add real EU/UK/CA zones to General profile with rates from the actual fulfilment partner. **OWNER INPUT REQUIRED** — real carrier cost + transit time |
| **Canada (Tier 1)** | Primary market is `United States`, handle `united-states-and-canada`, but its region list contains **only `US`** | The handle implies Canada is served; it is not. Canada sits in the disabled International market | Tier 1 market unreachable | Either add `CA` to the primary market or enable International with CAD pricing |
| **Payments** | Not verifiable via Admin API (owner-only screen) | If Shopify Payments setup is incomplete, every acquisition dollar is wasted | Total, if broken | **OWNER INPUT REQUIRED** — confirm Settings → Payments is Active, then place one live test order |

## P1 — conversion, AOV, measurement

| Area | Current state (verified) | Problem | Priority | Recommended change |
|---|---|---|---|---|
| **Brand identity vs directive** | `site/impulse/hivolt-logo.png` = boxed "HV" + wordmark + **"SPEC-FIRST APPAREL"**. Monochrome black/white | Directive §4/§5 specifies **volt/fluorescent-lime accent**, a **lightning/energy mark**, and slogan **"ACTIVATE YOUR POTENTIAL"**. Current asset carries none of these and states a different tagline | P1 | Re-cut the lockup to the specified identity, or supply the authoritative logo. Existing assets preserved either way |
| **Collection architecture** | 13 collections, all women's-activewear semantics (Leggings, Sports Bras, Dresses, Loungewear…). Title-rule based, all published, all imaged | Wrong taxonomy for a polo brand. Directive §19 wants Best Sellers / New / Performance / Golf / Solid / Prints / Seasonal | P1 | Re-map collections to polo taxonomy. Rules are title-based so they refill automatically |
| **Funnel data** | Last 14d: **801 sessions** — 693 direct (bot/self), 106 search, 2 social. 6 add-to-cart, 4 reached checkout, **0 purchases** | There is effectively no real shopper traffic. CVR is unmeasurable at this volume | P1 | Attribution + a real traffic source are prerequisites to any CRO claim |
| **Unit economics baseline** | Prior audit (`audit/FIVE-HUNDRED-K-2026-08-12.md`) measured the *deleted* catalogue: 65.7% catalogue-weighted gross margin, $46.90 avg price / $16.08 avg cost, 0 variants priced below cost | Baseline is now stale (catalogue deleted) but the **method** is sound and reusable | P1 | Re-run against the polo catalogue once built; keep `inventoryItem.unitCost` populated on every variant so margin stays scoreable |
| **Free-shipping economics** | US rate is **free at $0 minimum** | Removes the free-shipping-threshold AOV lever entirely (§15) and absorbs full shipping cost on every order, including 1-unit orders | P1 | Model a threshold (e.g. free over $X) against contribution margin before committing |
| **Analytics event model** | No custom event layer in the repo; Shopify + channel apps only | §40 event list (size_selected, bundle_viewed, cross_sell_added…) is unimplemented | P1 | Spec first (`HIVOLT-ANALYTICS-SCHEMA.md`), implement in theme once catalogue exists |

## P2 / P3

| Area | State | Note |
|---|---|---|
| Localization | No translations; no locale root URLs (`webPresence: null` on both markets) | Directive §34 — architecture-ready but nothing enabled. Do **not** machine-translate |
| Bundles / mix-and-match | None. Only an automatic "Two or more — 15% off" order-level discount | §13/§14 need a real bundle engine with platform-side pricing |
| Reviews | None installed | §29 — must be authentic; no fabricated reviews under any circumstance |
| Cookie consent | Not verified in theme | §39 — required before EU traffic |

## Standing constraints carried forward

These were established earlier in the project and remain binding:

1. **No fabricated product imagery.** 102 AI-generated garment images were purged 2026-08-10; on paid traffic this is the Merchant-Center misrepresentation class. Product photography must be real supplier imagery.
2. **No fabricated claims** — reviews, scarcity, counters, fabric specs, awards (§29/§72).
3. **Fabric/performance claims must be quoted from supplier data**, never inferred (§5).
4. Storefront domains are unreachable from the build environment (egress policy); all verification is via Admin API.

## OWNER INPUT REQUIRED

1. **The e-commerce reference document** — paste it or commit to `docs/research/`.
2. **Authoritative logo file** — the volt/lightning identity described in §4.
3. **Fulfilment partner for polos** — who ships, from where, at what cost, in what transit time (US, CA, UK, EU). Blocks all international shipping configuration.
4. **Payments status** — Settings → Payments active?
5. **Target retail price band and margin floor** for the polo line.
6. **Returns policy for EU/UK** (14-day statutory withdrawal differs from the current 60-day US promise).
