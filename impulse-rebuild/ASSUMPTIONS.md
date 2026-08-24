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
