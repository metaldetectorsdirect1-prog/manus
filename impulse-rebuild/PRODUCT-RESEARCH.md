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
