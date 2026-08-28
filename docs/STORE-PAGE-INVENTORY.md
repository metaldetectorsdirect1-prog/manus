# STORE-PAGE-INVENTORY.md — 2026-08-28 (master pass)

Candidate: `GENERAL STORE — IMPULSE MASTER CANDIDATE` (`158753849576`,
UNPUBLISHED). Legend — DESKTOP/MOBILE QA: `harness` = verified on rendered
local pixels; `native` = Impulse-native surface, engineering reviewed in
source, **rendered QA needs remote preview**; `—` = not applicable yet.
CONTENT: `owner-gated` = truthful content exists only as a draft the owner
must approve/paste (no invented facts are ever rendered).

| PAGE | STATUS | TEMPLATE | DESKTOP QA | MOBILE QA | SEO QA | CONTENT | PUBLICATION |
|---|---|---|---|---|---|---|---|
| Home | Built (reference rhythm live) | `templates/index.json` | harness (v4, 1440) | harness (v4, 390) | JSON-LD Org/WebSite verified; hero eager-LCP | Imagery preview-active, owner approval 0/28 | UNPUBLISHED candidate |
| All products / New arrivals / Best sellers / Sale | Architecture ready | collection template + circles/nav data gates | harness (48+100-card fixtures) | harness | canonical + CollectionPage JSON-LD | Blocked: 4 products DRAFT, no real collection tree | Not created (no fake collections) |
| Collection page | Built + campaign-tile block | `templates/collection.json` | harness fixtures 48/100 PASS | harness PASS | faceted nav = Shopify Search & Discovery only; no crawl traps added | Real filters need live products | UNPUBLISHED candidate |
| Product page (PDP) | Built (sticky info D, sticky ATC M, accordions via metafields, recommendations, recently viewed) | `templates/product.json` | native — needs remote preview | native — needs remote preview | Product JSON-LD real-data-only | 4 draft products; accordion data awaits supplier (CLASS A/B) | UNPUBLISHED candidate |
| Search | Predictive overlay ON (products/collections/pages/articles) | `templates/search.json` | native | native | noindex native | — | UNPUBLISHED candidate |
| Cart drawer + cart page | Native drawer + page; truthful static shipping line (NO fake threshold meter — US shipping has no minimum) | `templates/cart.json` | native | native | — | — | UNPUBLISHED candidate |
| Wishlist | NOT BUILT — no legitimate provider installed; no fake backend per directive §22 | — | — | — | — | Provider decision = owner | — |
| Gift cards | Shopify native (if enabled) | native `gift_card` | native | native | — | — | — |
| Customer account | Shopify-hosted new accounts; theme styles only what it owns | native customers/* | native | native | — | — | — |
| Contact Us | Template ready | Impulse `page.contact` | native | native | — | owner-gated (no invented phone) | Not published |
| FAQ | Template built | `templates/page.faq.json` | native | native | FAQPage schema only for visible content | owner-gated (`HIVOLT-FAQ-DRAFT.md`) | Not published |
| Shipping information | Policy page | Shopify policies | native | native | — | owner-gated; `shopPolicyUpdate` connector-blocked | Not published |
| Returns & refunds | Policy page | Shopify policies | native | native | — | owner-gated (60-day free returns ratified) | Not published |
| Order tracking | Merchant-configurable link surface only — no tracking app installed, no fake shipment data | page template | native | native | — | owner-gated | Not published |
| Size guide | Metaobject/metafield architecture from fit-system docs; NO fake measurements | page/PDP block | native | native | — | Blocked on supplier data (`HIVOLT-SIZE-DATA-ENTRY.md`) | Not published |
| Payment information | Page architecture | page template | native | native | — | owner-gated (must match real gateways) | Not published |
| About / Our story | Template ready; stats render ONLY real merchant-entered numbers | page template | native | native | — | owner-gated (`HIVOLT-ABOUT-DRAFT.md`) | Not published |
| Careers / Affiliates / Press | Architecture only — no invented openings/terms | page templates | — | — | — | owner-gated | Not created |
| Legal (Privacy/Terms/Refund/Shipping/Accessibility) | Shopify policy surfaces | native | native | native | — | owner-gated; connector-blocked paste | Not published |
| Blog / Journal index | Impulse native | `templates/blog.json` | native | native | Article schema native | No articles yet (none invented) | UNPUBLISHED candidate |
| Article page | Impulse native | native article | native | native | Article JSON-LD | — | — |
| 404 | Built | `templates/404.json` | native | native | — | — | UNPUBLISHED candidate |
| Password page | Impulse native | native | native | native | — | — | — |
| Search no-results / empty cart | Impulse native states | native | native | native | — | — | — |
| List collections | Built | `templates/list-collections.json` | native | native | — | — | UNPUBLISHED candidate |

**No page is forgotten; nothing fake is created to fill a slot.** The
recurring gate is the same three external facts: remote preview (rendered
QA of native surfaces), owner content approval (policies/pages/imagery),
and catalog reality (products/collections/supplier data).
