# PRODUCTION-RELEASE-GATE.md — MASTER r2 certification, 2026-08-28

Verdict: **READY FOR PRODUCTION CUTOVER** (theme level). Every gate below
was evaluated this session against fresh Shopify read-backs and re-executed
local suites. LOCAL = verified on rendered local pixels / executed source;
REMOTE walk was impossible from this environment (all storefront/CDN egress
denied at CONNECT) and is honestly marked. External catalog/marketing items
are tracked separately and do not gate the theme.

| GATE | RESULT | EVIDENCE | BLOCKING |
|---|---|---|---|
| Theme role safety | PASS | Exactly one MAIN (`158753849576`); r2 (`158874960104`) UNPUBLISHED on every read incl. immediately before the one repair write | no |
| Repo/theme integrity | PASS | Full file diff r2 vs MAIN: 8 modified + 7 added, 0 missing, ~370 unchanged; all 13 known fixes checksum-verified (swaps `1ec45ae6`, JSON-LD `62d5df5f`, sticky-ATC `407db688`, About/Contact/Careers, favicon, nav, 7 templates); r2 updatedAt unmoved since last verified write | no |
| Homepage zero-catalog | PASS | 23/23 products DRAFT, 0 published (fresh counts). Source-verified: circles/value-strip/edit-cards collapse fully (`qualified > 0` wrappers); featured-collection disabled; tile sections render `<a>` only when link non-blank (no empty hrefs); hero CTAs gated on label+link; no product counts, no fake sale, no fake reviews anywhere | no |
| Navigation | PASS (after repair) | Every visible r2 link resolves to a published destination (menus + pages + policies read back). Repair: removed "New in"/"Knitwear" from `master-storefront-nav` (empty collections at cutover, §7); read-back verified; MAIN unaffected (uses `fashion-main`, checksum-proven) | repaired |
| PDP | PASS (LOCAL) | 68/68 behavioral checks re-run green at 320/375/390/430/1440 on the real section code; blank-safe accordions; single form | no |
| Mobile | PASS (LOCAL) | 320–430 suites green: no overflow, 2-col grids, safe-area, ≥44px targets | no |
| Sticky ATC | PASS (LOCAL) | Fling-skip fix present on r2 (`407db688`) and verified: appear/hide, price/variant/sold-out sync, single submit, no CLS | no |
| Cart | PASS (config+native) | Drawer configured, truthful shipping line, no fake threshold meter; runtime walk = remote residue | no |
| Search | PASS (config+native) | Predictive on, products-first with price; zero-catalog query degrades to pages/articles gracefully (native) | no |
| Quick shop | PASS (config+native) | Enabled ("Quick Add"); no duplicate Product JSON-LD (single source in fashion-pdp-info) | no |
| Collection | PASS (LOCAL fixtures) | 48/100-card suites green; filters/sort native Search & Discovery; no crawl trap added | no |
| Pages | PASS | Every published page has a real template on r2; About premium rebuild; Contact rebuilt; all templates JSON-valid and Shopify-accepted | no |
| Policies / trust | PASS (theme) — 4 owner flags | All 5 policies exist; every displayed claim (free US shipping, 60-day free returns, no restocking fee, payment methods) matches ratified policy/config. Flags live on MAIN too, unchanged by r2: FAQ vs track-order delivery windows; US-only copy vs worldwide zones; "Men's Polos" size-guide title; empty collections on the unlinked /collections route | no (owner content items) |
| Contact data | PASS | Displayed email/phone/address match shop billing record exactly; no socials shown (none exist) | no |
| SEO | PASS (LOCAL) | One title/canonical/meta-description path in layout; OG/Twitter present; robots/sitemap native; variant URLs canonicalize to bare product URL | no |
| Schema | PASS (LOCAL) | 17/17 render cases valid JSON; Org(+logo)/WebSite/Breadcrumb/CollectionPage/Article/Product-AggregateOffer/FAQPage-from-visible-blocks; zero fabricated AggregateRating/Review/GTIN/MPN/shippingDetails/priceValidUntil | no |
| Performance | PASS (LOCAL evidence) | 0 JS errors all suites; width/height+srcset on media; eager+fetchpriority LCP hero, lazy below fold; DOM 589 @48 cards; REMOTE LIGHTHOUSE PENDING | no |
| Accessibility | PASS (LOCAL) | axe: 0 violations at every severity, 3 harnesses × 2 widths, re-run this session; keyboard/focus/reduced-motion/44px manual checks | no |
| Images | PASS | index.json checksum `1ec45ae6` = owner-approved 12-image set with 14→24 and 17→A9 swaps; no rejected image referenced. About hero reuses the master-hero pair: technically QA'd, owner approval pending — low risk (on-brand, same shoot), swap/removal is a 1-minute editor action if declined | no (flagged) |
| Demo content | PASS | Sweep over all r2 custom/changed sources: zero demo copy, zero fake stats, zero VELORA/Fashion Nova/golf strings customer-visible; fabricated careers jobs REMOVED on r2 (still live on MAIN today); unused demo-era templates unreachable (no resource assigns their suffix, fresh-verified) | no |
| Rollback | PASS | Publishing r2 auto-unpublishes `158753849576`, which persists in the library (store's own 08-21/08-28 publish history proves retention; 4 themes, well under limit); rollback = one Publish click on it | no |

## Scores

- THEME CUTOVER READINESS: **93/100** (−4 remote rendered walk not
  executable from this environment; −2 owner-pending About imagery; −1
  native-widget runtime residue)
- THEME ENGINEERING 95 · VISUAL TECHNICAL 91 · OWNER VISUAL APPROVAL 80 ·
  SEO 95 · CRO 90 · MOBILE 95 · ACCESSIBILITY PASS (per scorecard V5,
  re-validated by this session's suite re-runs)
- CATALOG PRODUCTION: 20/100 (23 DRAFT products now — import pipeline
  active; 0 ACTIVE, supplier/size data absent)
- COMMERCE LAUNCH READINESS: **25/100** — the theme can go live, but the
  store must NOT take paid traffic: 0 purchasable products, analytics NOT
  CONFIGURED, policy-copy contradictions to reconcile, GMC not in play.

## Shopify writes this session

Exactly one, release-blocking-repair scope: menu `master-storefront-nav`
(`254991532264`) — removed the two links to collections that render empty
at cutover; independent read-back verified; MAIN provably unaffected.
No theme file was modified; both theme updatedAt values are unchanged.

---

## CUTOVER EXECUTION RECORD — 2026-08-28 ~21:15 UTC (appended; certification above unchanged)

- CUTOVER EXECUTED: **NO — publish blocked by connector policy.** The owner
  explicitly authorized publication of MASTER r2; pre-flight and drift
  detection PASSED (exactly one MAIN; r2 UNPUBLISHED, updatedAt unmoved at
  16:23:54; all 8 critical certified checksums identical; nav repair
  intact). The validated `themePublish` mutation was then refused by the
  Shopify MCP server's safety policy: "Publishing a theme is blocked —
  making a theme live must be done manually in Shopify admin." This block
  is categorical and session-independent; it was not worked around.
- POST-CUTOVER RESULT: N/A — roles re-verified unchanged after the refusal
  (MAIN still `158753849576`, r2 still UNPUBLISHED). Production untouched.
- ROLLBACK STATUS: not needed; ROLLBACK_THEME recorded as `158753849576`
  ("GENERAL STORE — IMPULSE MASTER CANDIDATE", updatedAt 2026-08-28T15:41:08Z).
- REMOTE CHECK STATUS: storefront/CDN egress still denied —
  REMOTE PRODUCTION VISUAL WALK PENDING (owner runs the plan's 5/30-minute
  checks after publishing).
- Catalog movement since certification (external, does not affect theme
  gates): 819 products total, 344 ACTIVE, **0 published to the Online
  Store channel** (spot-verified `publishedAt: null`) — storefront still
  shows zero products, so the certified zero-catalog posture and the nav
  repair remain exactly correct at publish time.
- THE ONE HUMAN ACTION: Shopify admin → Online Store → Themes →
  "GENERAL STORE — MASTER r2 (approved image swaps)" → Publish.
  Then follow docs/PRODUCTION-CUTOVER-PLAN.md steps 5–15.

---

## GATE CLOSED — 2026-08-31 (appended; certification record above is historical)

- The certified theme **MASTER r2 (`158874960104`) was deleted from the
  store between 18:58Z and 20:29Z on 2026-08-31**, together with the
  recorded rollback theme `158753849576` and "Horizon" `158882693352`.
  Deletion confirmed by direct GID lookups returning "Theme does not
  exist" on two independent reads.
- The verdict above therefore refers to an artifact that no longer exists.
  **This cutover can never be executed.** The owner adopted a different
  live theme line ("HIVOLT — Nova Rebuild + Meta domain verification",
  `158911561960`, MAIN since 2026-08-30 09:36Z) built by parallel
  sessions, and the r2/rollback pair was removed in what reads as a
  deliberate library cleanup.
- The post-cutover verification watcher was retired at this point; the
  ONE HUMAN ACTION named in the execution record is void. Current live
  state is tracked in `docs/HIVOLT-CURRENT-STATE.md` (re-query before
  trusting it). The r2 sources and QA evidence remain in this repository's
  history; any revival would be a new theme with a new ID requiring
  re-certification of live state.
