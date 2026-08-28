# HIVOLT-1000-PRODUCT-RESEARCH.md — fashion best-seller backlog, 2026-08-28

Owner directive: research 1000 best-selling fashion products for the store.
Method: the AB Inner Circle Google-Ads playbook (categories not single
products; seasonal timing; compliant listing SOP; title formula) + live
Trendtrack traction signals + AutoDS supplier availability. The insertion
route is the proven one in `HIVOLT-PRODUCT-IMPORT-METHOD.md`
(`productCreate` DRAFT with supplier image URLs; read-back verified;
honest tags; zero inventory; supplier's words only).

**What "1000" means here, honestly:** the playbook's live-store sweet spot
is 500–800 products; more than that dilutes spend. So this backlog is
**1000 researched candidates feeding a live catalog of ~700–800**, with the
remainder consumed by the playbook's rotation rule (every zombie product
drafted is replaced 1:1 from the backlog). Nothing is imported in one dump:
**50/week batch pace** (or 25/day only while the GMC is fresh-approved),
because feed-change events trigger Google reviews.

## Timing (why these categories, why now)

Today is 2026-08-28. The playbook imports categories **2–3 months before
their seasonal peak, at the trough**. That makes late August exactly the
window for Oct–Jan peaks: knitwear, coats, boots, holiday dresses — and the
playbook's own worked example (letterman jackets: "import end of July, ride
Aug–Dec") is already live in ad data. Late-summer categories (linen
dresses, swim) are deliberately excluded despite currently high reach —
importing at the peak is the classic error.

## Live traction evidence (Trendtrack, pulled 2026-08-28, US-targeted ads)

Scaling fashion ads by 7-day reach growth, category 257 Fashion & Style
(credits used: ~40 of 10,000; 7,763 remaining):

| Signal | Advertiser (live ads) | 7-day reach Δ | Category confirmed |
|---|---|---|---|
| "Riviera Knit co-ords" | Mauvais (530) | +254K | Knit co-ord sets |
| "gradient boucle knit… Knit Season" | bound (289) | +407K | Statement knits |
| "Asana Wide Pant — soft brushed knit" | Ninepine (1,577) | +523K | Wide-leg knit pants |
| "Martinne chiffon overlay maxi" | Meshki (4,687) | +450K | Maxi/occasion dresses |
| "ribbed bamboo maxi slip dress" | Ninepine | +338K | Slip dresses |
| "bootcut flared jeans" | JADED MAN (203) | +446K | Bootcut/flare denim |
| "petite jeans, stylist approved" | L'AGENCE (1,170) | +212K | Fit-specific denim |
| "Baxter Mohair Knit + Woven Overshirt" | bound | +93K | Layering knits/shackets |
| Satin/backless formal minis | Rihoas (882) | +168K | Party dresses |

Top US-market fashion shops (200+ products, by active ads) for ongoing
category mining: Meshki, BloomChic, Babyboo, Scuffers, Blakely, Nude
Project, JW PEI (bags), Veinci, Miss Rosier, The Normal Brand.

## Supplier availability check (AutoDS research channel)

Query "women chunky knit sweater" (US region): returns exactly on-category
listings — e.g. Eytino chunky cable-knit pullovers, **US warehouse
(Walmart), $27.99 cost + $6.99 ship, 1–2 day delivery, MSRP ~$37–40**; and
Amazon-warehouse fleece-lined leggings at $11.99. Two honest economics
notes:
1. **US-warehouse retail-arbitrage costs mostly fail the 3.5× pricing
   floor** (a $35 landed sweater needs ~$98 retail). They win on 1–2 day
   shipping and image quality. AliExpress-region sourcing hits the floor
   but ships in ~3 weeks. The mix is an owner economics decision per
   category; every import is tagged `margin-fails-3-5x-floor` when it does.
2. AutoDS free-text search still drifts on short queries (the documented
   polo→Volkswagen failure) — **every candidate is eyeballed before
   `productCreate`**, now actually possible in-session via the sandbox
   image pipeline proven this morning.

## The 1000-candidate category tree (quotas, P=permanent / S=seasonal)

| # | Category (research keywords per title formula) | Quota | Class | Evidence |
|---|---|---:|---|---|
| 1 | Chunky/cable crew-neck sweaters | 70 | P (winter-weighted) | AutoDS verified; "Knit Season" ads scaling |
| 2 | Turtleneck sweaters | 40 | S (Oct–Feb) | store's own category |
| 3 | Cardigans — long & cropped | 50 | P | homepage category live |
| 4 | Sweater dresses | 35 | S (Oct–Jan) | knit + dress crossover |
| 5 | Knit co-ord sets | 45 | P | Mauvais +254K |
| 6 | Statement/boucle/gradient knits | 25 | S | bound +407K |
| — | **Knitwear** | **265** | | |
| 7 | Wool/tailored coats | 50 | S (Oct–Feb) | V3 brand direction |
| 8 | Puffer jackets | 40 | S (Nov–Feb) | |
| 9 | Trench coats | 25 | P (two peaks) | |
| 10 | Teddy/sherpa jackets | 30 | S | |
| 11 | Varsity/letterman jackets | 25 | S (import NOW per playbook example) | |
| 12 | Faux-leather/moto jackets | 25 | S (Sep–Dec) | |
| 13 | Shackets/overshirts | 25 | S | bound layering ad |
| — | **Outerwear** | **220** | | |
| 14 | Maxi/slip dresses | 40 | P | Meshki/Ninepine scaling |
| 15 | Cocktail/party dresses | 35 | P (peaks Nov — playbook: keep permanently) | |
| 16 | Everyday midi dresses | 30 | P | |
| 17 | Satin/formal minis | 20 | S (Nov–Dec) | Rihoas |
| — | **Dresses** | **125** | | |
| 18 | Wide-leg jeans | 30 | P | Ninepine +523K |
| 19 | Bootcut/flare jeans | 25 | P | JADED +446K; playbook 10K–100K band |
| 20 | Boyfriend/straight jeans | 25 | P (playbook market-gap example) | |
| 21 | Denim jackets | 15 | P | |
| — | **Denim** | **95** | | |
| 22 | Fleece-lined leggings | 25 | S (Oct–Feb) | AutoDS $11.99 US-warehouse |
| 23 | Wide-leg knit/lounge pants | 25 | P | Ninepine |
| 24 | Lounge/hoodie-jogger sets | 35 | P (playbook 10K–100K) | |
| 25 | Tailored trousers | 20 | P | store direction |
| — | **Bottoms & sets** | **105** | | |
| 26 | Layering basics/bodysuits | 30 | P | |
| 27 | Blouses/shirts | 25 | P | |
| 28 | Hoodies/sweatshirts | 35 | P | |
| — | **Tops** | **90** | | |
| 29 | Knee-high/heeled boots | 25 | S (Sep–Dec) | playbook title example |
| 30 | Chelsea/ankle boots | 25 | S | |
| 31 | Cowboy boots | 15 | P | |
| 32 | Sneakers | 15 | P | |
| 33 | Loafers | 10 | P (playbook 10K–100K) | |
| — | **Shoes** | **90** | | |
| 34 | Bags (unbranded) | 30 | P (Q4 gifting) | JW PEI top shop |
| 35 | Scarves/beanies/gloves | 25 | S (Oct–Jan) | |
| 36 | Belts/hair/jewelry (unbranded only) | 15 | P | |
| — | **Accessories** | **70** | | |
| | **TOTAL** | **1000** | | 60% fall/winter-seasonal-weighted, 40% permanent |

Keyword validation per playbook: each category keyword set goes through
Keyword Planner (10K–100K band = strong; 1K–10K = keep; below = only with
strongly positive 3-month change) and Google Trends 5-year seasonality —
this is an owner-side/Google-Ads-side step (Keyword Planner needs the Ads
account; egress here can't reach it) and slots into each batch's checklist.

## The batch pipeline (repeats weekly until the backlog is live)

Per batch of 50 (one week):
1. **Discover**: AutoDS `search_products` with 4–6-word category queries
   (short queries drift) + Trendtrack ad mining of the shop list above.
2. **Eyeball**: every candidate's supplier images checked with real vision
   via the sandbox pipeline. Reject: watermarks/text/logos on images,
   branded/counterfeit goods (terminal GMC risk), raw-AliExpress-quality
   photos, misrepresented garments.
3. **Title**: AB formula, 3–4 real keywords + one feeling word, unique, no
   caps, no sale text; handle matches title.
4. **Create**: `productCreate` **DRAFT**, vendor HIVOLT (never the
   supplier), supplier images via `originalSource`, category assigned, tags
   `hivolt-sourcing-candidate` + honesty tags, **zero inventory**,
   supplier's own words in description marked as such. Read-back per
   mutation rules (media READY, status, mediaCount).
5. **Owner gate**: price vs the 3.5× floor (or a deliberate AOV-strategy
   exception), then activation **in one weekly batch event**, never
   dripped — and only within GMC pacing rules.

## Hard gates before any of this goes ACTIVE (playbook phase check)

The store relaunched its storefront **today**. Per the playbook's sequence
the feed must not balloon while GMC standing is unestablished: (1) GMC
domain claim (5838274874) still pending per the earlier audit; (2) the
misrepresentation gate is designed to be triggered/cleared on a SMALL clean
store first; (3) after any approval: 4-week freeze, ads live, then paced
import. Products can be **researched and created as DRAFTS at full speed**
— activation follows the pacing. This is what protects the GMC, which is
the business.

## Standing prohibitions (unchanged)

No fake products/inventory/reviews; no invented specs (CLASS A/B only —
supplier-attributed text allowed and labeled); no counterfeit/branded
goods; no >50% discounts, ever; no AutoDS→store auto-upload (no store
connected; `productCreate` is the route); publish/activation authority is
the owner's.
