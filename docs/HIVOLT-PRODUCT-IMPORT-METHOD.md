# Adding products to Shopify — working method

**Established and proven 2026-08-23.** AutoDS is not the route; the Shopify
Admin API is, and it solves the product-image problem as a side effect.

## The method

`productCreate` via the Shopify MCP connector, passing supplier image URLs in
the `media` argument.

```graphql
mutation CreateDraft($product: ProductCreateInput!, $media: [CreateMediaInput!]) {
  productCreate(product: $product, media: $media) {
    product { id handle status mediaCount { count } }
    userErrors { field message }
  }
}
```

```json
{
  "product": { "title": "...", "vendor": "HIVOLT", "status": "DRAFT",
               "tags": ["hivolt-sourcing-candidate"], "descriptionHtml": "..." },
  "media": [{ "originalSource": "https://ae01.alicdn.com/kf/....jpg",
              "mediaContentType": "IMAGE", "alt": "..." }]
}
```

### Why the image half works when nothing else does

**Shopify's servers fetch `originalSource`, not ours.** Our egress to
`ae01.alicdn.com` and `cdn.shopify.com` is denied at CONNECT — that has blocked
every previous attempt to read product imagery, including the two H01 detail
images still unread. It does not block this, because we only ever send the URL
string; Shopify does the fetching from its own network.

Verified end-to-end: three alicdn URLs went in, three `MediaImage` records came
back `READY` at 1000×1000 and 800×800, rehosted on Shopify's CDN.

**This also answers the branded-imagery question.** These are the supplier's
real photographs of the real garment, not generated images. Fabricated product
imagery stays refused — it is the Merchant Center misrepresentation class, and
this store already removed 102 fabricated images once.

## Why AutoDS is not the route

`list_stores_api` returns `[]`. No store is connected, so `upload_products` has
no `store_ids` target. Connecting one is an owner action in the AutoDS
dashboard. Until then the AutoDS→Shopify pipeline does not exist.

AutoDS remains useful for **research** — it is the only reachable window onto
AliExpress, which is 403 at CONNECT.

## The real bottleneck is discovery, not insertion

Insertion is solved. Discovery is not, and this is the constraint that decides
how many products can responsibly be added.

| Problem | Evidence |
|---|---|
| **No sales or ranking data at all** | No order count, rating or review count on any record. Sorting by `total_sold_count` → HTTP 400. `get_winning_products` → empty for polo queries |
| **Search drifts to wrong products** | Querying "Kermei men summer solid casual breathable cotton polo" returned **Walmart linen button-down shirts** from a different supplier |
| **Search returns the wrong category entirely** | Querying "polo" on AliExpress returns the **Volkswagen Polo** — mirror glass, wing-mirror caps, grab handles, turn-signal blinkers, a reversing camera |
| **Duplicate listings** | The same garment appears under multiple `id_on_site` values |

A batch import driven by these searches would put car parts and linen shirts in
a polo collection. **Every product must be eyeballed before insertion.** That is
the reason this was not run as a bulk job.

## Safety rules for this method

1. **`status: DRAFT`, always.** Publishing is an owner decision.
2. **No inventory.** Artificial inventory is prohibited (standing prohibition 4);
   these carry `totalInventory: 0`.
3. **No invented specs.** Description carries the supplier's own words, marked
   as the supplier's, plus cost facts. No composition, measurement or fit claim
   is asserted as verified.
4. **Tag honestly**: `hivolt-sourcing-candidate`,
   `unpriced-needs-owner-review`, `unverified-specs`, and
   `margin-fails-3-5x-floor` where the cost does not clear the pricing floor.
5. **Read back independently.** `userErrors: []` proves nothing; confirm
   `status`, `mediaCount` and that every `MediaImage` reached `READY`.

## Created so far

| Product | GID | Media | Status |
|---|---|---:|---|
| AIOPESON Badge Embroidery Cotton Polo | `9605582553320` | 3 READY | DRAFT, 0 inventory |
| AIOPESON Henley Neck Cotton Polo | `9605584486632` | 3 READY | DRAFT, 0 inventory, tagged margin-fail |

Both from AIOPESON Official Store — the same supplier as the existing HIVOLT
polo, whose evidence request is already pending. One supplier relationship
covers all three.
