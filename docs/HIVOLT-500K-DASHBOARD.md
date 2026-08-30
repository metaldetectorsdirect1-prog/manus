# HIVOLT — $500K Dashboard Specification

## Arithmetic

$500,000/month at various AOVs:

| AOV | Orders/month | Orders/day |
|---|---|---|
| $80 | 6,250 | 208 |
| $100 | 5,000 | 167 |
| $125 | 4,000 | 133 |
| $150 | 3,333 | 111 |

Traffic required at $125 AOV:

| CVR | Sessions/month | Sessions/day |
|---|---|---|
| 1.0% | 400,000 | 13,333 |
| 2.0% | 200,000 | 6,667 |
| 3.0% | 133,333 | 4,444 |

**Current real traffic: ~801 sessions / 14 days, of which 693 are direct
(predominantly bot/self). Real shopper sessions are a rounding error.** The
gap to $500K is a distribution problem measured in multiples of ~1,000×, not a
CRO problem measured in percentages. Any dashboard that hides this is lying.

## Metrics and their real sources

| Metric | Source | Available today |
|---|---|---|
| MTD revenue | ShopifyQL `FROM sales SHOW total_sales` | Yes (=$0) |
| Goal completion | revenue ÷ 500,000 | Yes |
| Required daily revenue | (500,000 − MTD) ÷ days remaining | Yes |
| Orders / AOV | ShopifyQL `sales` | Yes |
| Sessions / CVR | ShopifyQL `sessions` | Yes |
| Add-to-cart, checkout rate | `FROM sessions SHOW sessions_with_cart_additions, sessions_that_reached_checkout` | Yes |
| CAC | ad spend ÷ new customers | **No** — needs ad platform connection |
| MER | revenue ÷ total ad spend | **No** — needs ad spend feed |
| ROAS | platform-reported | **No** |
| Contribution margin | revenue − (COGS + ship + fees + ads) | **No** — needs `HIVOLT-UNIT-ECONOMICS.md` inputs |
| Refund / return rate | Shopify refunds | Yes, once orders exist |
| Email revenue % | Klaviyo or equivalent | **No** — not installed |
| Repeat purchase % | `FROM sales SHOW returning_customer_rate` | Yes, once orders exist |
| Inventory coverage | variant `inventoryQuantity` ÷ units-sold-per-day | Yes, once catalogue + sales exist |

Metrics marked **No** must not be rendered with placeholder numbers. Show them
as "not connected" until their source exists.
