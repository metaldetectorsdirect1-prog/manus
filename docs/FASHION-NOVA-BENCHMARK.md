# Fashion Nova audit and HIVOLT gap analysis — 2026-08-30

Brief: *"audit https://www.fashionnova.com/"* and *"our goal is to make our store
look better then fashionnova.com and have best collection of all top best selling
fashion products and our landing page must be better then them and we need to
display large collection too."*

---

## 0. How this was measured

`WebFetch` returns `EGRESS_BLOCKED` for both `fashionnova.com` and
`hivolt-usa.com` — the environment is on **Trusted** network access, so neither
site is reachable from this session directly (see `docs/cloud-network-allowlist.md`).

Both sites were therefore rendered in a headless Chromium in the Higgsfield MCP
sandbox, which has its own egress, and the DOM was measured rather than
described: computed styles, element counts, grid geometry, JSON-LD, meta tags.
Catalogue figures for HIVOLT come from the Shopify Admin API in this session, not
from any document in this repo. Market figures come from the TrendTrack
connector.

**Every number below is a reading taken on 2026-08-30.** The HIVOLT catalogue is
being written concurrently by another automated process; re-measure before acting
on anything here.

---

## 1. What Fashion Nova actually is

| Measure | Value |
|---|---:|
| Monthly visits | 39,772,590 |
| Traffic growth, 30d | +5.0% |
| Products indexed | ~25,000 |
| Dresses collection alone | **7,009** |
| Live Meta ads | 161 |
| Live Google ads | 362 (663 Search, 45 Shopping, 22 YouTube) |
| TikTok followers | 4.9M, 5,931 posts, 2,024 active TikTok ads |
| Traffic mix | US 80%, CA 6.5%, GB 2.6%, AU 1.9% |
| Email cadence | ~2/week, every one a discount campaign |
| Founded | 2013 |

Recent subject lines, verbatim: *"60-80% Off? Say Less 😏"*, *"Leather Weather
Has Arrived🖤"*, *"The Fall Dress Forecast🍂"*, *"‼️NEW SALE ALERT‼️"*.

### They are not on a Shopify theme

Homepage merchandising images are served from `cdn.sanity.io`; product images
from `cdn.shopify.com`. There are **zero `shopify-section` elements** on the
page and the entire body is one React root. Fashion Nova runs a headless front
end with Sanity as the merchandising CMS and Shopify as the commerce backend.

This matters for the brief: **their homepage is not a theme you can out-configure.**
It is an application. Competing on raw feature count is the wrong axis.

---

## 2. Homepage anatomy

13,700px tall. 169 images (164 lazy-loaded, 153 with `srcset`). 57 distinct
products and 29 distinct collections linked from the homepage alone.

| # | Section | What it does |
|---:|---|---|
| 1 | Announcement | `✈️ FREE SHIPPING ON ORDERS OVER $75  ·  SHOP NEW` |
| 2 | Division nav | WOMEN · PLUS+CURVE · MEN · NEW SPORT · KIDS |
| 3 | Category sub-nav | 19 links, always visible, not hidden in a dropdown |
| 4 | Hero | Single 2880×1136 editorial image |
| 5 | THE TREND REPORT | 4 editorial tiles: *The Perfect Pair · Cotton House · Labor Day · The Office Edit* |
| 6 | SHOP BY BRAND | Brand tiles |
| 7 | SHOP BY CATEGORY | 7 tiles: Dresses, Jackets, Tops, Bottoms, Jeans, Shoes, Accessories |
| 8 | SHOP THE LATEST | **Tabbed** product rail: *For You · New In · Sale · Dresses · Jeans · Sets* |
| 9 | Footer | 4 columns — Help, Company, Quick Links, Legal |

Two structural decisions are worth stealing:

- **The category sub-nav is permanently on screen.** 19 destinations, no hover
  required. On a 25,000-product catalogue this is the single highest-leverage
  navigation choice they make.
- **The main product rail is tabbed, and the first tab is "For You".** One
  section does the work of six, and it personalises without a separate page.

### Their design system is deliberately plain

| Token | Value |
|---|---|
| Typeface | `proxima-nova` — **one family, 2,006 elements**. No display/body pair. |
| Headings | 28px / weight 800 / uppercase / letter-spacing −0.5 to −1px / `#000` |
| Body | 16px |
| Dominant surface | `#EFEFEF` (301 elements) |
| Secondary | `#FFFFFF` |
| Accent | `#BE2D2E` red — used **twice on the entire page** |

That is the whole system. No serif, no second weight axis, no colour beyond a
red that appears twice. **Fashion Nova does not win on design.** They win on
catalogue depth, price, ad volume and social reach. A store that competes with
them on typography and layout is competing where they are weakest — which is
exactly the opening the brief is asking for.

---

## 3. The product card is the real engine

Every card, everywhere on the site, carries:

```
[NEW! badge]  [40% OFF badge]
Add to Bag        ← button on the card
XS S M L XL 1X 2X 3X   ← full size run, selectable on the card
Going Out For Fun Jumpsuit
$34.99   $49.99 Comp. Value
Get $30 Off $125+ Orders With Code: SAVE30
```

Denim cards carry the numeric run instead: `0 1 3 5 7 9 11 13 15 14 Plus 16 Plus
18 Plus 20 Plus 22 Plus`.

Three things are doing work here:

1. **Size selection happens on the grid.** You never open a PDP to find out your
   size is gone. On a catalogue this size that removes an enormous number of dead
   clicks.
2. **The size run is the plus-size proof.** `1X 2X 3X` on every card is a
   stronger inclusivity signal than any banner.
3. **"Comp. Value", not "Compare at".** This is a deliberate legal hedge — it
   claims a comparable market value rather than a former selling price, which is
   what FTC pricing rules actually bite on. Note it: HIVOLT must not copy the
   strike-through pattern without either genuine sales history or the same
   careful wording.

---

## 4. Collection page

`/collections/dresses` — **7,009 products**, 73 per page.

Faceted navigation, all six facets populated:

| Facet | Values |
|---|---|
| Size | XXS, XS, S, S/M, M, L, … |
| Colors | Black, Blue, White, Pink, Brown, Red, Yellow, Green, Grey, Purple, Orange, Gold, Silver, Nude, Ivory |
| **Occasion** | Vacation, GNO/Date Night, Nightlife & Social, Professional & Office, Brunch, Daywear |
| Length | Maxi, Mini, Midi, Gown, Micro Mini |
| Style | Straight, A Line, Flowy, Mermaid, Shirt Dress, High Slit, Gown |
| Sleeve | Sleeveless, Long Sleeve, … |

**Occasion is the one to copy.** Size and colour are table stakes; occasion is
how customers actually shop for dresses, and it is a merchandising facet, not a
product attribute — it can be built from tags without new supplier data.

- H1: `WOMEN'S DRESSES` — present and specific
- Canonical strips the `?division=` parameter
- JSON-LD: `Organization`, `CollectionPage`, `BreadcrumbList`
- Meta description written per collection

---

## 5. Product page

Example: `/products/on-the-daily-tie-back-maxi-dress?color=red-combo`

Page content in order:

```
Breadcrumb: Women › Women's Dresses › On The Daily Tie Back Maxi Dress
NEW! badge
$27.99   $39.99 Comp. Value
No reviews yet                      ← honest, not faked
or 4 payments of $7.00
Get $30 Off $125+ Orders With Code: SAVE30
Color: Red Combo
Size | View Size Guide     XS S M L XL 1X 2X 3X
Add to Bag
Shipping to 97058                   ← geo-detected
Get it by TUE, SEP 1 with 1-Day Shipping
3-7 Business Days Free shipping $75+
Estimated Delivery: Thursday, Sep 3
30-day Returns: Store Credit
Product Details / Material
SEE 20+ SIMILAR STYLES
STYLE IT WITH  → 3 cross-sells with prices
YOU MIGHT ALSO LIKE → 6+ products
```

Schema: `Organization`, **`ProductGroup`** with `productGroupID`, `BreadcrumbList`.
`ProductGroup` is the correct type for a colour-varied garment and is what
Merchant Center prefers — HIVOLT emits a single `@graph` block and should be
checked against this.

Two details worth taking:

- **"No reviews yet."** A site this size states it plainly rather than
  manufacturing stars. That is the standard HIVOLT must hold to.
- **A dated delivery promise, geolocated.** *"Get it by TUE, SEP 1"* against
  HIVOLT's *"3-7 business days"* is not a close contest.

And one worth refusing: `30-day Returns: **Store Credit**`. HIVOLT already
offers 60 days with a free prepaid label and a real refund. That is a genuine,
defensible advantage and should be said louder.

---

## 6. HIVOLT measured against them, same day, same method

| | Fashion Nova | HIVOLT (live) |
|---|---:|---:|
| Homepage height | 13,700px | 6,724px |
| Homepage images | 169 | **26** |
| Distinct products on homepage | 57 | **8** |
| Collections linked from homepage | 29 | 31 |
| Nav divisions | 5 | 7 links, no persistent sub-nav |
| Category links always visible | 19 | 0 |
| Typefaces | 1 (proxima-nova) | 2 — **Jost + Instrument Serif** |
| Palette | `#EFEFEF` / white / one red | `#FFFFFF` / `#1A1A1A` / `#F7F5F2` |
| Size selection on card | yes | no |
| Faceted filters | 6 facets | availability + price only |
| Collection H1 | `WOMEN'S DRESSES` | **empty string** |
| Dresses | 7,009 | 89 live |
| Active products | ~25,000 | **925** |

**HIVOLT already has the better type system and the better palette.** Jost paired
with Instrument Serif against a warm off-white is a considered choice; Proxima
Nova on grey is not. The brief's "look better than them" is closer than the
traffic numbers suggest.

What HIVOLT does not have is *density*. Eight products on the homepage against
fifty-seven is the gap a visitor feels in the first three seconds, and it is not
a design problem — it is a merchandising problem.

---

## 7. Five defects that must be fixed before "better" is achievable

These were all found in the live store today, by measurement.

### 7.1 The live hero says WINTER, on 30 August

```
AUTUMN / WINTER
The Winter Edit
Considered knitwear, tailored outerwear and dresses made to be worn on repeat.
```

Fashion Nova's homepage today leads with *Labor Day* and *The Office Edit*.
The September Edit homepage built on 2026-08-29 fixes exactly this and is sitting
on unpublished theme `158905008360`, awaiting the owner's publish decision.

### 7.2 Clone listings survived the image sweep

The duplicate-image sweep drafted 929 products that shared a lead photo. A second
clone axis remains, invisible to that method because these listings use
*different* photos of the same garment:

**57 collision groups, 92 excess products**, after stripping the leading adjective
and the trailing colour word:

| Count | Garment | The listings |
|---:|---|---|
| 5 | Men's Linen Blend Shirt | Soft… in Khaki / Modern… in Chocolate / Effortless… in Sage / Refined… in Mustard / … |
| 5 | Women's Double-Breasted Formal Coat | Polished… in Khaki / Relaxed… in Chocolate / Modern… in Rust / Effortless… in Sage / … |
| 5 | Women's Hooded Waterproof Long Parka | Elevated / Rugged / Premium / Classic / … — *identical titles but for the adjective* |
| 4 | Men's Pocket Crew T-Shirt | Timeless / Rugged / Effortless / Elevated |

These are colour variants of one garment sold as separate products. Fashion Nova
handles this correctly: one `ProductGroup`, colour as a variant, one URL. HIVOLT
is splitting each garment into up to five competing listings, which divides its
own search authority and reads to Merchant Center as duplicate content.

Two of these are visible on the live homepage right now — *Cozy Women's Layered
Chain Necklace Set* appears twice, at **$19.95 and $29.95**.

### 7.3 Colour claims are back in 54 titles

The 2026-08-29 pass stripped fabricated colour claims from 984 titles. Today 54
active titles end in a colour again — *"…Fleece Tights in Tan"*, *"…Baggy Loose
Fit Jeans in Chocolate"*, *"…Pleated Relaxed Trousers in Olive"*. Every one was
created on **2026-08-28 or 2026-08-29**, i.e. after the fix.

The concurrent import process is re-introducing the defect faster than a one-off
sweep removes it. **This needs a guard at the import, not another sweep.**

### 7.4 918 of 925 active products carry phantom inventory

Inventory values found: 10, 680, 1000, 1999 — maximum 1,999. Only 7 products sit
at zero. This is why every collection page reads *"In stock (646) · Out of stock (0)"*.

Nothing has been received into a warehouse. Selling against invented stock is the
fastest route to a chargeback rate that Shopify acts on, and it is the single
item on this list the owner must resolve rather than a session.

### 7.5 Collection and category structure is duplicated and partly fabricated

44 collections, with at least six duplicate pairs:

| | | |
|---|---|---|
| `dresses` (173) | vs | `dresses-1` (171) |
| `knitwear` (166) | vs | `knitwear-sweaters` (154) |
| `loungewear` (78) | vs | `loungewear-sleep` (58) |
| `menswear` (92) | vs | `men` (1,172) |
| `new-arrivals` (2,251) | vs | `new-in` (1,400) |
| `all` (2,251) | vs | `best-sellers` (2,036) |

Two of these are worse than untidy:

- **`sale` contains 0 products** and promises *"Up to 80% off — shop HIVOLT
  markdowns before they're gone."* An empty sale page with an 80% claim is a live
  trust defect, and 80% exceeds the store's own 50% discount ceiling.
- **`best-sellers`** is titled "Shop All" but its SEO description reads *"our
  most-loved styles across menswear and womenswear, chosen by customers again and
  again."* **The store has zero orders.** That sentence is fabricated social proof
  on a live, indexed page and should be rewritten today.

Product types are in the same state: **164 types for 925 products**, 44 of them
roman-numeral duplicates — `Puffer Jackets II`, `Blazers II`, `Knit Dresses II`,
`Cardigans II`, `Women's Knitwear III`, `Women's Coats III`.

---

## 8. What "large collection" can honestly mean

The brief asks to *"display large collection too."* The arithmetic has to be
stated plainly.

Fashion Nova has ~25,000 products and 7,009 dresses. HIVOLT has 925 active
products built from 899 distinct photographs. **Matching them on count is not
reachable, and every attempt so far has produced clones rather than garments** —
the 1,854-product catalogue that existed yesterday was the same 899 photos
counted twice.

There are three honest ways to look large, in order of value:

1. **Collapse the 92 clone listings into colour variants.** This *reduces* the
   product count to ~833 and simultaneously makes the store look bigger, because
   each product then shows a colour swatch row instead of appearing five times as
   near-identical grid tiles. It is the single highest-value catalogue action
   available.
2. **Raise homepage density from 8 products to 40–50.** Fashion Nova reaches 57
   with a tabbed rail. HIVOLT has 925 products and shows eight of them. This costs
   nothing but section configuration and closes most of the perceived-size gap.
3. **Build occasion and edit collections from existing tags** — *Office*, *Going
   Out*, *Weekend*, *Layering*, *Under $50*. A customer counts routes into the
   catalogue, not SKUs. Fashion Nova's 19-link persistent sub-nav is doing exactly
   this work.

Growing past ~900 genuine products means sourcing genuinely distinct garments.
That is a supplier decision, not a session's work, and it should not be
simulated.

---

## 9. Recommended sequence

Ordered so that nothing is built on top of something that has to be undone.

| # | Action | Owner |
|---:|---|---|
| 1 | Zero the phantom inventory on 918 products | **Owner** |
| 2 | Rewrite the `best-sellers` "chosen by customers again and again" description; empty or unpublish `sale` | Session |
| 3 | Collapse the 57 clone groups into colour variants (−92 listings) | Session |
| 4 | Guard the import against colour-in-title, then clear the 54 residual | Session + owner |
| 5 | Merge the six duplicate collection pairs; collapse 164 product types to a real taxonomy | Session |
| 6 | Publish the September Edit homepage — replaces the WINTER hero | **Owner** decision |
| 7 | Raise homepage product density to 40–50 via a tabbed rail | Session |
| 8 | Add a persistent category sub-nav, ~15 links | Session |
| 9 | Add H1s to collection pages | Session |
| 10 | Build occasion facets from tags on Dresses first | Session |
| 11 | Size run + swatches on the product card | Session |
| 12 | `ProductGroup` schema; verify against Merchant Center | Session |

Items 1 and 6 are the owner's — production inventory and theme publication are
not this session's to decide.

---

## 10. What this audit does not establish

- **It is one reading of one page each.** Fashion Nova personalises ("For You")
  and geolocates ("Shipping to 97058", detected as Oregon); another visitor sees
  a different homepage.
- **It does not inspect Fashion Nova's mobile experience**, where ~70% of their
  traffic lands.
- **It says nothing about whether HIVOLT's 925 remaining products are accurate.**
  The image sweep removed clones; it did not verify that any surviving listing
  shows the garment it describes. In a hand-inspected sample of 22 during the
  September Edit work, 8 had title/image mismatches and 1 was counterfeit.
- **It does not price the gap.** Fashion Nova runs 362 live Google ads and 2,024
  TikTok ads. Design parity does not produce traffic parity.

---

## Appendix — fixes applied in this session, 2026-08-30

Two items from §7.5 were live false claims and were corrected immediately.
Verified by independent re-read, not by the mutation payload.

| Collection | Was | Now | `updatedAt` |
|---|---|---|---|
| `sale` (0 products) | *"Up to 80% off — shop HIVOLT markdowns before they're gone."* | *"HIVOLT markdowns. There is nothing in this edit at the moment — new reductions appear here when they are made."* | `02:49:14Z` |
| `best-sellers` (0 orders) | *"…our most-loved styles across menswear and womenswear, chosen by customers again and again."* | *"The complete HIVOLT range for women and men — dresses, coats, knitwear, denim, footwear and accessories. Free US shipping on every order and 60 days to return."* | `02:49:14Z` |

The `best-sellers` SEO title also read "Best Sellers" while the collection is
titled "Shop All" and contains the entire catalogue; it now matches.

**29 collections carried a malformed meta description** — the string ` - HIVOLT`
appended to the description body, not only the title, producing SERP snippets
that end *"…from October to spring. - HIVOLT"* under a title already reading
"Knitwear & Sweaters - HIVOLT". All 29 stripped; re-read confirms
`updatedAt 2026-08-30T02:50:05Z` on each and **zero** remaining occurrences
across all 44 collections.

`new-arrivals` also had the placeholder description *"Shop the latest drops at
HIVOLT."* on a 2,251-product collection; rewritten.

### These fixes may not hold

Collection `updatedAt` timestamps immediately before this work were spread
across `02:20`–`02:34` on the same day — the concurrent import process is
rewriting collection metadata continuously. If it regenerates descriptions from
a template, the ` - HIVOLT` suffix and the fabricated best-seller claim will
come back. **Re-read before assuming the store is clean, and fix the template
rather than the output.**
