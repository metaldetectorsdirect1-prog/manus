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
| 0.1 | **Domain: DECIDED — Option A, this store, hivolt-usa.com.** Owner instructed repeatedly on 2026-08-27 to build, stock, and redesign THIS store ("fix the store and add products and run google ads"). Consequence accepted with it: the published spec-first positioning (About/homepage/Terms promises) comes down as part of the design rebuild — the two cannot coexist without creating the exact misrepresentation GMC punishes. Fresh-domain recommendation stays on record as the road not taken. | ✅ OPTION A |
| 0.2 | **RESOLVED 2026-08-27: store linked** (AutoDS store id `5685625` → f36zps-yd.myshopify.com, account 5658972). Historical note — the link was missing for weeks and explained the empty catalogue:  Connector live 2026-08-27; authoritative reads show the AutoDS account (`metaldetectorsdirect1@gmail.com`, id 5658972, created 2026-07-14) has **zero stores attached** (`list_stores_api: []`, `has_added_store: false`) — the "AutoDS prod-bmvgnutb" fulfillment service on Shopify belongs to an installation never linked to this account. **This is why the store has no products.** Smallest action: AutoDS → Settings → Stores → Add Store → Shopify → approve OAuth for the store. Research API (`search_products`) currently `upstream_unreachable` — retry after the store link/onboarding completes. | ✅ LINKED |
| 0.3 | **GMC `5838274874`**: owner confirms 2026-08-27 the merchant account is **verified**. Verification (business identity, website claim) is not misrepresentation clearance — a verified GMC with zero products has not yet faced the misrep review that Phase 4 deliberately triggers, so the 5-product gauntlet still applies. No suspension reported → assume **3/3 appeals available**. Feed owner: **Simprosys — settled by the skill's master timeline** ("Simprosys, not the Google & YouTube app"); disable the Google & YouTube channel's feed sync before any product flows. | 🟢 VERIFIED |
| ⚠️ | **Sequence deviation, named:** the timeline requires the store finished **before** the GMC exists; ours exists against an unfinished store. Not reversible — consequence: every Phase-0/2 store item below completes **before the first feed sync**, and nothing changes during review ("every edit is a tracked feed change"). | RECORDED |
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
- 🟡 **Design rebuild** sequenced after the first import lands: nav + collection
  structure for a fashion catalogue, homepage converted from spec-first
  positioning — built on an **unpublished theme** (MAIN-theme writes are
  connector-blocked; owner publishes when ready). Doing it before products
  exist would be styling empty shelves. Committing this design on
  hivolt-usa.com is the Option A choice (0.1).
- 🟡 **Google Ads access**: no session tooling reaches Google Ads yet — Windsor
  holds only the old Meta account. Owner authorizes Google Ads into Windsor:
  https://onboard.windsor.ai/connect?connector=google_ads&next=/google_ads/authorize
  Then this session can create/manage campaigns (PMax at $5/day per Phase 4) —
  though the playbook still hands ads to a media buyer at ~500 spend.

## Phase 3 — First import — ✅ 4/5 DRAFTS LIVE ON SHOPIFY (2026-08-27; see PRODUCT-RESEARCH §4.3.1; 5th = owner imports private-supplier item 10282354278688 in AutoDS UI)

**5 products, ONE category — knitwear (window open now, FEED-CALENDAR §2) — not 600.**
Titles: formula per TITLE-FORMULA.md, US pool names, generated against the
scored list. Every listing passes `check-product-listing.py --batch`. Prices
end .95. Vendor = store name. No supplier CDN images, EXIF stripped, handles
regenerated. Products accumulate as DRAFTS, launch flips them ACTIVE in one
aliased mutation (SOP launch mechanics). **No product is created from invented
data — supplier images/specs come from the supplier catalogue (0.2) or not at
all** (§1.2 honesty rule; PRODUCT-RESEARCH §4 carries the candidate titles).

## Phase 4 — GMC gauntlet (course sequence, verbatim on file)

Pre-feed gate (timeline, Phases 0–1): policies pasted on site **and mirrored
word-for-word in GMC shipping/returns settings**; dead-link scan clean
(deadlinkchecker.com) **before** the feed syncs; trust assets up; Simprosys
owns the feed; then **change nothing during review** (3–5 business days SLA;
past 5, the scripted support push). Ads account: same Gmail, timezone is
permanent, billing country = paying entity, **one unique card** (1 domain =
1 GMC = 1 Ads = 1 card). PMax: Purchases goal, target country only.

€5/day on the 5 products → expect **misrepresentation suspension** in 5–7 days
(deliberate; if nothing after 7, add 5 more same-niche products to force it) →
**classify before appealing** — fix a *Shopping ads* suspension, ignore a
free-listings-only one (fixing it can cause the real one later) →
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
