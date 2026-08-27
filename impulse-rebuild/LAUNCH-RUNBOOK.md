# LAUNCH-RUNBOOK.md — the general dropshipping store, start to scale

Assembled 2026-08-27 from every course module streamed to date, the topgoogle
skill, and live store reads made today. One page; each line links to the doc
that carries the detail. Internal-only — built on paid course material.

**Live state at assembly (fresh reads, this session):** store `HIVOLT` on
`hivolt-usa.com`, Advanced plan, USD, **0 products**. Fulfillment services
installed: Manual, **AutoDS** (`autods-prod-bmvgnutb`), **ODMPOD**, Supliful;
Tapstitch delivery profile present. Compliance gate `check-product-listing.py`
self-test **24/24**.

---

## Phase 0 — Decisions (owner; everything below waits on the first two)

| # | Decision | State |
|---|---|---|
| 0.1 | **Domain**: general store on hivolt-usa.com **or** fresh domain + fresh GMC. The published HIVOLT spec-first standard cannot share a domain with a 600–700 SKU generic catalogue (GOOGLE-SHOPPING-RESEARCH §6). Recommendation on file: fresh domain. | 🔴 OPEN |
| 0.2 | **Supplier**: confirm which installed service is the China supplier — **AutoDS is the likely answer** (general-catalogue dropship automation; ODMPOD/Tapstitch are POD apparel; Supliful is supplements). **Smallest action: authorize the AutoDS connector in claude.ai → Settings → Connectors** — then this session can read its catalogue and wire the import path. | 🟡 NARROWED |
| 0.3 | **GMC `5838274874`**: current status + appeals already used. Read from the GMC UI. | 🔴 OPEN |
| ✅ | Markets: **US + UK** — both top-4 (§8); worst pair on GMC-approval difficulty and chargeback culture; trade-off recorded, accepted. | DECIDED |
| ✅ | Niche: **general women's fashion** — the course's only endorsed niche. | DECIDED |

## Phase 1 — Research (done or awaiting one owner run)

- ✅ Competitor sheets, both markets, course taxonomy: `competitor-tracker.csv` (US, 15 players) / `competitor-tracker-uk.csv` (12). Re-run **monthly**; sourcing-index stores marked. (GOOGLE-SHOPPING-RESEARCH §7)
- ✅ Keyword master list: 640 terms, `keywords/keyword-master-list.txt`, paste-ready for Keyword Planner.
- 🟡 **Owner run (~20 min): Keyword Planner + Trends pass**, US and UK sheets, per `keywords/README.md`. Fills `scored-list.csv`; unlocks the positive title gate (≥3 scored-keyword catches per title).

## Phase 2 — Store build (partly blocked on 0.1)

- ✅ Policy bodies drafted in `policies/` — owner pastes into Shopify (write_legal_policies is denied to the connector). Payment Policy page live. (GMC-READINESS)
- 🟡 Course GMC policy templates: Notion page egress-blocked here — pull locally (Browser MCP) or paste; I diff against `policies/` before anything changes.
- 🔴 14 empty collections need unpublishing (connector-blocked; owner action).
- 🔴 Owner: Instagram 25+ posts, Trustpilot, warehouse address, feed-app choice (Simprosys vs Google & YouTube — both installed; pick ONE feed owner).

## Phase 3 — First import (blocked on 0.1 + 0.2; the sequence is fixed)

**5 products, ONE category — knitwear (window open now, FEED-CALENDAR §2) — not 600.**
Titles: formula per TITLE-FORMULA.md, US pool names, generated against the
scored list. Every listing passes `check-product-listing.py --batch`. Prices
end .95. Vendor = store name. No supplier CDN images, EXIF stripped, handles
regenerated. Products accumulate as DRAFTS, launch flips them ACTIVE in one
aliased mutation (SOP launch mechanics). **No product is created from invented
data — supplier images/specs come from the supplier catalogue (0.2) or not at
all** (§1.2 honesty rule; PRODUCT-RESEARCH §4 carries the candidate titles).

## Phase 4 — GMC gauntlet (course sequence, verbatim on file)

€5/day on the 5 products → expect **misrepresentation suspension** (deliberate)
→ appeal (3 per GMC lifetime — count against 0.3) → approval →
**three concurrent clocks** (GOOGLE-ADS §3): 4-week feed freeze (no imports, no
edits) · 2–3-week campaign warm-up (revenue unreadable, judge nothing) ·
~3-week media-buyer gate. PMax + Shopping stay live at $5/day throughout;
Search campaigns later; Video/Display never (GOOGLE-ADS §1).

## Phase 5 — Scale (post-freeze)

- Imports: 25/day (fresh GMC cadence) or 50–100/week batches; weekly atomic
  drops read as retail (SOP camouflage). Mix per FEED-CALENDAR §4:
  40% permanent / 45% in-season / 15% early-next-season.
- **Switch point: 400–600 products OR first profitability, whichever first** —
  then batch weekly only, media buyer onboarded (~500 spend, ~10% of spend).
- Feed hygiene from day 30–60: the four draft triggers (zombie 90d,
  season-over, min-spend-19/max-ROAS-2, refund-rate outlier), draft-never-
  delete, draft-50-import-50. (FEED-CALENDAR §7)
- Seasonal imports 2–3 months pre-peak at the trough — §2 windows open now:
  winter coats, knitwear, boots, leather/suede jackets.
- Competitor sheets re-run monthly; category demand spikes are sourced from
  big-player competitors first (§7), always through the SOP de-linking chain.

## Standing rules that outrank everything above

No copyright/trademark products, ever (terminal). No health-adjacent products.
No fabricated reviews, scarcity, or invented specs — `[[NEEDS:]]` and stop.
Grey-area course tactics (anti-detect browsers, purchased reviews, insider
approvals) are recorded, not practiced. Every Shopify mutation runs the
CLAUDE.md sequence: fresh read → identity/role/status check → smallest write →
independent read-back → `updatedAt` moved. `userErrors: []` proves nothing.
