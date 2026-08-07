# hivolt-usa.com — full page audit

2026-08-07, against `HIVOLT v17 — LIVE` (`OnlineStoreTheme/158306992360`),
published by the store owner at 17:35 UTC.

The sandbox's egress proxy blocks both `hivolt-usa.com` and
`f36zps-yd.myshopify.com`, so this is not a crawl. It is an audit of route →
template resolution plus the underlying store data, which catches a class of
defect a crawler misses entirely: **designed templates that no page points at.**
Three were found that way.

---

## Fixed during this audit

### Three designed templates were orphaned

The theme shipped page templates that nothing on the store referenced, so they
rendered for nobody. The published pages were falling through to the generic
`page.liquid` instead.

| Page | Was | Now | Template activated |
|---|---|---|---|
| Our Mission (`about-us`) | no suffix → generic | `about` | `page.about.liquid` — 9,120 B |
| Returns & Refunds (`returns-refunds`) | no suffix → generic | `returns` | `page.returns.liquid` — 9,242 B |
| Materials & Sustainability (`materials-sustainability`) | no suffix → generic | `fabric` | **`page.fabric.liquid` — 30,414 B** |

`page.fabric.liquid` is the **largest template in the theme** — larger than the
homepage and the product page — and it was reaching zero visitors. On a store
whose entire proposition is published fabric weights, the page that explains
fabric weight was rendering as plain body text.

All three were checked before wiring: each renders `page.content` *in addition*
to its own designed sections, so activating the suffix adds design without
discarding the admin-entered body.

### A broken template suffix

`60-day-love-it-guarantee` carried the suffix `page`, which makes Shopify look
for `page.page.liquid`. That file does not exist, so it silently fell back.
Cleared to empty so it resolves to `page.liquid` deliberately rather than by
accident.

### The 210 gsm contradiction — second occurrence

The Drop 04 collection **SEO meta description** still read:

> "sweat-mapped compression in **210 gsm** quick-dry knit"

while the collection body and every product page say 220 g/m².

This is the same defect recorded as fixed in `STOREFRONT-IMAGE-AUDIT.md`. That
fix corrected the collection *body* and missed the *meta description* — which is
the copy Google actually prints in search results, so the wrong number was the
public-facing one. Now corrected, and a search across all collections confirms
no other 210 remains.

---

## Template resolution — all 17 published pages

12 of 17 now render a bespoke template, up from 8 before this audit.

| Page | Suffix | Renders |
|---|---|---|
| Our Mission | `about` | `page.about.liquid` |
| Help Center | `faq` | `page.faq.liquid` |
| Shipping & Delivery | `shipping` | `page.shipping.liquid` |
| Contact Us | `contact` | `page.contact.liquid` |
| Returns & Refunds | `returns` | `page.returns.liquid` |
| Size Guide | `size-guide` | `page.size-guide.liquid` |
| HIVOLT Circuit | `membership` | `page.membership.liquid` |
| Drop Calendar | `drops` | `page.drops.liquid` |
| Track Your Order | `track-order` | `page.track-order.liquid` |
| Materials & Sustainability | `fabric` | `page.fabric.liquid` |
| 60-Day Love-It Guarantee | — | `page.liquid` |
| Your Privacy Choices | — | `page.liquid` |
| Terms of Service | — | `page.liquid` |
| Ambassador Program | — | `page.liquid` |
| Accessibility Statement | `accessibility` | `page.liquid` (no such template) |
| Wholesale & Teams | `wholesale` | `page.liquid` (no such template) |
| Google Site Verification | `google-verify` | `page.liquid` (no such template) |

The last three carry a suffix with no matching template and fall back cleanly.
They render correctly, just without a bespoke layout. Google Site Verification
is a utility page and should stay generic.

---

## Correcting an earlier error in this engagement

An earlier note in this repository claimed the leftover pages from a previous
build were "still live and indexable". **That was wrong.** All 17 are
`isPublished: false` and return 404 on the storefront:

`about` · `ambassador` · `contact` · `halal` · `help` · `ingredients` ·
`press` · `privacy` · `quality` · `returns` · `reviews` · `share-photo` ·
`shipping` · `subscribe` · `subscription-help` · `team` · `terms`

Several name a different brand outright — "The YUBBEX Parent Crew", "Who's
Behind YUBBEX", "Halal & Certifications", "Ingredients & Science", "Managing
Your Subscription". They are invisible to customers and to search engines.
Worth deleting as housekeeping, but they are not a live defect and were
wrongly reported as one.

---

## Second pass — the customer account portal

`shop.customerAccountsV2.url` = **`https://account.focusfoxes.shop`**

The store runs `NEW_CUSTOMER_ACCOUNTS`, and the portal hosting them sits on
**focusfoxes.shop** — the same Focus Foxes brand that appears in the July
abandoned-checkout records. Every "Log in" and "Account" link, the *log in for
faster checkout* prompt Shopify shows during checkout, and the account links in
order confirmation emails all resolve to a domain with nothing to do with
HIVOLT.

A buyer part-way through checkout on `hivolt-usa.com` who watches
`focusfoxes.shop` appear in the address bar reads that as a redirect attack.
This is a live and plausible cause of 24 checkout arrivals and zero
completions.

**Not fixable from this connector** — it is Settings → Customer accounts in
admin. `loginRequiredAtCheckout` is `false`, so accounts are at least not
mandatory to buy.

## Second pass — fixed directly on the store

These were applied through the Admin API, so they leave no diff in this
repository. Recorded here instead.

1. **Three collections had no image.** `tops` (71 products), `bottoms` (45) and
   `frontpage` now carry supplier photography taken from a product inside that
   collection — the same approach used for the ten fabricated collection
   images. `all` is deliberately left without one; it is the catch-all and
   renders no hero.

2. **The Returns & Refunds page promised returns it cannot honour.** It offered
   "Canada: free on orders over $150, otherwise $12 deducted" and
   "International: customer arranges return shipping" on a store whose shipping
   policy, delivery profiles and enabled markets all agree it ships to the
   United States only. Two of the three rows described a service nobody can
   buy. Replaced with the one true line: US only, free, prepaid label.

3. **The footer About menu linked `/blogs/learn`, which has zero articles.**
   Replaced with Materials & Sustainability — which now renders through
   `page.fabric.liquid`, the largest template in the theme, and previously had
   no path to it from anywhere in the navigation.

## Still outstanding

### Blocking, and only the owner can clear them

1. **The legal policies still describe a supplement subscription business.**
   Terms of Service says "HIVOLT sells dietary supplement products"; the Refund
   Policy is about "HIVOLT Collagen Peptides", "opened containers" and
   automatic subscription billing. Shopify links the Refund Policy from the
   checkout page. Replacement text is in `LEGAL-POLICY-REWRITE.md`.
   `shopPolicyUpdate` requires the `write_legal_policies` scope, which this
   connector does not hold — the mutation was attempted and refused.

2. **No card has ever been charged.** `ordersCount` is 0. 24 sessions reached
   checkout across 40 days and none completed.

### Storefront defects, lower severity

3. **Four collections have no image**: `tops` (71 products), `bottoms` (45),
   `frontpage` (13), `all` (131). The other ten all carry supplier photography.
   `tops` and `bottoms` are not in any menu, but they are reachable and
   indexable.

4. **`/blogs/learn` is linked in the footer and holds zero articles.** The
   footer "About" menu points at it. The other blog, `news`
   ("Training Journal"), holds 500.

5. **Two active products still carry a single image** —
   `women-s-color-block-yoga-tank-top` and
   `womens-ruched-halter-neck-sports-bra`. Both are missing the alternate view
   the supplier import provided for everything else.

6. **The Returns & Refunds page offers Canada and international returns** —
   "Canada: free on orders over $150, otherwise $12 deducted" and
   "International: customer arranges return shipping" — on a store that ships
   to the United States only. Both the shipping policy and the delivery
   profiles agree it is US-only. Those two table rows describe a service that
   cannot be purchased.

### Verified healthy

- Theme: `processingFailed: false`, 32 files intact, sizes match the built zip.
- No password protection — the storefront is publicly reachable.
- Every menu link resolves to a page or collection that exists and is
  published, with the single exception of the empty `learn` blog.
- All 110 active products carry `vendor`, a specific Standard Product Taxonomy
  category, SEO title and description, options named `Color` and `Size`, and
  inventory with oversell enabled.
- Collection SEO titles and descriptions are populated on all 14.
