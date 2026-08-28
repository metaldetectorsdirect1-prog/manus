# GENERAL-STORE-DESIGN-SCORECARD.md — V2, 2026-08-28 (engineering pass)

V2 separates what V1 (59.5/100, single score) blurred: **build quality**,
**owner visual approval**, and **catalog reality** are different gates owned
by different parties. No score borrows from another. Points are awarded for
what is verified, not for code existing.

## Score 1 — THEME ENGINEERING: 74/100

What the candidate theme's code verifiably does. Verification levels:
write-verified (checksum read-back on the theme) vs render-verified (real
pixels). Only the local harness surfaces are render-verified; everything
else on the theme awaits remote preview.

| Component | Max | Score | Basis |
|---|---|---|---|
| Grid/card scalability | 15 | 14 | 48-card + 24-card stress test executed: 14/14 viewport checks PASS on rendered pixels (GENERAL-STORE-STRESS-TEST.md). −1: harness reproduces the design language, not Impulse runtime |
| Homepage merchandising rhythm | 12 | 11 | FN rhythm live on candidate (checksum 9356a1f2 verified); density band proven in fixture at 24 cards; first shopping surface 571–639px on phones |
| PDP conversion architecture | 15 | 11 | Variant buttons+swatches, dynamic checkout, spec/trust module, gated reviews, Product JSON-LD; **new: mobile sticky ATC + desktop sticky panel** (write-verified, mirrors main form, no fake urgency). −4: rendered behavior unverified until remote preview |
| Sale-system truthfulness | 10 | 10 | Real bug found and fixed: `product_save_type` was `"percent"` (invalid — snippet accepts `dollar`/`percentage`) and `product_save_amount` was unset, so savings labels could never render. Now `percentage`+`true`, read-back verified. Badge math verified in snippet: `(compare_at−price)×100/compare_at`, gated on `compare_at > price`. Zero products carry compare_at today → zero sale UI, honest |
| In-grid campaign merchandising | 10 | 8 | Built: `campaign_tile` block on main-collection (limit 3), injected in collection-grid page 1 only, hidden under filters, plain crawlable anchor, empty by default. Write-verified. −2: render unverified (needs a configured tile + live products) |
| Mega menu | 8 | 7 | Impulse-native `mega_menu` header block verified in theme source; activation is pure data (menu item name match) so dead nav is impossible from the theme side; recipe documented in owner package. −1: not activated (correctly — no real collection tree yet) |
| Navigation honesty | 5 | 5 | Main menu + footer carry only real destinations (footer 404s fixed on live menu earlier, read-back verified) |
| Search & cart | 7 | 5 | Predictive search on, drawer cart, quick add; rendered QA impossible locally |
| Performance discipline | 8 | 6 | Eager LCP hero + lazy below fold + dimensioned srcsets; sticky bar adds no CLS (fixed overlay); unmeasured — owner Lighthouse required |
| SEO/structured data | 6 | 5 | Org/WebSite/Product/FAQPage/CollectionPage JSON-LD verified single-source; campaign tiles add no schema pollution; canonical/meta present |
| Accessibility | 4 | 2 | Code-level AA patterns (focus-visible, aria mirroring on sticky bar, 44px targets); no rendered keyboard walk yet |
| **TOTAL** | **100** | **74** | |

Not awarded anywhere above: anything requiring real inventory, real promos,
or rendered verification on Shopify. The 26 missing points are dominated by
render-verification debt (remote preview) — not by unbuilt features.

## Score 2 — VISUAL APPROVAL: 0/100

**0 of 31 active images are owner-approved. 0 rendered-theme reviews have
passed.** This score belongs to the owner's eyes and cannot be raised by
code. The review machinery is complete: numbered index
(HIVOLT-V3-IMAGE-REVIEW.md), in-chat gallery, and the new browser-rendered
contact sheet (docs/review/hivolt-v3-contact-sheet.html) with per-image
inspection lists and unambiguous commands. Two prior programs (V1, V2) were
rejected on real pixel defects, so this gate is demonstrably not a
formality. No image may reach a published storefront before approval.

## Score 3 — CATALOG-PRODUCTION READINESS: 15/100

What could actually be sold today. 4 products exist, all DRAFT (correct —
publishing is owner-gated), with clean hygiene: category, productType, SEO,
compare-at cleared (ratified). Everything else is data that does not exist
yet and must come from CLASS A/B sources only: composition/care/origin/
measurements 0% populated, size-chart metaobject skeleton empty, supplier
data request unanswered, 11 empty collections awaiting owner unpublish,
policies unpasted, GA4 unconnected, 0 reviews (honest zero-state), GMC gate
unpassed, AutoDS payment due 2026-08-30. None of this can be faked to raise
the score.

## Verdict

Theme Engineering 74 · Visual Approval 0 · Catalog-Production 15.
**Lowest: Visual Approval (0).** Per the iteration rule, the single next
task keys to the lowest score: **owner pixel review of the 31-image contact
sheet** — approve / reject / replace / regenerate / inpaint by number.
Engineering cannot proceed past render-verification debt without remote
preview, and catalog work is blocked on supplier data; neither is the
bottleneck. The bottleneck is the approval gate.
