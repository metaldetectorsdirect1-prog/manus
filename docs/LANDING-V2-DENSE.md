# Landing page v2 — density rebuild, 2026-08-30

Brief: *"we need to have exactly similar landing page like fashionnova.com"* and
*"on landing page we need to have 200 images."*

Theme: **`158911987944` — "HIVOLT — landing v2 dense (Claude, draft)"**, role
`UNPUBLISHED`. Duplicated from the live MAIN so it starts from current state.
Preview: `https://hivolt-usa.com/?preview_theme_id=158911987944`

---

## 1. Theme role changed mid-session

The MAIN theme is **not** what it was earlier today.

| | Earlier today | Now |
|---|---|---|
| MAIN | `158888526056` "Nova Rebuild (Claude)" | **`158911561960` "Nova Rebuild + Meta domain verification"** |
| `158888526056` | MAIN | now `UNPUBLISHED` |

This is precisely the failure mode `CLAUDE.md` documents: a theme's role changes
between the first read and the write. The role was re-queried immediately before
the upsert and the target confirmed `UNPUBLISHED` against a separately-queried
MAIN. Nothing was written to production.

## 2. What was built

Fashion Nova's *structure*, HIVOLT's *identity*. Their layout conventions are
functional patterns; their palette, typefaces, photography and copy are theirs
and are not reproduced. Their design system is also measurably weaker — one
typeface, `#EFEFEF` grey, one red used twice on the whole page — so copying the
skin would have been a downgrade from Jost + Instrument Serif on `#F7F5F2`.

### Section order (17)

| # | Section | Type | Images |
|---:|---|---|---:|
| 1 | The turn of the season | slideshow | 1 |
| 2 | Shop by category | image-grid | 3 |
| 3 | The September Edit | featured-collection 5×2 | 10 |
| 4 | New this week | featured-collection 5×5 | 25 |
| 5 | Outerwear, first | featured-collection 5×5 | 25 |
| 6 | Published, not claimed | rich-text | — |
| 7 | Knitwear we live in | featured-collection 5×5 | 25 |
| 8 | The dress edit | featured-collection 5×5 | 25 |
| 9 | Boots that carry the season | featured-collection 5×5 | 25 |
| 10 | Sixty days, and a real refund | rich-text | — |
| 11 | Denim and bottoms | featured-collection 5×5 | 25 |
| 12 | Tops and blouses | featured-collection 5×5 | 25 |
| 13 | Finishing pieces | featured-collection 5×5 | 25 |
| 14 | Menswear | featured-collection 5×5 | 25 |
| 15 | Made to be kept | text-and-image | 1 |
| 16 | Service promises | text-with-icons | — |
| 17 | Join the list | newsletter | — |
| | | **Total** | **240** |

**240 images against the 200 target, and against Fashion Nova's 169.** The live
homepage carries 26.

`per_row` maxes at 5 and `rows` at 5 in this theme's `featured-collection`
schema, so 25 products is the hard ceiling per rail. Ten rails was the way to
the number.

### Every rail is filled by real, in-stock-status products

Storefront-visible (active) counts checked before building, so no rail renders
placeholder tiles:

| dresses | knitwear | coats | shoes | bottoms | tops | accessories | men |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 89 | 107 | 88 | 92 | 60 | 26 | 99 | 190 |

### No AI-generated imagery

Every one of the 240 is real photography already in the catalogue. Six
atmospheric images were generated earlier in the session but **remain unverified**
— Cloudfront and the Shopify CDN are both blocked by the network policy, so they
could not be downloaded and inspected. They are not used here and will not be
until they have been looked at.

## 3. Copy changes that fix live defects

- The live hero reads **"AUTUMN / WINTER — The Winter Edit"** on 30 August. This
  one reads "SEPTEMBER — OCTOBER / The turn of the season".
- "Sixty days, and a real refund" states the genuine advantage over Fashion
  Nova's `30-day Returns: Store Credit` — which the live site currently buries.
- "Published, not claimed" states the specification policy rather than implying
  specs that do not exist.
- No discount shouting, no urgency, no fabricated social proof.

## 4. Verification

`themeFilesUpsert` returned `userErrors: []` — which on this store proves
nothing. Confirmed instead by an independent re-read of the stored file:

- 17 sections present, `order` matches `sections` exactly
- all 10 rails carry the intended collection handle and grid settings
- `updatedAt` moved to `2026-08-30T03:54:11Z`
- target theme role still `UNPUBLISHED`, MAIN untouched

One setting, `width: "wide"` on `brand-story`, was dropped by Shopify as not
valid for that section. Harmless; the local file has been synced to match.

A first attempt was rejected with *"Setting 'grid_spacing' must be a valid
number"* — it had been sent as a boolean. Corrected from the known-good
September Edit settings rather than guessed.

## 5. Not done

- **Publishing.** The owner's decision alone.
- **Persistent category sub-nav.** Fashion Nova's 19 always-visible links are
  their single best navigation decision and this theme's header does not support
  it without a section edit.
- **Size run and swatches on the grid card.** Requires the variant restructure —
  every product is currently a single SKU with no size and no colour option.
