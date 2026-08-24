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
