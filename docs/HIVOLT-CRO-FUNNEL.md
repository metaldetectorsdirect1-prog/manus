# HIVOLT-CRO-FUNNEL.md — 2026-08-28

Funnel model: SESSION → CATEGORY VIEW → PRODUCT VIEW → SIZE SELECT → ADD TO
BAG → CART → CHECKOUT → PURCHASE.

**Current measurement: none** (no GA4/pixel layer — see
HIVOLT-COMMERCE-TRACKING.md). No experiment may run before baseline
instrumentation exists; every "friction point" below is an architecture
observation, not a measured finding.

## Known structural friction (pre-launch, from audit facts)

1. Catalog: 4 products, 3 single-size — size-select step collapses; PDP
   cannot demonstrate a size run except on Elena.
2. Zero reviews (Judge.me installed, empty) — social-proof step absent.
3. Policies not yet pasted — trust interruption at the decision moment.
4. No wishlist / back-in-stock — no recovery path from unavailability.
5. Supplier color names ("Jiahua Green") in variant pickers — comprehension
   friction; normalize at import.

## A/B test roadmap (post-instrumentation, post-publication; ranked I/C/E)

| Test | Impact | Confidence | Effort | Priority |
|---|---|---|---|---|
| PDP CTA visibility (sticky purchase column depth) | H | M | M | 1 |
| Shipping/returns messaging position (trust block above vs below fold) | H | M | L | 2 |
| Quick Add on collection cards on/off | M | M | L | 3 |
| Product grid density 4 vs 5 at ≥1680px | M | L | L | 4 |
| Hero strategy (editorial vs product-forward) | M | L | M | 5 |
| Size-guide entry point (picker-adjacent vs details) | M | M | L | 6 (needs charts) |
| Reviews placement (needs reviews to exist) | H | M | L | later |
| Complete-the-Look module (needs relationships) | M | L | M | later |

Prerequisites in order: pixel layer → publication → 2–4 weeks baseline →
first test. One variable at a time; PMax freeze-period rules (topgoogle)
take precedence over storefront experiments during ad ramp.
