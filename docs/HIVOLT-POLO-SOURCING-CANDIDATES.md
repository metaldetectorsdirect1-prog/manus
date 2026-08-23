# Polo sourcing candidates — AliExpress research, 2026-08-23

> ## Margin ranking, 2026-08-23 — the decisive finding
>
> Ranked by landed cost (item + shipping) against the 3.5× pricing floor from
> `docs/google-ads-playbook.md`, with lead time as the tiebreak.
>
> | Product | Landed | 3.5× floor | Days | Whs | vs $49 |
> |---|---:|---:|---:|:--:|---|
> | Kermei solid cotton | $9.68 | **$33.88** | 13 | CN | **CLEARS** |
> | AIOPESON solid *(= H01's own source)* | $11.58 | **$40.53** | 11 | US | **CLEARS** |
> | XuBu custom-LOGO *(min shipping)* | $13.08 | **$45.78** | 28 | CN | **CLEARS** |
> | AIOPESON V-neck striped | $15.06 | $52.71 | 13 | CN | fails |
> | AIOPESON breathable stretch | $18.38 | $64.33 | 11 | CN | fails |
> | AIOPESON henley | $19.79 | $69.27 | 14 | US | fails |
> | AIOPESON badge embroidery | $20.58 | $72.03 | 13 | CN | fails |
> | Business casual knitted | $21.01 | $73.54 | 12 | CN | fails |
> | King Billion contrast | $22.33 | $78.16 | 14 | US | fails |
> | NN man sport/golf | $23.41 | $81.94 | 14 | CN | fails |
> | XuBu custom-LOGO *(max shipping)* | $40.25 | $140.88 | 29 | CN | fails |
> | We Men's 6XL embroidery | $50.75 | $177.62 | 14 | CN | fails |
> | Crush on Retro knitted | $111.79 | $391.26 | 20 | CN | fails |
>
> **3 of 13 clear a $49 price point.** At 3.0× — the blended margin this store
> actually runs, per PR #2 — 4 clear.
>
> One of the three is the item H01 is already sourced from, so the genuinely
> new options are **two**: Kermei, and XuBu *if* its shipping can be pinned to
> the low end of its $6.85–$34.02 range.
>
> This inverts the request. The constraint on adding polos is not finding them
> — it is that at $49, almost nothing sourced this way earns its keep. The
> options are to price well above $49, or source materially cheaper than
> $14 landed.

**Read the two caveats before using this list.**

## Caveat 1 — these are NOT ranked by sales

The request was for *top selling / top ranking* polos. **That data is not
available through any surface this environment can reach**, so nothing below is
ranked by sales and it would be a fabrication to present it as such.

| What was tried | Result |
|---|---|
| `get_winning_products` (AutoDS), sorted `-orders_count`, search "polo" and "polo shirt men" | **Empty result set** both times — no polo data in the winning-products index, or the Product Finding Hub tier is not active |
| `search_products` sorted by `total_sold_count` | **HTTP 400** — not a sortable field in this catalog |
| Any sales/rating field on returned products | **Absent.** No order count, no rating, no review count, no sold-count on a single record |
| AliExpress directly | **403 at CONNECT** — network policy denial, unchanged |

So the list below is ordered by **landed cost**, which is real data the catalog
does return. Ordering it by anything sales-related is not possible today.

## Caveat 2 — the search is polluted with car parts

Searching AliExpress for "polo" returns the **Volkswagen Polo**. Of 20 results
on the AliExpress-filtered query, 7 were mirror glass, wing-mirror caps, grab
handles, turn-signal blinkers and a reversing camera. Any bulk "import all
results" would have put car parts in a clothing store.

---

## Candidates — real polo shirts only

Prices are supplier cost in USD, region US, as returned 2026-08-23. "3.5× floor"
is the minimum retail price under the pricing rule in
`docs/google-ads-playbook.md`, applied to the **max** cost.

| # | Product | Supplier | Cost | Ship | Days | 3.5× floor | Item ID |
|---|---|---|---:|---:|---:|---:|---|
| 1 | Men Summer Solid Casual Breathable Cotton Polo | Kermei Men Dropshipping | $6.93–7.69 | $1.99 | 13 | **$26.92** | `3256806213968458` |
| 2 | 8-colour Polo, **custom LOGO printing** | XuBu Customize | $6.23 | $6.85–34.02 | 27–29 | **$21.81** | `1005002637713860` |
| 3 | Men Polo Contrast Colour Streetwear | King Billion Official | $7.31–20.34 | $1.99 | 14 | **$71.19** | `1005005444494595` (US warehouse) |
| 4 | Polo man T-shirt wool sport golf | NN man | $8.28 | $12.25–15.13 | 13–14 | **$28.98** | `3256808727437235` |
| 5 | AIOPESON Cotton Polo, solid | AIOPESON Official | $10.25–11.58 | **free** | 11 | **$40.53** | `1005005785557420` (US whs) |
| 6 | AIOPESON V-Neck Striped Slim Fit | AIOPESON Official | $12.81–15.06 | **free** | 13 | **$52.71** | `1005008457301989` |
| 7 | AIOPESON Breathable Lightweight Stretch | AIOPESON Official | $17.32–18.38 | **free** | 11 | **$64.33** | `1005008383805960` |
| 8 | Business Casual Knitted Slim Fit | Top Mens Selling Jeans | $19.54–21.01 | **free** | 12 | **$73.54** | `1005011831687634` |
| 9* | Leisure Embroidery Cotton Polo, to 6XL | We Men's Store | $26.09 | $2.05–24.66 | 14 | **$91.32** | `1005003219784243` |
| 10 | Men's Polo Knitted, tennis/golf | Crush on Retro | $42.27 | $0–69.52 | 9–20 | **$147.95** | `1005003218023322` |

### Duplicates found

The catalog lists the same garment under multiple IDs. Importing the raw result
set would have created duplicate products:

- King Billion contrast polo — `1005005444494595` **and** `3256805258179843`
- AIOPESON solid cotton polo — `1005005785557420` **and** `3256805599242668`

### What the cost column implies

HIVOLT's existing polo (H01) retails at **$49.00**. Against the 3.5× floor:

- **Rows 1–5 clear it** with room. Row 1 at $7.69 landed clears at $26.92.
- **Rows 6–7 sit near it** — $52.71 and $64.33 floors against a $49 price point
  means either a higher price or a thinner margin than the playbook allows.
- **Rows 8–10 do not clear it** at any price this brand currently charges.

Rows 3, 5 ship from a **US warehouse**, which is the only way to get delivery
under two weeks. Everything else is 11–29 days from CN.

---

## Row 2 deserves separate attention

`1005002637713860` — *"8-color POLO shirt custom LOGO color matching lapel
short sleeve printing LOGO"*, XuBu Customize Store, $6.23.

This supplier **prints a customer logo onto the garment**. That is the only
route in this list to a polo that is genuinely a HIVOLT product rather than a
relabelled generic — and therefore the only route to product photography that
legitimately shows HIVOLT branding, because the branding would actually be on
the shirt being photographed.

Cost: 27–29 day lead time, and shipping runs $6.85–$34.02, which needs pinning
down before the $21.81 floor means anything.

---

## What has NOT been done

No product was created, imported or modified in Shopify. Reasons, in order of
weight:

1. **AutoDS has no store connected** — `list_stores_api` returns `[]`, so the
   AutoDS→Shopify import path has no target and `upload_products` cannot run.
2. **Every candidate inherits H01's open blockers.** H01 cannot publish today
   because its fibre composition is unverified and no garment measurements
   exist. Ten more products sourced the same way means ten more of the same
   two blockers, not one product's worth of progress.
3. **The catalogue was deliberately curated down** to 20 active products on
   2026-08-16, from 114. Adding ten polos reverses that decision, which is the
   owner's to make.
4. **Cost data is a snapshot.** Supplier prices move; these were read once, on
   2026-08-23.
