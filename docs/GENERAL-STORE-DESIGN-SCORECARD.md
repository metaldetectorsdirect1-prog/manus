# GENERAL-STORE-DESIGN-SCORECARD.md — 2026-08-28

Scored honestly against the directive's rubric. Points are not awarded for
code existing — only for what a shopper would experience on the candidate
today. The dominant deductions come from one fact: **the catalog is 4 DRAFT
products**, so the commerce surfaces that define this store class cannot
render inventory yet, and **0 of the 31 active images are owner-approved**.

| Dimension | Max | Score | Basis |
|---|---|---|---|
| Homepage merchandising | 15 | 10 | Full FN rhythm restored (verified checksum); campaigns/tiles/strip/newsletter live; product rows disabled by draft catalog — no product abundance yet |
| Product discovery | 15 | 6 | Predictive search on, honest nav; zero live categories/products to discover |
| Collection UX | 10 | 7 | Product-first template, drawer filters, 4-col grid; filters unconfigured (S&D admin UI), unproven visually |
| PDP conversion | 15 | 10 | Gallery, variant buttons + swatches, Quick Add, dynamic checkout, spec/trust module, gated reviews, Product JSON-LD; no mobile sticky ATC; spec data 0% |
| Mobile | 15 | 10 | Dedicated portrait heroes, 2-col grids, scroll-snap category strip, ≥44px targets — code-level; no rendered verification |
| CRO | 10 | 5 | Quick Add, honest -XX% math, drawer cart; no upsell/threshold modules (no real promos exist to power them) |
| Visual quality | 5 | 0 | Cannot be claimed: no pixel inspection possible; 0/31 assets approved |
| Performance | 5 | 4 | Eager LCP + lazy below-fold + dimensioned srcset everywhere; unmeasured (owner Lighthouse) |
| SEO | 5 | 4 | Canonicals/meta/JSON-LD (Org, WebSite, Product, FAQPage)/alt text; faceted-nav policy documented, not yet enforced in filter config |
| Accessibility | 3 | 2 | Code-level AA patterns + component matrix; rendered keyboard walk pending |
| Trust | 2 | 1.5 | True claims everywhere; live policy paste still pending (owner) |
| **TOTAL** | **100** | **59.5** | |

**Verdict: NEEDS MORE ITERATION — under 90.** The gap decomposes as:
~25 points locked behind catalog reality (products/collections/filters/
upsells need real inventory), ~5 behind owner approvals (visuals, policy
paste), ~10 behind genuinely buildable next iterations (mobile sticky ATC,
grid-interleaved campaign tiles, mega-menu activation at publication,
free-shipping progress bar once a threshold is real, mobile-drawer nav
polish). The buildable items are the next code pass; the rest cannot be
closed by design work and should not be faked to inflate the score.
