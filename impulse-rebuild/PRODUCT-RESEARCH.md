# PRODUCT-RESEARCH.md

Product/category research for HIVOLT, run 2026-08-26 against the `topgoogle`
playbook's Module 7.1 method.

---

## 🔴 Read this before the shortlist: the first import is 5 products, not 500

The playbook's single hardest rule is sequence. HIVOLT has **zero products** and
has **not yet run the deliberate misrepresentation campaign**. In that state:

> *"Trigger the suspension early, on purpose … while the store is 5 clean products
> in one niche, because that is the easiest state to appeal from. You get 3 appeals
> per GMC — no more."*

**Importing a broad catalogue before that suspension is cleared means appealing
across hundreds of products instead of five.** The 500–700 product target is a
Phase 5 number, reached *after* approval and *after* a 4-week freeze. It is not a
starting position.

So this document answers two different questions, and they have different answers:

| Question | Answer |
|---|---|
| What do we import **first** | ~5 products, **one tight category** |
| What do we import **later** (weeks 4–10) | the shortlist in §3, at 25/day or 50/week |

---

## §1 What I measured, and what I could not

**Measured — live competitor data (TrendTrack, 2026-08-26):**
Apparel shops with ≥20 active ads and ≥50k monthly visits, US audience.

| | |
|---|---|
| Apparel shops in sample | 19 |
| Running **live Google ads** | **13** |
| Combined live Google ads | **633** |
| Google ads launched in last 30 days | **119** |

The category is actively contested on Google right now — that is a real signal,
not an inference.

**Not measured, and I will not invent it:** Google Keyword Planner search-volume
bands (the playbook's 10K–100K / 1K–10K / 100–1K filters) and Google Trends
5-year seasonality curves. Both require a Google Ads login this integration does
not have. **No search volume in this document is a number I produced.** Where the
playbook's own worked examples give a curve, it is cited as the playbook's, not
mine. §5 hands you the exact procedure to run those two tools yourself — it is
about twenty minutes of work and it is the part that cannot be delegated here.

---

## §2 Two findings from the competitor data worth acting on

### 2.1 Almost nobody is at the playbook's target catalogue size

| Shop | Products | Live Google ads | vs 500–700 target |
|---|--:|--:|---|
| daisysilk.com | 809 | **271** | above |
| selurewear.com | 29 | 103 | far below |
| sexymodest.com | 412 | 73 | below |
| enzocavalli.com | 43 | 59 | far below |
| nuagewears.com | 103 | 41 | below |
| nautinati.com | 500 | 4 | **at target** |

Most shops spending hard on Google are running **very small catalogues very
aggressively** — 29 products against 103 live ads. That is the opposite of the
playbook's feed-volume model. Neither is wrong, but they are different businesses,
and HIVOLT should pick one deliberately rather than drift between them.

### 2.2 The top Google spender is showing the exact failure the playbook warns about

`daisysilk.com` platform mix across 271 live ads:

| Platform | Ads |
|---|--:|
| Search | **497** |
| Other | 80 |
| YouTube | 58 |
| **Shopping** | **43** |

The playbook's §8.2 gotcha is *"forgetting to disable asset optimization = budget
bleeding into YouTube/Search/Gmail instead of Shopping."* This is what that looks
like from the outside. Whether daisysilk intends it or not, it is a live example
of why the PMax build in §8.2 says to **disable the asset-generation toggles** so
the campaign serves the Shopping feed only.

---

## §3 Category shortlist for HIVOLT

Filtered by three things: Q4 timing, HIVOLT's existing collection tree, and
whether the category lets the brand's actual position ("we publish fabric weight
and composition; where we don't have it we say so") do any work.

| Category | HIVOLT collection exists | Q4 fit | Why it suits *this* brand |
|---|:--:|---|---|
| **Knitwear** — cardigans, turtlenecks, cable knit | ✅ `knitwear` | peak season | **Strongest.** Fibre composition is the decisive spec in knitwear — wool vs merino vs acrylic blend is what the buyer actually wants and what most stores hide |
| **Outerwear** — puffers, wool coats, parkas | ✅ `coats-jackets` | peak season | Fill weight, shell composition and lining are publishable specs |
| **Denim** — wide-leg, barrel, straight | ✅ `denim` | permanent | Playbook names *boyfriend jeans* as high-demand/low-supply. Denim weight in oz is a real publishable figure |
| **Loungewear / matching sets** | ✅ `loungewear`, `sets` | rises into Q4 | The live 15% two-or-more discount is naturally a set-seller |
| **Dresses** — cocktail, knit midi | ✅ `dresses` | playbook: cocktail dress *"peaks November, keep permanently"* | |

**Timing, from the playbook's own worked examples:** import at the trough, never
the peak, 2–3 months before demand — product indexes roughly a month after
import. Late August is the correct window for Q4 knitwear and outerwear. It is
already slightly late for letterman/varsity jackets, which the playbook says to
import *end of July*.

---

## §4 The opening 5 — one tight category: knitwear

Recommended because it is the only category where three things line up:

1. **Q4 timing is correct right now** — imported at the trough, peaks Nov–Dec.
2. **The supporting content already exists and is published.** `/pages/care-guide` covers wool, merino and cashmere with citations to ISO 3758 and ASTM D5489. A GMC reviewer landing on a knitwear product page can follow a link to genuine, sourced care guidance. That is a trust signal the store already owns.
3. **It plays to the brand's position.** Composition is the whole argument in knitwear, and HIVOLT's entire published standard is about composition.

### Titles, using the playbook's formula

`[optional first name] + [feeling word] + [3–4 researched keywords]` — no caps,
unique, upcoming season named, gender word optional.

| Title | Ranks for |
|---|---|
| Elena relaxed merino wool turtleneck sweater | merino sweater · wool sweater · turtleneck sweater · relaxed sweater |
| Warm cable knit cardigan with pockets | cable knit · knit cardigan · cardigan with pockets |
| Nora oversized chunky knit winter sweater | oversized sweater · chunky knit · winter sweater · knit sweater |
| Elegant longline wool blend cardigan | longline cardigan · wool cardigan · wool blend cardigan |
| Ivy soft ribbed knit turtleneck jumper | ribbed knit · knit turtleneck · turtleneck jumper |

Each carries 3–4 keywords, one feeling word, and names **winter** — the upcoming
season, not the current one. Verify every keyword in Keyword Planner before use;
I have not measured their volume.

### §4.1 AutoDS sourcing brief — how the owner fills the 5 slots (added 2026-08-27)

AutoDS is the confirmed supplier route (fulfillment service live on the store).
In the AutoDS marketplace, one search per slot; import each pick as **DRAFT**:

| Slot | Search in AutoDS | Title waiting for it |
|---|---|---|
| 1 | `merino wool turtleneck sweater women` | Elena relaxed merino wool turtleneck sweater |
| 2 | `cable knit cardigan pockets` | Warm cable knit cardigan with pockets |
| 3 | `oversized chunky knit sweater` | Nora oversized chunky knit winter sweater |
| 4 | `longline wool blend cardigan` | Elegant longline wool blend cardigan |
| 5 | `ribbed knit turtleneck jumper` | Ivy soft ribbed knit turtleneck jumper |

Pick rules, in refusal order (skip a candidate the moment it fails one):

1. **No brand names, logos, or lookalike branding anywhere** on garment or
   images — copyright is the terminal, unappealable suspension.
2. **Images**: single product, neutral background, no watermarks, no text
   overlays, no Chinese characters, not obviously AliExpress-staged.
3. **Variant depth**: target ≥4 sizes × ≥3 colors (playbook ideal ≈ 6×5).
4. **Ships US and UK**, stated delivery ≤ ~12 days.
5. **Cost** such that retail lands **$34.95–$59.95** at 2.5–3× markup,
   shipping included.
6. Composition listed by the supplier (we publish only what the supplier
   states — no invented fabric claims; gaps become `[[NEEDS:]]`).

Titles above are pre-built to the formula but **unverified in Keyword
Planner** — the §5 owner run still applies before ads spend against them.
On landing, every draft gets the full SOP pass (title/description rewrite,
EXIF strip, handle regen, .95 price, vendor = store name, `--batch` gate).

### §4.2 Sourcing round 1 — AutoDS catalog, 2026-08-27 (agent sweep)

Confirmed picks (screened for brand-risk, images-by-metadata, variants,
shipping, margin; **image pixels unverifiable from this environment — human
spot-check for watermarks/Chinese text before publishing**):

| Slot | AutoDS `_id` | Site / item | Landed cost | Variants | Composition (supplier-stated) | Retail |
|---|---|---|---|---|---|---|
| 1 | `6957787ef76d530001901236` | AliExpress 3256807242236207 | ~$16–18, free ship 13d | 4 sizes × ~17 colors | "100% Australia Extrafine Merino Wool" (mock-neck) | $44.95 |
| 3 | `6a03c53539ba4b00017a54f5` | Walmart 5030481746 (US warehouse, 1–2d) | ~$30–32 | 5 sizes × 9 colors (full matrix) | 45% acrylic / 55% polyester | $59.95 |
| 5 (fallback) | `673bc7b27126c18f62f09c9d` | AliExpress 3256807073935486 | ~$16, free ship 13d | 4 sizes × 10 colors | conflicting — publish only "30% merino wool blend" | $39.95 |

Rule flexes recorded: shipping ≤14 stated days (policy pages will state 8–15
business days honestly); US-warehouse landed cost to $32 with a real variant
matrix.

**Round 2 (same day):** slot 4 filled — private-supplier wool-blend longline
cardigan, `6a2a0d70b2166070237a654b` (item 10282354278688), $18.30 landed,
free 11–14d, **5 sizes × 6 colors = 30 variants**, publishable only as
"wool blend" (no percentages stated) → retail $49.95. ⚠️ Its image filenames
read Dutch ("kath-vest-van-wol-en-mohair…deqalli") — likely lifted from
another store ("Deqalli"); the de-linking chain plus a human image check is
mandatory before it publishes. Slot 5 = the round-1 fallback promoted (13-day
shipping now inside the flex). **Slot 2: no compliant cable-pocket cardigan
exists in the catalog** — nearest miss DOKOTOO `6d5a06926ee704c7a6d14530` at
$41.58 landed would need $79.95 retail; held as alternate, not a pick.
Round 3 running: one distinct fifth silhouette (sweater vest, or plain button
cardigan without cable/chunky).

Dropped with reasons across rounds: first private-supplier longline (no
composition stated — unpublishable under §1.2), all single-variant
Walmart/Amazon listings, v28 sweater dresses (wrong garment + cost),
everything with unstated composition.

### §4.3 THE BATCH — final five, locked 2026-08-27

Round 3 found no compliant fifth silhouette (all US-warehouse vests and
button cardigans land ≥$34.98; the sole under-cap item had no stated
composition). Decision: the round-1 DOKOTOO cable-pocket cardigan enters at
an honest 1.9× ($79.95 on $41.58 landed) — thin margin accepted, carried by
US 1–2-day shipping; **no fabricated compare-at price.**

| # | Final title (stack ≥3 ✓) | AutoDS `_id` | Retail |
|---|---|---|---|
| 1 | Elena relaxed merino wool mock neck sweater | `6957787ef76d530001901236` | $44.95 |
| 2 | Nora oversized chunky knit winter sweater | `6a03c53539ba4b00017a54f5` | $59.95 |
| 3 | Elegant longline wool blend cardigan | `6a2a0d70b2166070237a654b` | $49.95 |
| 4 | Ivy soft knit merino blend mock neck sweater | `673bc7b27126c18f62f09c9d` | $39.95 |
| 5 | Warm cable knit cardigan with pockets | `6d5a06926ee704c7a6d14530` | $79.95 |

Titles renamed true-to-garment (mock neck, not turtleneck — the honesty rule
outranks keyword volume); master list grew 8 forms the titles were designed
against (640→648). Gate: titles/prices/handles/vendor pass; full `--batch`
re-runs at import with real images and copy (image-less products are
refused by design). Blocked on: AutoDS store link (LAUNCH-RUNBOOK 0.2).

### §4.3.1 OUTCOME — four of five live as Shopify drafts, 2026-08-27

Store linked (AutoDS store id `5685625`) and uploaded through AutoDS for
fulfillment mapping, then SOP-passed in Shopify (status→DRAFT, sentence-case
titles, clean descriptions, tags). All images re-hosted on the store's CDN.

| Product | Shopify GID | Price | Variants |
|---|---|---|---|
| Elena relaxed merino wool mock neck sweater | `9613182468328` | 44.95 | 68 |
| Nora oversized chunky knit winter sweater | `9613182435560` | 59.95 | 1 |
| Ivy soft chunky knit turtleneck sweater | `9613182370024` | 54.95 | 1 |
| Warm cable knit cardigan with pockets | `9613182402792` | 79.95 | 1 |

Changes from §4.3 as planned: the original Ivy (merino-blend mock neck,
AliExpress `3256807073935486`) died at upload — supplier listing gone
("ScrapersProductOOS") — replaced by the round-1 Amazon alternate
`B09MYYL7D6` as a chunky turtleneck (title stacks 3). **Single-variant
reality accepted:** Walmart/Amazon supplier listings sell one size/color per
listing; padding Shopify variants beyond what the supplier item delivers
would sell unfulfillable goods, so those three stay 1-variant. Fifth product
(private-supplier longline `10282354278688`): no documented API site enum —
owner imports it in the AutoDS marketplace UI (search the item id → import
as draft), then it gets the same SOP pass. Owner image spot-check before
anything publishes still stands.

### §4.4 Upload spec — executable from any session once a store row exists

Preconditions: `list_stores_api` returns ≥1 store (capture its AutoDS store
id); connector account = the one holding the store. Then three
`upload_products` calls (buy_site_id is per-request), each with
`region: 1` (US), `status: 1` (**draft**), `upload_settings.tag:
["knitwear"]`:

| Call | `buy_site_id` | `new_products[].asin` |
|---|---|---|
| AliExpress | 2 | `3256807242236207` (Elena, $44.95) · `3256807073935486` (Ivy, $39.95) |
| Walmart | 4 | `5030481746` (Nora, $59.95) · `326807556` (Warm cable, $79.95) |
| Private supplier | (resolve enum from server instructions; if unsupported, add item `10282354278688` manually in AutoDS UI) | `10282354278688` (Elegant longline, $49.95) |

Pass each product's retail as `price`. Poll `get_bulk_action_items` with the
returned `bulk_action.id`. Then verify in **Shopify** (authoritative read:
products exist, status DRAFT), run the SOP pass per §4.1/§4.3, and only then
continue the LAUNCH-RUNBOOK sequence. Owner image spot-check in AutoDS
before anything publishes — this environment cannot render the image CDNs.

- Images: single product, neutral background, **no AliExpress photos, watermarks, logos or Chinese text**
- **No images inside the description** — a named suspension trigger
- **URL handle must match the final title** — the playbook calls this *"a top automatic-indexing trigger"*
- Vendor filled transparently — **never** an AliExpress/CJ-style supplier name
- Every product assigned to a real, **non-empty** collection
- Discount ≤ 50%; not every product discounted

---

## §5 What you have to run yourself — ~20 minutes

I cannot reach Keyword Planner or Trends. This is the part of Module 7.1 that
must be done in your own Google Ads login:

1. **Google Ads → Tools → Keyword Planner → Get search volume and forecasts.**
2. Paste the §3 categories plus their sub-categories (cable knit cardigan, merino turtleneck, wool coat, puffer jacket, wide-leg jeans, cocktail dress…).
3. Read **average monthly searches** and **3-month change**. Keep 10K–100K; keep 1K–10K; drop 100–1K **unless** the 3-month change is strongly positive.
4. Take each survivor to **trends.google.com** → country US → **last 5 years** → note the all-time high and low month.
5. Label each **permanent** (keep forever) or **seasonal** (import at trough, draft after peak).
6. Save the list. The playbook is explicit that you build it once and reuse it.

---

## §6 What actually blocks importing anything

**No supplier is confirmed.** That has been the standing blocker across this
engagement, and it is unchanged. Without one there is no composition, no fabric
weight, no garment measurement and no dispatch window — which means a HIVOLT
product page cannot currently meet the store's own published standard.

That is not a reason to lower the standard. It is the reason the first import is
five products: five is a small enough number to get real supplier specification
sheets for.

**Nothing was added to Shopify by this research.** The store still holds zero
products.

---

## §7 Honesty note on the source

The playbook records one practitioner team's method. Parts of it sit in grey
areas — anti-detect browsers, purchased followers, **purchased reviews**, paid
insider approvals. None are applied here and none are recommended. Purchased or
fabricated reviews in particular are the exact defect class this rebuild has
spent six sessions removing.

Google's policies and the GMC interface change; verify anything time-sensitive
before acting on it.

---

## §8 The 400 — Phase 5 allocation (provisional, awaiting scored keywords)

Owner asked (2026-08-27) to add 400 women's fashion products. The skill's
timeline is unambiguous: **400–600 is Phase 5, imported at 25/day or
50–100/week starting when the 4-week post-approval freeze ends** — with the
gauntlet starting now, that is roughly late October. Importing 400 before the
misrepresentation suspension clears would put all 400 inside the appeal
(3 appeals per GMC, then dead). The research starts now; the imports start on
the timeline.

Provisional allocation per FEED-CALENDAR §4 mix (40% permanent / 45%
in-season / 15% early-next), sized for a late-Oct start toward the Nov–Dec
peak. Counts firm up when the owner's Keyword Planner run fills
`keywords/scored-list.csv`:

| Block | Category | Count |
|---|---|---|
| Permanent (160) | Jeans & denim | 40 |
| | Everyday dresses | 40 |
| | Tops & basics | 40 |
| | Lounge & activewear | 25 |
| | Knit basics | 15 |
| In-season (180) | Coats & jackets (wool, puffer, leather/suede) | 60 |
| | Knitwear expansion (cardigans, sweaters, vests) | 50 |
| | Holiday & party dresses | 40 |
| | Boots | 30 |
| Early-next (60) | Spring dresses | 25 |
| | Light jackets & trench | 20 |
| | Spring knits | 15 |

Sourcing per batch runs the §4.1 pick rules through AutoDS (now linked) plus
the competitor sourcing index (big players in both tracker CSVs); every batch
takes the SOP pass and the compliance gate before it accumulates as drafts.
