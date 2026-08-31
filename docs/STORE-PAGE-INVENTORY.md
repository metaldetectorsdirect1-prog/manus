# STORE-PAGE-INVENTORY.md — 2026-08-28 (r2 hardening pass)

Live theme (MAIN): `GENERAL STORE — IMPULSE MASTER CANDIDATE` (`158753849576`)
— owner-published 2026-08-28 15:41 UTC, untouched by sessions since.
Candidate: `GENERAL STORE — MASTER r2 (approved image swaps)` (`158874960104`,
**UNPUBLISHED**) — carries everything below; owner publishes r2 to ship it.

Legend — DESKTOP/MOBILE QA: `harness` = verified on rendered local pixels
(LOCAL RENDER VERIFIED); `native` = Impulse-native surface, source-reviewed,
rendered walk needs remote preview (REMOTE SHOPIFY VERIFICATION PENDING);
`—` = not applicable. CONTENT: `real` = truthful content is live in the
template/page body; `owner-gated` = truthful draft awaits owner action.
All page/template facts below are same-day Shopify read-backs, not memory.

| PAGE | TEMPLATE | BUILT | DESKTOP QA | MOBILE QA | SEO QA | CONTENT | PUBLICATION |
|---|---|---|---|---|---|---|---|
| Home | `index.json` | Yes — locked reference rhythm; approved 12-image set wired (swaps 14→24, 17→A9 checksum-verified) | harness v4 1440 PASS | harness v4 390/320 PASS | Org+WebSite JSON-LD render-validated; hero eager+fetchpriority | real (imagery owner-approved 2026-08-28) | r2 UNPUBLISHED; same page live on MAIN minus swaps |
| Collection | `collection.json` | Yes — sidebar filters (drawer), sort, count, 4-across, description block | harness 48+100-card PASS (0 overflow, uniform rows, pagination UI) | harness 320–430 PASS, 2-col | canonical native; BreadcrumbList+CollectionPage render-validated; filters = native Search & Discovery, no added crawl trap | real (2 populated collections; 13 empty await owner) | r2 UNPUBLISHED |
| All products / New arrivals / Best sellers / Sale | collection template | Architecture ready; nav data-gated | harness fixtures | harness fixtures | as above | Blocked: 4 products DRAFT (catalog) | Not faked |
| Product (PDP) | `product.json` | Yes — gallery+zoom native, price/variants/swatches/dynamic checkout, spec accordions (blank-safe metafields), recommendations, recently viewed | native + desktop sticky panel harness PASS 1440 | **sticky ATC harness PASS 68/68 at 320/375/390/430** (appear/hide, price/variant/sold-out sync, single submit, no CLS; fling-skip bug found & fixed this pass) | Product JSON-LD (AggregateOffer, real data, no fabricated fields) render-validated; BreadcrumbList added | 4 DRAFT products; spec metafields await supplier | r2 UNPUBLISHED |
| Quick shop | settings `quick_shop_enable: true` ("Quick Add") | Impulse native modal | native | native | no duplicate Product JSON-LD (single-source in fashion-pdp-info) | — | r2 UNPUBLISHED |
| Search | `search.json` + predictive overlay (products first, then collections/pages/articles; price shown) | Yes (native) | native | native | native noindex | — | r2 UNPUBLISHED |
| Cart drawer + page | `cart.json` + drawer (`cart_type: drawer`) | Yes; recently-viewed on cart page; NO fake free-shipping meter (US shipping already free, no minimum — truthful announcement instead) | native | native | — | real | r2 UNPUBLISHED |
| Wishlist | — | **Decision B: no wishlist.** No legitimate provider installed; device-local pretence rejected; nothing faked | — | — | — | owner may pick a provider later | — |
| Gift card | `gift_card.liquid`, `product.gift-card.json` | Shopify native | native | native | — | — | — |
| Customer account | `customers/*` (7 templates) | Yes (native) | native | native | — | — | — |
| Contact Us | `page.contact.json` **rebuilt this pass**: heading, verified email + phone, Help Center / track-order / returns shortcuts, native form | Yes | native | native | BreadcrumbList | real (page published; suffix wiring to `contact` template = 1-click owner step, live-safe) | page live |
| FAQ / Help Center | `page.faq.json` — 9 real Q&As, accordion, keyboard-native | Yes | native | native | FAQPage JSON-LD generated from visible blocks only | real | page live, template wired |
| Shipping information | `page.shipping.json` **created this pass** + published page + Shopify policy | Yes | native | native | BreadcrumbList | real | page live |
| Returns & refunds | `page.returns.json` **created this pass** + published page + policy | Yes | native | native | BreadcrumbList | real | page live |
| Order tracking | `page.track-order.json` **created this pass**; page body = honest timeline + carrier-email flow; NO fake tracking states (no provider installed) | Yes | native | native | BreadcrumbList | real | page live, template wired (suffix `track-order`) |
| Size guide | `page.size-guide.json` **created this pass**; page states honestly that garment measurements are unsupplied | Yes | native | native | BreadcrumbList | real (data itself = supplier blocker) | page live |
| Payment information | default page template | Yes (published page `payment-policy`) | native | native | BreadcrumbList | real | page live |
| About / Our Mission | `page.about.json` **rebuilt this pass**: hero (approved master-hero pair) + real mission body + value strip + newsletter; demo skeleton with map removed | Yes | native | native | BreadcrumbList | real (body verified honest) | page live, template wired (suffix `about`) |
| Careers | `page.careers.json` **gutted this pass** — fabricated demo jobs/benefits removed; architecture only | architecture | — | — | — | no page exists; nothing invented | Not created |
| Affiliates / Press | — | Correctly absent — no program/mentions exist; §16 forbids invention | — | — | — | — | Not created |
| Legal (Privacy/Terms/Refund/Shipping/Accessibility) | Shopify policies + published pages (`terms-of-service`, `accessibility`, `data-sharing-opt-out`) | Yes | native | native | BreadcrumbList on pages | real | live |
| Blog / Journal index | `blog.json` | Yes (native; Training Journal, **79 real articles**) | native | native | BreadcrumbList render-validated | real | live |
| Article | `article.json` + "You may also like" related posts | Yes | native | native | **Article JSON-LD added this pass** (headline, date, author, publisher; render-validated) | real | live |
| 404 | `404.json` | Yes (native) | native | native | no JSON-LD emitted (verified) | — | r2 UNPUBLISHED |
| Password | `password.json` | Yes (native) | native | native | — | — | — |
| Search no-results / empty cart / empty states | native | Yes | native | native | — | — | — |
| Collections index | `list-collections.json` | Yes (native) | native | native | no JSON-LD emitted (verified) | — | r2 UNPUBLISHED |
| Fabric index / Google verify / Materials | `page.fabric.json`, `page.google-verify.json` **created this pass** | Yes | native | native | — | real | pages live |

**Header/nav:** new store menu `master-storefront-nav` (Journal · About ×4
children · Help ×6 children — every destination a real published surface)
wired into r2's header-group only; live MAIN still reads `fashion-main`.
The "New in"/"Knitwear" collection links were removed at certification
(2026-08-28) because all 23 products are DRAFT and both collections render
empty — re-add them after product activation (see
PRODUCTION-CUTOVER-PLAN.md). Favicon (512px HV mark) wired in r2 settings.
Announcement bar: two truthful messages, sticky.

**No page is forgotten; nothing fake fills a slot.** Remaining gates are the
same three external facts: remote preview (rendered walk of native Impulse
surfaces), owner actions (publish r2, template-suffix click for contact,
populate collections), and catalog reality (activate products, supplier data).
