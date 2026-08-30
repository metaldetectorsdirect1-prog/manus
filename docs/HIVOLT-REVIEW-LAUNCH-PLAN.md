# HIVOLT-REVIEW-LAUNCH-PLAN.md — 2026-08-28

State: **Judge.me is installed** (its metafields exist on all 4 products:
badge, widget, review_widget_data) with **0 reviews, 0 questions**. No
review is ever fabricated or AI-generated; no seed reviews.

## Zero-review launch behavior — recommendation

Showing "No reviews" on every card and PDP at launch **hurts** trust more
than absence helps: it broadcasts "nobody has bought here." Recommended
honest behavior:

- **PLP star badges: hidden until a product has ≥1 review.** (Judge.me
  setting "hide badge when no reviews", or theme-side gate on
  `product.metafields.judgeme.review_widget_data.number_of_reviews > 0`.)
- **PDP star row near title: same gate.**
- **PDP full review widget: keep, below the details module** — Judge.me's
  zero-state there reads as an invitation ("Be the first to write a
  review"), which is honest and acceptable at the bottom of the page, not
  at the decision point.

## Placement plan (theme-side, dev workbench; needs Decision D)

| Surface | Placement | Mechanism |
|---|---|---|
| PDP rating summary | under product title, gated ≥1 review | Judge.me **app block** in the main product section (Impulse supports `@app` blocks — verified) |
| PDP full widget | after `fashion-pdp-info`, before recommendations | app block / app embed |
| PLP card badge | under price, gated ≥1 review | Judge.me badge snippet or metafield gate |
| Review photo gallery | later, only when customer photos exist | Judge.me gallery widget |

Configuration is prepared but **not applied** — adding the app block
changes the PDP; bundled with Decision D and the next theme pass.

## Legitimate acquisition sequence (post-purchase, provider-native)

1. Judge.me review request email at **delivery + 7 days** (knitwear needs a
   wear or two) — automatic, order-verified, so every review is a verified
   purchaser.
2. One reminder at delivery + 21 days; none after.
3. Photo/video encouraged in the same email (Judge.me native) — no
   incentives that require positive sentiment; if any incentive is ever
   used it applies to *any* review and is disclosed.
4. Negative reviews stay published; support responds via Judge.me reply.
5. AggregateRating schema activates only when genuine review data exists
   (currently: none emitted anywhere — verified this session).

Prerequisite chain: products published → orders exist → deliveries →
first requests. Nothing to send before commerce activates.
