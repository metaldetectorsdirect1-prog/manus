# FEED-CALENDAR.md

The seasonal feed rotation for a women's general fashion store on Google
Shopping, built from the `topgoogle` Module 7.1 rules. Written 2026-08-26 —
dates below are anchored to that.

---

## §1 The rules this calendar encodes

| Rule | Value |
|---|---|
| What matters on Google | **The feed, not the website** (opposite of Meta) |
| Research unit | **Categories, never single products** — shoppers search "flare jeans", not "jeans" |
| Sweet spot | **700–800 products ≈ ~25,000 SKUs** in GMC |
| Import timing | **2–3 months before the category's peak** — Google needs ~1 month to index, then time to build spend |
| Never | import at the peak — too late, the early importer has the momentum ("first in, first served") |
| Seasonal handling | seasonal categories are **drafted after their peak**, never deleted; re-imported at the next trough |

### The SKU math nobody does

25,000 SKUs ÷ 750 products = **~33 SKUs per product**. That is roughly
**6 sizes × 5 colours**. This constrains supplier selection more than anything
else on this page: a product offered in one colour and three sizes contributes 3
SKUs — you would need 8,000 of them. **Prefer products with full size runs and
multiple colourways; check this before importing, not after.**

---

## §2 What this means TODAY (late August)

The import window that is **open right now** is for categories peaking
**October–December**. The transcript's own example — winter jackets bought in
October–November — means importing them **now**.

| Priority | Category | Peak | Status of window |
|---|---|---|---|
| 🔴 now | **Coats & winter jackets** — puffers, wool coats, parkas, quilted | Nov–Dec | **open, closing through September** |
| 🔴 now | **Knitwear** — cardigans, turtlenecks, cable knit, oversized sweaters | Nov–Jan | open |
| 🔴 now | **Boots** — knee-high, heeled, chelsea (the playbook's own worked title example) | Oct–Dec | open |
| 🔴 now | **Leather & suede jackets** — moto, cropped, faux leather, shackets | uptrend Aug → peak Oct–Dec | **late by ~4 wks but alive** — 5-month demand run, indexed by late Sep still catches Oct–Dec whole |
| 🟠 next 2–3 wks | **Cocktail / party dresses** | peaks Nov (playbook: *"keep permanently"*) | open |
| 🟠 next 2–3 wks | **Loungewear & matching sets** | rises Nov–Jan | open |
| 🟠 September | Holiday-adjacent: sequins, velvet, satin slips | Dec | opens shortly |
| ⚪ marginal | Letterman/varsity jackets | Nov | ideal entry was end of July; short runway. Contrast with leather jackets above: same trough, but leather's 5-month run keeps its window open while letterman's shorter one closes |
| ⚫ do not import | Swim, summer dresses, linen, shorts | Jun–Jul | at their trough of *demand*, but their import window is **February–April**, not now |

---

## §3 The 12-month rotation

**Method note (§1.3):** rows marked ▣ come from the playbook's own worked
examples. The rest are standard northern-hemisphere fashion seasonality, and the
peak months are my inference — **verify each in Google Trends (5-year view, US)
before acting**; the 20-minute procedure is in `PRODUCT-RESEARCH.md` §5.

| Import in | Category | Peak | Draft after |
|---|---|---|---|
| Jan ▣ | Wedding guest & wedding-adjacent (re-import) | Apr–Jun | July |
| Feb–Mar | Spring dresses, light trench coats, denim jackets | Apr–May | June |
| Feb–Apr | Swim, summer dresses, linen, skirts, sandals | Jun–Jul | August |
| May–Jun | Festival, shorts, co-ords | Jul | September |
| **End of July ▣** | **Letterman/varsity jackets** | Nov | December |
| **Aug–Sep** | **Winter coats, knitwear, boots** | **Nov–Dec** | January |
| Sep ▣ | Wedding dresses → **draft** them (trough) | — | re-import January |
| Sep–Oct | Party/holiday: sequins, velvet | Dec | January |
| Oct | Gifting-adjacent: robes, slipper boots, sets | Dec | January |
| Nov–Dec | Nothing new — ride the peak; **feed freeze discipline** | — | — |

**Permanent backbone (never drafted), per the playbook:** cocktail dresses ▣,
boyfriend jeans ▣ (named as high-demand/low-supply), plus the year-round core —
leggings, basic knit tops, everyday denim. The store is a **mix**: permanent
backbone + the rotating seasonal layer.

---

## §4 How this becomes 700–800 products

| Layer | Share | ~Products |
|---|---|---:|
| Permanent core (denim, basics, dresses, leggings) | ~40% | 300 |
| In-season layer (right now: coats, knitwear, boots, party) | ~45% | 340 |
| Next-season early imports (staggered per §3) | ~15% | 110 |

Rotation cadence once scaled, from the playbook: weekly best-seller sweep ·
monthly zombie purge (no spend/sales in 90 days → **draft, never delete**) ·
**if you draft 50, import 50** — the feed stays at size while its composition
rotates with §3.

---

## §5 Standing gates (one line each, unchanged)

1. **Sequence:** first import is still ~5 products → misrep → appeal → 4-week freeze → *then* 25/day toward 700. The calendar above is what you fill the feed *with*; it does not skip the gate.
2. **Which store:** 700 generic SKUs on hivolt-usa.com contradicts its published spec-first position → separate domain/GMC, or the position changes. Still needs your call.
3. **Supplier:** named app still unknown to me (`appInstallations` denied) — tell me what it is and I'll map the import path, including whether its products carry the size/colour depth §1 requires.

## §6 The freeze clock — resolved to 4 weeks, two different clocks explained

Module 1.2 said "wait three weeks"; the master timeline and the scaling module
both say **four weeks of touching nothing after approval** — and the scaling
module's own narration confirms four. Resolution:

- **Feed freeze = 4 weeks.** No imports, no feed edits, no site changes.
- **The "3+ weeks" figure belongs to a different clock** — the media-buyer
  handover gate ("GMC approved 3+ weeks") measures GMC age at onboarding, not
  the freeze length.
- Throughout the freeze the **PMax warm-up stays live at $5/day**. Pausing ads
  on an approved GMC is itself a suspension risk — a GMC with no spend reads as
  abandoned. The freeze freezes the *feed*, never the ads.

## §7 Draft triggers — the four reasons a product leaves the feed

All drafts, never deletions. Rebalance rule applies: draft 50 → import 50.

| Trigger | Threshold | Source |
|---|---|---|
| **Zombie** | no spend or no sales in **90 days** | Pythago / manual |
| **Season over** | category past its peak (draft winter coats when spring demand arrives — by the *curve*, not the calendar) | `scored-list.csv` draft_month |
| **Spend without return** | getting spend, bad ROAS — Pythago review: min spend 19, max ROAS 2, read 30d→14d→7d | Pythago, bi-weekly |
| **High refund rate** | product-level refund outlier | **Pythago — new lens this module** |

**Why drafting on time matters more than it looks — the spend-hogging argument:**
a mediocre product that absorbs spend isn't just underperforming, it is
**starving every other product of impressions** — and some of the starved ones
may be better than the hog. Budget is zero-sum inside the feed; a draft is not
an admission of failure, it is reallocating oxygen. This is also why
out-of-season products get drafted *promptly*: their decaying performance drags
spend away from in-season products at exactly the moment those need it.

Even with zero drafts, seasonal imports continue on the calendar — the feed
rotates forward regardless of what leaves.
