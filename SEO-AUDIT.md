# HIVOLT — Technical SEO Audit

Store: `hivolt-usa.com` (`f36zps-yd.myshopify.com`)
Theme: `hivolt-theme-v13-engineering-sheet` (GemPages-built, MAIN)
Scope: US-only market

---

## Baseline

| Metric | Value |
|---|---|
| Sessions (90d) | 3,140 |
| — of which organic search | **130** |
| Orders, all time | 0 |
| Active products | 98 |
| Blog articles | 500 |
| Static pages | 15 |
| URL redirects | 87 |

500 articles and 98 optimised product pages producing 130 organic sessions in
90 days is the central anomaly. The content exists; it is not being found.

---

## Fixed

### 1. Google Search Console verification was broken
`/pages/google-site-verification` had `isPublished: false`, and redirect
`/google6945ed5c46bc40d8.html` pointed at it. The verification file returned 404,
so HTML-file verification silently failed.

Without Search Console there is no sitemap submission, no index-coverage data,
and no way to know whether the 500 articles are indexed at all.

**Action taken:** page published (`publishedAt: 2026-08-05T00:46:48Z`).
**Follow-up for the owner:** re-run verification in Search Console, submit
`https://hivolt-usa.com/sitemap.xml`, then check Pages > Indexing.

### 2. Catalogue on-page SEO (earlier in engagement)
- 98/98 meta descriptions rewritten (80 were size-chart dumps exceeding 1,000 chars)
- 98/98 SEO titles standardised
- 16 keyword-hostile product titles rewritten to search intent
- 18 products retagged into the collection taxonomy (15 were in no collection)
- 3 collection meta descriptions repaired

---

## Open — requires theme edits (blocked from API; live-theme writes are denied)

### 3. No Product structured data — highest-value remaining item
`templates/product.liquid` and `snippets/gp-head.liquid` contain no
`application/ld+json`. The blog articles emit `Article` and `FAQPage` schema,
but the product pages emit nothing.

Consequences:
- No Product rich results (price / availability never shown in SERP)
- No breadcrumb rich results, despite the template rendering a breadcrumb
- Weaker eligibility for Google Shopping free listings

**Fix:** paste `theme/product-structured-data.liquid` at the bottom of
`templates/product.liquid`.

### 4. No Organization / WebSite entity
No brand entity is declared anywhere. On a new domain with no backlinks this is
a meaningful missing signal.

**Fix:** paste `theme/organization-structured-data.liquid` before `</head>` in
`layout/theme.liquid`. Fill in `sameAs` with real social profiles first.

### 5. Returns policy contradicts itself
`templates/product.liquid` states **"30-day returns, unworn"** and
**"returned within 30 days"**. The store also publishes a page titled
**"60-Day Love-It Guarantee"**, and redirect `/pages/30-day-risk-free-guarantee`
→ `/pages/60-day-love-it-guarantee` shows the policy was deliberately extended.

Every product page therefore understates the guarantee. Trust signal and
conversion issue, not just copy.

**Fix:** update both strings in `templates/product.liquid` to 60 days.

### 6. Stale anchor text in blog articles
16 product titles were rewritten during this engagement. Handles were left
unchanged, so **no links are broken and no redirects are needed** — but blog
anchor text still uses old titles in places, e.g. an article links
`/products/classic-stripe-trim-basketball-shorts` with the anchor text
"Classic Stripe Trim Basketball Shorts", now titled
"Men's Stripe Trim Basketball Shorts".

Low severity, cosmetic. Worth a pass if the articles are ever regenerated.

---

## Assessment of the 500-article blog

Sampled articles are **good**, not thin spam: direct answer up front,
real fabric specifications, comparison tables, FAQ sections with valid
`FAQPage` JSON-LD, and deliberate internal linking to products and collections.

The risk is not quality but **footprint**: 15 articles were published within an
8-minute window (~30s apart), implying all 500 landed in bulk on a
zero-authority domain. That publication pattern is what Google's scaled-content
policies look at.

Recommendation: **do not add more articles.** The bottleneck is authority and
indexation, not volume. Verify indexation in Search Console first, then invest
in links and brand signals rather than further content.

---

## Realistic expectation

SEO is a compounding channel measured in quarters. At an AOV near $55, $100,000
in revenue is roughly 1,800 orders — about 90,000–170,000 qualified sessions at
realistic conversion rates. Organic search will not deliver that on an urgent
timeline for a new domain in the activewear category.

The items above are worth doing because they are permanent foundations. They are
not a fast revenue lever, and should not be resourced as one.
