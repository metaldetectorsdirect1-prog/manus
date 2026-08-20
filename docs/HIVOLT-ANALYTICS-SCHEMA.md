# HIVOLT — Analytics Schema

## Rule zero: one abstraction

Shopify already emits standard commerce events (`page_view`, `product_viewed`,
`add_to_cart`, `begin_checkout`, `purchase`) to connected channels. **Do not
build a second competing tracking layer.** Custom events extend that surface;
they do not replace it.

## Custom events HIVOLT needs (beyond Shopify defaults)

These are the apparel-specific decisions that Shopify does not capture and that
directly inform merchandising and returns:

| Event | Why it earns its place |
|---|---|
| `size_guide_opened` | Size friction is the #1 avoidable apparel return cause |
| `size_selected` | Which sizes get chosen vs. which get returned |
| `color_selected` | Colour demand signal for reorders — cheaper than guessing |
| `product_image_interaction` | Which gallery position drives ATC |
| `bundle_viewed` / `bundle_selected` | Direct AOV attribution |
| `cross_sell_view` / `_clicked` / `_added` | Cart cross-sell yield |
| `free_shipping_threshold_view` | Threshold effectiveness |
| `country_changed` / `currency_changed` | International intent vs. conversion |
| `email_signup` | Retention capture rate by placement |
| `review_filter` | Which fit questions shoppers actually ask |

## Property set

Attach to relevant events: `product_id`, `sku`, `variant_id`, `product_name`,
`size`, `color`, `collection`, `quantity`, `unit_price`, `discount`, `bundle_id`,
`currency`, `country`, `cart_value`, `source`, `campaign`, `content`,
`landing_page`.

Never capture: email, name, address, or any PII in an analytics payload.

## Attribution integrity

UTM parameters must survive navigation (§24). Preserve `utm_source`,
`utm_medium`, `utm_campaign`, `utm_content`, `utm_term` across internal links
and into checkout, so creative-level performance stays attributable.

## Status

**Not implemented.** Specification only — implementation is gated on the
catalogue existing, since every event above fires on product surfaces that do
not currently have products.
