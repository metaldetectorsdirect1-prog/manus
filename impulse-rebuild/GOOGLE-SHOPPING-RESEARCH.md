# GOOGLE-SHOPPING-RESEARCH.md

Which women's / general apparel stores are actually scaling **on Google Shopping**,
2026-08-26. Google only — Meta-driven shops are excluded by construction.

---

## §1 Method, and its limits

**Source:** TrendTrack shop index. Two queries (`women`, `dress`), US audience,
≥30,000 monthly visits, merged and deduplicated.

**The Google-only filter that matters:** every shop below has a
`platformMix` entry for **`Shopping`** with a non-zero ad count. A shop running
only Search or YouTube ads is excluded even if its Google spend is large.

| | |
|---|--:|
| Apparel shops found running **live Google Shopping ads** | **52** |
| Combined Shopping ads across the sample | ~600 |

### Three caveats, stated rather than buried

1. **"Scaling" here means ad-launch velocity, not traffic growth.** I ranked by `adsLaunched30d` — new Google ads put live in the last 30 days. Reported `growth30d` for most of these shops is **1–3%**, not the double-digit growth the word "scaling" implies.
2. **A filter I set did not apply.** I requested `traffic_growth last30d ≥ 15%`; results came back at 1–3%. The filter appears not to have constrained the result set, so every growth figure below is read from the returned field directly, not from the filter.
3. **This is not a census.** It is the shops TrendTrack indexes in its trending feed above the traffic floor, from two keyword queries. Shops it does not index are invisible here.

---

## §2 The stores actually scaling on Google Shopping

Ranked by Google ads launched in the last 30 days.

| # | Store | Country | Born | Products | Monthly visits | Shopping ads | **New ads 30d** |
|--:|---|---|---|--:|--:|--:|--:|
| 1 | **pomuyoo.com** | 🇨🇳 CN | 2023-05 | **1,786** | 184,571 | 75 | **66** |
| 2 | **smukoslo.no** | 🇳🇴 NO | 2024-01 | 250 | 30,631 | **89** | **28** |
| 3 | **averymae.com** | 🇺🇸 US | 2024-06 | **4,961** | 52,007 | 12 | **23** |
| 4 | pointcarre.be | 🇧🇪 BE | 2025-04 | 16,056 | 129,684 | 36 | 13 |
| 5 | francisbyfb.com | 🇳🇱 NL | 2021-02 | 191 | 180,906 | 3 | 12 |
| 6 | vrajbhoomi.in | 🇮🇳 IN | 2023-02 | 250 | 78,847 | 21 | 11 |
| 7 | outdoorvoices.com | 🇺🇸 US | 2020-11 | 573 | 342,312 | 21 | 10 |
| 8 | fkofficial.it | 🇮🇹 IT | 2022-09 | 2,724 | 119,477 | 22 | 9 |

### The three worth studying

**`pomuyoo.com`** — the closest match to the model being described here.
Chinese-registered, three years old, 1,786 products, and **66 new Google ads in
30 days — the highest launch velocity in the sample.** All 279 of its Google ads
target the **US only**. Its catalogue is unisex, not women's-only (bestsellers are
men's three-piece suits at $139).

One detail worth copying: its top "bestseller" is **"Chiffon Swatches" at $1**.
Cheap swatch SKUs are a known way to widen a Shopping feed and pick up
low-competition impressions. It is a feed tactic, not a margin product.

**`smukoslo.no`** — the cleanest **women's general fashion** store scaling here.
Norway only, 250 products, **89 Shopping ads** — the second-highest Shopping count
in the sample from a quarter of pomuyoo's catalogue. Coat dresses, jeans, hair
claws. This is the playbook's *"on a tight budget, start in smaller markets — GMC
approval is easier and lasts longer"* thesis, running live.

**`averymae.com`** — US women's, opened **June 2024**, already at **4,961
products** with 23 new Google ads in 30 days. Bestsellers are Judy Blue denim and
reversible basics. A US boutique operating at roughly **7× the playbook's 500–700
target** and still launching ads.

### The outlier worth understanding

**`xenaworkwear.com`** — US, **29 products**, and **555 Shopping ads**. Women's
safety footwear. Its entire Google mix is Shopping 555 / Search 168 / Other 6 — a
near-pure Shopping account. It is the inverse of the feed-volume model: a tiny,
tightly-defined catalogue pushed extremely hard. Not a general store, but proof
that catalogue size is not what wins Shopping.

---

## §3 What the data actually says about catalogue size

| Products | Store | Shopping ads |
|--:|---|--:|
| 29 | xenaworkwear.com | **555** |
| 250 | smukoslo.no | 89 |
| 1,786 | pomuyoo.com | 75 |
| 4,961 | averymae.com | 12 |
| 16,056 | pointcarre.be | 36 |

**Shopping ad volume does not track catalogue size in this sample — if anything it
runs the other way.** The 29-product store has 46× the Shopping ads of the
4,961-product store.

That does not disprove the playbook's 500–700 target; the playbook's argument is
about *feed breadth capturing more long-tail searches*, which is a different
measure from ad count. But it does mean **"more products" is not on its own the
lever**, and 600–700 should be treated as a target to grow into rather than a
number to hit on day one.

---

## §4 The import gate — unchanged

Noted once, not laboured. The store has **zero products** and has **not run the
deliberate misrepresentation campaign**. The playbook allows **3 appeals per GMC,
then the GMC is dead**. Appealing a suspension across ~5 products is survivable;
across 600–700 it is not.

So the sequence to 600–700 is: **5 → suspension → appeal → approval → 4-week
freeze → 25/day or 50/week → 600–700.** Roughly 10–12 weeks, and it ends in the
same place.

---

## §5 Open questions I need answered

1. **Which supplier app is connected, and how do I read its catalogue?** `appInstallations` is denied to this integration, so I cannot enumerate installed apps. A `Tapstitch: Special Line` delivery profile exists but carries **no fulfillment-service location**, which is why I read sourcing as absent. Tell me the app name and I can work out the import path.
2. **Which store is this — HIVOLT, or a new domain?** See §6. This one matters most.
3. **Target market.** All analysis above assumes **US**. `smukoslo.no` is a live argument for a smaller market instead.

---

## §6 🔴 A collision worth naming before anything is imported

HIVOLT is live, and its published position is explicit, on the homepage, the
About page, the Help Center and the Terms:

> *"Every figure we publish carries its source. Where we don't have one, we say so
> instead of guessing."*
> *"We publish the details that usually stay hidden — fabric weight, composition,
> how a seam is finished."*

**A 600–700 SKU general dropship catalogue cannot meet that standard.** No
supplier of that breadth supplies verified fabric weight, composition and garment
measurements per SKU, and six sessions of this rebuild have been spent removing
exactly the invented figures that fill that gap.

Two coherent options. Both are fine; the mix is not:

| | |
|---|---|
| **A. Keep the position, narrow the catalogue** | HIVOLT stays a spec-published store. Fewer SKUs, real supplier documents. The published standard survives. |
| **B. Keep the catalogue, change the store** | The general 600–700 dropship store runs on a **separate domain and a separate GMC**, and HIVOLT's promises do not follow it. The playbook recommends separate domains and companies anyway. |

Running a 700-SKU general catalogue **on hivolt-usa.com** would put the store's own
About page in contradiction with its product pages — which is the definition of
misrepresentation, and the exact suspension reason this account is most exposed to.

---

## §7 The course's manual method (competitor-research module)

Captured from the module as streamed 2026-08-27. The course does this by hand
with three tools; §1's TrendTrack pass assembles the same fields in one query.
The value here is the **screening bars**, which the course states only by
demonstration.

**Why competitors matter:** product discovery. When a seasonal window opens
(their example: needing leather jackets), check what competitors already launched
before researching from scratch. Match competitor markets **by season** —
Europe/US share a season, Australia is opposite. Copy from same-season markets
only.

**The stack:**

| Tool | Role | Notes |
|---|---|---|
| Browser search, on a **VPN in the target market** | Find stores (searched "letter jackets") | SERPs and Shopping ads are geo-targeted; he researches the UK from a UK NordVPN exit. Any VPN works. |
| **PPSPY** (free browser extension, account required) | Inspect a Shopify store: product count, catalogue | His demo store showed 789 products. |
| **SimilarWeb** | Traffic check on each candidate | The number that qualifies or kills a store. |

**Destination:** qualifying URLs go straight into the competitor sheet — the
same template the tracker CSV in this repo mirrors.

**Screening bars, from the live demo (each is a real store he judged):**

| Store seen | Verdict | The bar it reveals |
|---|---|---|
| 789 products, **17k visits/mo** | Skip | In a **"big five" market** (he names UK, US, Australia) 17k/month "is not much at all." The bar is market-relative — small markets can qualify lower (cf. smukoslo.no, §2). |
| ~500 products, **started in October** (~2 months old) | Skip | Recency screen: a young store with no trajectory proves nothing, whatever its catalogue size. |
| **1,300 products, steep traffic uptrend**, projected 50k+/mo | **Save to sheet** | The qualify shape: real catalogue + **rising trend** heading past ~50k in a big-five market. |

**Dropshipper identification** (how he tells a dropship competitor from retail,
worth copying *from*): lower price points than retail; **city names in store
names**; recognizable dropship products. He notes most of the UK-results
operators "are gonna be Netherlands" — NL-based stores working the UK market.

**Recording date:** stated outright while filling the sheet — **"today is the
sixth of January two thousand twenty six."** (The earlier "December" was him
reading a SimilarWeb chart month, not the date.) Recorded in winter either way:
none of its seasonal examples (letter jackets, leather jackets) transfer to late
August without re-deriving from FEED-CALENDAR.md.

**Status taxonomy and the product-count floor.** The sheet's Status column takes
**"mid player"** or **"big player"** — thresholds are yours to set, but the demo
draws them: 1,338 products (UK) = mid player; 3,300 products + 93k visitors =
big player; **260 products = "not enough," skipped**. Target **10–15
competitors, mostly mid and big players**, then repeat the whole pass per
market — UK done, then USA, Netherlands, Germany — so you hold same-season
competitors "all around the globe."

**A fourth dropshipper tell:** the stores *look alike*. Same themes, same
layouts — visual similarity across candidates is itself the signature, alongside
lower prices, city-name store names, and recognizable dropship products.

**What the list is actually for — this is the module's point.** The competitor
sheet is a **product-sourcing index**, not a watchlist. When Trends says a
category will trend (letter jackets for spring/summer), you don't research
products from scratch — you open a favorite competitor, search "letter jackets"
*on their store*, and **import the first page of results** — ahead of the trend,
"so we can catch the momentum when it's there." That is why the product-count
floor exists: a 260-product boutique can't answer a category query; a
3,300-product catalogue can. Catalogue breadth is the qualifying feature because
breadth is what you'll be searching.

⚠️ **"Import the first page" does not suspend the listing module's own rules.**
Every competitor import still runs the de-linking chain in
PRODUCT-LISTING-SOP.md: title and description rewritten from scratch, EXIF
stripped before upload, handle regenerated. A first-page bulk import that skips
the chain is a first-page bulk *fingerprint*.

**Two closing rules:**

- **Competitors are also a design reference.** Study the site itself — layout,
  features you don't see elsewhere. "He's doing well — why can I not?"
- **Cadence: monthly.** Re-run the pass every month — new products they launch,
  and new competitors entering the market. The sheet is a living document, not
  a one-time exercise.

**How the §2 tracker rows hold up against these bars:** all fifteen rows sit at
≥30k visits/month (the TrendTrack query floor), above the 17k dismissal; none
was born within the last two months (youngest: pointcarre.be, 2025-04). The one
screen my ranking did not apply is his **uptrend** test — I ranked by ad-launch
velocity, and reported `growth30d` was 1–3% across the sample (§1, caveat 1).
If a row must be cut to match the course exactly, cut on flat growth, not on
traffic.

### §7.1 The top-up pass, 2026-08-27 — filters set the course's way

Re-queried TrendTrack with the module's bars as literal filters: category
`Women's Clothing`, products ≥1,000, visits ≥30k (US) / ≥20k (GB), **sorted by
30-day traffic growth** for the uptrend screen, then post-filtered to shops with
live Google ads and ≥40% target-market audience share. Three corrections to
earlier caveats:

1. **The growth sort works.** §1 caveat 2 reported the traffic-growth filter not
   constraining results; sorting by `growth30d` this time returned a real 5–79%
   spread for the US. The earlier flatline was a property of ranking by
   ad-launch velocity, not of the data.
2. **"Most is gonna be Netherlands" is confirmed in the data.** The US uptrend
   page alone carries three NL-registered shops trading under anglo family
   names on ≥90% US traffic (susan-michael.com, theharringtonsisters.com,
   thewilsonfamilypalmbeach.com); the GB pass adds lunelondon.co.uk — NL HQ,
   London in the name, 25,000 products. The course's dropshipper tells (family
   or city name, young store, off-market HQ) select these rows mechanically.
3. **Recency needs the traffic exception.** The course skipped a 2-month-old
   store *with no traffic*. averylanebrighton.com is 2 months old with 138k
   monthly GB visits and rising — a young store already carrying traffic is the
   most informative row on the sheet, not a skip.

Output: `competitor-tracker.csv` (US, 15 players + WATCH + OUTLIER) and
`competitor-tracker-uk.csv` (12 rows) — both in the sheet's column layout,
tiers per the module's taxonomy. Figures are TrendTrack indexed values read
2026-08-27; `shopAds` (platform split) was unindexed for most uptrend rows, so
Google activity is evidenced by `liveAds` counts instead.
