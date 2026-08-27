# keywords/ — the reusable category master list

`keyword-master-list.txt` — **574+ women's fashion category and subcategory
keywords**, one per line, no icons, no headers. This is the saved, reusable list
Module 7.1 says to build once and keep (its "Notion/Google Docs" step — here it
lives in the repo instead).

Every line is phrased the way a shopper searches — *flare jeans*, not *jeans*;
*cropped puffer jacket*, not *outerwear* — because Google shoppers search
specifically, and a specific high-demand/low-supply subcategory is a market gap.

## The 20-minute run (owner-side — needs a Google Ads login)

1. **Google Ads → Tools → Keyword Planner → Get search volume and forecasts.**
2. Paste the whole file (it fits; Keyword Planner takes up to ~1,000 lines).
3. Read two columns: **avg. monthly searches** and **3-month change**.
   - **10K–100K** → strong general category, keep
   - **1K–10K** → still interesting, keep
   - **100–1K** → drop, **unless** 3-month change is strongly positive (e.g. +900%) — that's a riser
4. Survivors → **trends.google.com**, country = target market, **last 5 years**:
   note the all-time-high month and all-time-low month.
5. Label each: **permanent** (flat/consistent → backbone, never drafted) or
   **seasonal** (spiky → import at trough per `FEED-CALENDAR.md`, draft after peak).
6. Export the labelled sheet back into the repo as `keywords/scored-list.csv` —
   that becomes the buying list the 700-product feed is built from.

## Sourcing note (§1.3)

This list is generated category knowledge — the ChatGPT step of the method — not
measured demand. **No line carries a search volume until step 3 gives it one.**
The playbook-named categories are all present: boyfriend jeans, cocktail dress,
letterman jacket, wedding guest dress, heeled knee-high cowboy boots.

Season skew: the list is deliberately weighted toward the **currently-open Q4
import window** (coats, knitwear, boots, party) per `FEED-CALENDAR.md` §2, with
the permanent backbone fully covered and only a thin summer set (those import
February–April).

## The scored-list template (step 6 lands here)

`scored-list.csv` columns — one row per surviving keyword:

```
keyword,country,volume_band,change_3m,ath_month,atl_month,class,import_month,draft_month
letterman jacket,GB,1K-10K,+,Nov & Apr,Jul,dual-peak,Jul & Jan,Dec & May
cocktail dress,US,10K-100K,flat,Nov,—,permanent,keep listed,never
flare jeans,US,10K-100K,flat,—,—,permanent,keep listed,never
```

Derivation rules, mechanical:

- **import_month = trough month** (all-time low on the 5-year curve) — never the peak.
- **draft_month = the month after the peak ends.**
- **dual-peak** (like letterman jackets in the UK: Nov *and* Apr highs, Jul low) → **two import windows**: at the trough for the autumn peak, and again ~Jan for the spring peak. One-peak logic would leave half the year's demand on the table.
- **permanent** = flat/consistent curve → backbone, never drafted.
- The exact volume number no longer matters — Google only shows bands. The band gets the keyword *onto* the sheet; the **curve decides everything after that.**
- **Run Trends against the target market's country, and against today's date** — a curve read for the wrong country or the recording's season gives the wrong import month.

## The market-gap test (demand high, supply thin)

The boyfriend-jeans case generalises. A gap keyword shows **high demand and low
supply**, and each half is read in a different place:

- **Demand** — the Planner band: 1K–10K or above.
- **Supply** — search the exact keyword on Google, open the **Shopping tab**, and
  look at who is actually advertising: few distinct merchants, weak or generic
  listings, big brands absent → supply is thin. Many merchants with tight
  listings → contested, you're buying your way in.
- **Curve** — "tough to read" (flat, noisy, no clean peak) is not a bad sign; it
  is the **permanent** signature. Gap + permanent = a backbone product you list
  once and never draft.

The scored sheet gets one extra optional column for this: `supply` = thin /
contested, filled from the Shopping-tab check. Thin-supply permanents are the
highest-priority imports in the whole list — they compound the longest.

## Target markets: US + UK — two sheets, not one

The research source covers general dropshipping for **USA and UK**. Both are in
the playbook's beginner set (US, UK, AU, DK — card-only markets), with its
caveat that big markets bring more traffic, more bad reviews and stricter
Google enforcement.

Operationally: **run the Trends pass once per country.** Curves genuinely
differ — letterman jackets are the proof already on file (UK shows a second
April peak; the US curve is dominated by the autumn one). So the scored sheet
carries one row per keyword **per country**, and a category can be
import-worthy in one market while marginal in the other. Planner volume should
also be pulled per-market (set location US, then UK) rather than once globally.

Structural reminder from the playbook if both markets go live: **1 domain =
1 GMC = 1 Ads account = 1 card** — a US store and a UK store are two stores,
two feeds, two calendars. One store cannot serve both markets on one GMC.

## scored-list.csv is seeded

Twelve rows exist already — the categories the course itself confirmed on
screen (bands read from the instructor's own Planner/Trends session, so
`source=course-confirmed`, **not owner-verified**). Rows marked `pending` had a
band named but no curve shown. The owner's own Planner + Trends run replaces
`unknown`/`pending` cells and appends every additional survivor from the
610-line master list. Course-confirmed rows should be spot-checked too —
recorded curves age.
