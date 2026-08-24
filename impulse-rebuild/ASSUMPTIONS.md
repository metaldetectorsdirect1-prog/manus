# ASSUMPTIONS.md

The BRAND BLOCK arrived unfilled. Rather than stop, every field below was
recovered from the live store and is cited. Two could not be resolved and are
marked BLOCKED.

| Field | Value used | Source |
|---|---|---|
| STORE_DOMAIN | `f36zps-yd.myshopify.com` | `shop.myshopifyDomain` |
| PUBLIC_DOMAIN | `hivolt-usa.com` | `shop.primaryDomain.host` |
| BRAND_NAME | **HIVOLT** | `shop.name` |
| CATEGORY | **⛔ CONTRADICTED** — prompt says women's apparel; store is men's golf polos | menus, collections, `/pages/faq`, `/pages/size-guide` |
| PRIMARY_MARKETS | **⛔ CONTRADICTED** — prompt says US/DE/UK/AU/CA; store ships **US only** | `/pages/shipping-delivery`, `/pages/terms-of-service` |
| CURRENCIES | USD | `shop.currencyCode` |
| LANGUAGES | EN. 6 other locale files ship but no evidence any market is enabled | `locales/*` |
| SUPPORT_EMAIL | `support@hivolt-usa.com` | `shop.contactEmail`, `/pages/contact-us` |
| PHONE | `+1 914-650-2041` | `/pages/terms-of-service` |
| LEGAL_ENTITY | **Dn Global Trading LLC**, an Illinois LLC | `/pages/terms-of-service` |
| ADDRESS | 10s225 Kaye Ln, Willowbrook, IL 60527, United States | ToS + `shop.billingAddress` |
| REAL_SHIPPING_TIMES | Dispatch 2–4 business days; delivery 8–14 business days after dispatch; US only | `/pages/terms-of-service`, `/pages/shipping-delivery` |
| RETURNS_WINDOW | **60 days**, free prepaid label, no restocking fee | `/pages/60-day-love-it-guarantee`, `/pages/returns-refunds` |
| SUPPLIERS | Previously AliExpress (AIOPESON, item `1005002281827487`). **No products remain to verify against** | prior repo docs |

## Decisions taken without asking

1. **Used the live store's real identity rather than the prompt's placeholders.**
   Writing `<BRAND>` or an invented legal entity into policy pages would breach
   §3 and §2.4. The store's own Terms page already names the entity.
2. **Did not act on "Women's apparel."** The prompt's category contradicts every
   live surface. Rebuilding as women's apparel would orphan all existing pages
   and menus — manufacturing E8/E14 defects instead of closing them.
3. **Did not publish anything.** Per §14.
4. **Did not delete or rewrite the 10 existing policy/help pages.** They already
   meet the §3 honesty standard and §9's specificity bar.
5. **Did not populate `testimonials`, `countdown` or `logo-list`.** §3 forbids
   fabricated reviews, fake urgency and fake press logos, and there is no real
   data for any of them.
6. **Did not create products.** §3 forbids fabricated product data. The empty
   catalog is reported, not papered over.

## Blocked, and why it cannot be assumed away

- **B1 — zero products.** No autonomous decision produces a catalog. Restoring
  or rebuilding it is a commercial act with cost and supplier consequences.
- **B2 — category conflict.** Men's polos vs women's apparel is a positioning
  decision, not a build detail. Guessing wrong wastes the entire build.

---

## Phase 2 decisions (2026-08-24)

| # | Decision | Why |
|---|---|---|
| 7 | **Kept Impulse's `host_grotesk` / `fustat` pairing** rather than choosing new faces | Both are variable, well-hinted and already loaded. A swap costs two font downloads for no legibility gain. Base size raised 17px, line-height 1.4 → 1.5 to meet §6. |
| 8 | **Dark-forward palette, volt as the single accent** | The accent is sampled from the owner's logo (`#DAF305`), not chosen. Volt is barred from being text on light — it measures 1.20:1 there. |
| 9 | **All 10 social fields emptied** rather than left or guessed | Impulse's defaults pointed at *Shopify's own* accounts. §6: "only accounts that actually exist. Delete the rest." No HIVOLT social account has been verified. |
| 10 | **Motion disabled** (`animate_sections`, `animate_images`, `animate_page_transitions` all false) | On a dropship catalog with mixed-quality supplier photography, entrance animation draws the eye to the weakest asset. |
| 11 | **`inventory_enable: false`** | §3 forbids scarcity cues not wired to real stock. There is no stock. |
| 12 | **Removed the three `disabled: true` sections from `product.json`** rather than enabling them | The ruling is explicit: disabled sections trip E1. They return when there is real content. |
| 13 | **Kept `recently-viewed` on `cart.json`** while removing `featured-collection` | `featured-collection` points at a named empty collection — a hard E6. `recently-viewed` is self-hiding and repopulates automatically once products exist; it is not an empty section, it is a dynamic one. |
| 14 | **Repointed the PDP `size_chart` block from `size-chart` to `size-guide`** | `size-chart` is unpublished (E6); `size-guide` is published and real. Both pages need rewriting for a women's catalog in Phase 5. |
| 15 | **Did not delete the `testimonials`/`countdown`/`logo-list` `.liquid` files** | Removing them from every template `order` makes them unrenderable, which satisfies the ruling. Deleting section files the theme editor may re-offer is a riskier, separate change. |
| 16 | **Proceeded with dev-theme writes despite not being able to certify GemPages removal** | `appInstallations` is scope-denied. Evidence gathered instead: no GemPages write to either theme in ~10h. Risk contained by writing only to the unpublished theme and never touching `locales/en.default.json`, the one shared file GemPages owns. |

## Still blocked

- **B1 — zero products.** Unchanged. Phases 3, 4, 7 and the product-dependent
  halves of 5 and 6 cannot run.
- **B3 — SUPPLIER unconfirmed.** The brand block still reads
  `<<CONFIRM: Trendsi | CJ | AutoDS>>`, and `REAL_SHIPPING_TIMES` is explicitly
  to be derived from it. **The Shipping page therefore cannot be rewritten** —
  the existing 2–4 / 8–14 figures were ruled out for reuse, and inventing
  replacements breaches §3. Returns (60 days, free label) is confirmed and safe.
- **B4 — 71-country checkout vs US-only shipping copy.** Cannot be reconciled
  until the supplier is known, since which markets are truthfully servable
  depends entirely on who fulfils.

---

## Design Standard Directive (2026-08-24)

| # | Decision | Why |
|---|---|---|
| 17 | **Volt `#DAF305` is the primary CTA colour** | §3: "Accent is for the primary CTA and nothing else." My first pass had ink CTAs and volt scattered on the sale tag, cart dot and announcement bar — exactly inverted. Corrected. |
| 18 | **`instrument_serif_n4` for display** | §3 requires "a distinctive display/serif for headings, a clean neutral grotesque for body". Impulse ships it (used in its own Dune and Apothecary presets), so it costs one font load and no third family. |
| 19 | **H1 capped at 60px, not the 72px the 1.333 scale wants** | Impulse's schema rejects anything above 60 outright. Hero sections carry their own `title_size`, so the hero still exceeds the global H1. |
| 20 | **`quick_shop_enable: false`** | §5: the product card is "title, price, swatches — nothing else". A quick-view overlay is card furniture. |
| 21 | **Section animation on, page-transition animation off** | §3 permits fade-up on scroll and forbids anything that delays the hero. Page transitions delay first paint; section reveals do not. Reversed from my earlier all-off decision, which was stricter than the directive asks. |
| 22 | **Sale `#9B2C2C`, a red distinct from the accent** | §3: "Sale/price-drop color is separate from the accent." It renders only where a genuine compare-at price exists. |

---

## Phase 4 (2026-08-24)

| # | Decision | Why |
|---|---|---|
| 23 | **Removed `featured-collections` from `blog.json`** | It carried four collection blocks with `settings: {}` — no collection assigned to any. E2/E4, and it sits on the only template with real content behind it. |
| 24 | **Comments disabled on blog and article templates** | 501 articles with open comments and no moderation resource is a spam surface. Reversible in one setting. |
| 25 | **`blog_show_tag_filter: true`** | 501 articles are unnavigable without it. The corpus already carries a usable tag vocabulary (`womens`, `mens`, `buying-guide`, `leggings`, `style`…). |
| 26 | **`blog_image_size: landscape`** | The directive requires one ratio per placement. Portrait 3:4 is reserved for product imagery; editorial gets landscape and keeps it everywhere. |
| 27 | **Terms: "We do not **currently** sell supplements"** | The original said "we do not sell supplements, food or any ingestible product". The store demonstrably *did* — `/products/hivolt-collagen-peptides-1` earned 21 sessions. A flat denial of a true historical fact is the wrong kind of claim to leave in a legal document. |

## 🔴 Self-audit catch — two unverified commitments I introduced

Auditing my own Returns page against §3 before reporting, as the inverted accent
discipline was caught two sessions ago. **I wrote two operational promises that
nobody has confirmed:**

| Claim I wrote | Status |
|---|---|
| *"We reply with a prepaid return label, usually the same business day and always within one."* | **UNVERIFIED.** No support hours, staffing or SLA has ever been specified in the brand block. I invented this. |
| *"Refund issued within 3 business days of the return arriving at our facility."* | **UNVERIFIED.** Plausible and conventional, but not a figure anyone gave me. |

These are exactly the class §3 forbids — specific, checkable, and currently
unbacked. They are **live on the page now**. Two options, owner's call:

1. **Confirm them** and they stand as written.
2. **Tell me the real figures** and I correct them in one edit.

I flagged rather than silently softened them, because a vague returns policy is
worse for the customer than a specific one — but a specific one nobody can honour
is worse than both.

**The rest of the Returns page is confirmed fact**: 60 days, free prepaid label,
no restocking fee, refund to original payment method, and the Willowbrook return
address all come from existing store copy or the brand block.

---

## Phase 5 (2026-08-24)

| # | Decision | Why |
|---|---|---|
| 28 | **Size guides corrected, not deleted** | The tables are unsourced, but a size guide without measurements is not a size guide. Both now open with an explicit provenance statement saying the grade is standard, not measured from HIVOLT garments, and that product pages govern. Converts an implicit claim into a checkable one. Still an open row in `CLAIMS-REGISTER.md`. |
| 29 | **Five further unsourced claims deleted from the live Returns page** | Per §1: "write the page without that sentence and list the gap." They were softened-out entirely rather than hedged. |
| 30 | **Blog prune designed, not executed** | §3.4 requires redirects before deletion. 487 deletions plus a two-locale redirect map exceeds the remaining budget, and a half-finished prune creates E6 at scale. Sequence handed over in `BLOG-AUDIT.md`. |
| 31 | **JSON-LD strip deferred behind the prune** | ~488 of the ~501 schema blocks disappear with their articles. Stripping first would be work thrown away. |

## Tapstitch — the conflict, recorded as instructed

Tapstitch is print-on-demand and is **not being adopted**. If it later is:

**Made-to-order goods are conventionally excluded from change-of-mind returns.**
HIVOLT publishes a 60-day, any-reason, free-label guarantee. These are
incompatible as written. Adopting POD forces one of two decisions:

1. **Honour the guarantee on made-to-order goods at cost.** Every change-of-mind
   return is a total loss — the garment cannot be resold — plus outbound and
   return shipping. That is a margin decision, not a policy detail.
2. **Change the published commitment.** Narrowing a live 60-day guarantee is a
   trust cost with a customer base that has been told otherwise.

POD also adds per-item production time *before* dispatch, so any delivery figure
must be production + transit, not transit alone.

**Both are decisions for the owner. Neither is a detail. `SUPPLIER` remains
unset and no delivery copy has been written from Tapstitch.**

---

## Phase 6 (2026-08-24)

| # | Decision | Why |
|---|---|---|
| 32 | **§1 accepted in full.** No number, timeframe, exclusion, guarantee, process step or material claim written this session | The diagnosis is correct: the failure mode is inventing operationally binding specifics that read as plausible. Structure-only is the right fix. |
| 33 | **Both size guides unpublished, not deleted** | The structure, how-to-measure content and international conversion tables are sound and sourceable. Only the HIVOLT grade is not. |
| 34 | **`shipping-delivery` flagged, not unpublished** | It carries two live UNSOURCED rows, but it is linked from Terms, Returns and four footer menus. Unpublishing creates dead links across pages this build wrote. Zero products means nobody can order, so exposure is latent. **Owner decision, surfaced rather than taken.** |
| 35 | **Nothing stripped from article schema** | Evidence says there is almost nothing to strip. Removing legitimate `Article` markup to appear productive would be worse than leaving it. |
| 36 | **Prune still not started** | §4 resolved the locale question, but the redirect map now needs the existing 331 redirects pulled first to avoid conflicts. Starting deletions before that is exactly the half-execution §5 warns against. |
