# INFORMATION-ARCHITECTURE.md

Structure only. **Nothing here is wired to a menu** — every collection holds
zero products, and attaching navigation to them manufactures E6/E8 rather than
closing them.

## The two-path tree

`Women` and `Men` sit at equal top-level weight. Structure is parallel so the
mega-menu template is one component with two data sources, not two designs.

```
HIVOLT
├── WOMEN ─────────────────────────────┐
│   ├── New In            women-new-in │
│   ├── Categories                     │  parallel
│   │   ├── Dresses       women-dresses│  structure,
│   │   ├── Tops          women-tops   │  one template
│   │   ├── Bottoms       women-bottoms│
│   │   ├── Knitwear      women-knitwear
│   │   ├── Outerwear     women-outerwear
│   │   └── Sets          women-sets
│   ├── Edits
│   │   ├── The Essentials     women-essentials
│   │   └── Workwear           women-workwear
│   └── Sale              women-sale
│
├── MEN ───────────────────────────────┘
│   ├── New In            men-new-in
│   ├── Categories
│   │   ├── Shirts        men-shirts
│   │   ├── Tops          men-tops
│   │   ├── Bottoms       men-bottoms
│   │   ├── Knitwear      men-knitwear
│   │   └── Outerwear     men-outerwear
│   ├── Edits
│   │   └── The Essentials     men-essentials
│   └── Sale              men-sale
│
├── ABOUT          (shared, after the split)
└── HELP           (shared, after the split)
    ├── Size Guide — Women   /pages/size-guide-women
    ├── Size Guide — Men     /pages/size-guide-men
    ├── Shipping & Delivery
    ├── Returns & Refunds
    ├── Track Your Order
    ├── Care Guide
    └── Contact
```

**Namespaced handles throughout.** `women-tops` / `men-tops` rather than a
shared `tops`, so a garment can never land in the wrong gender path and the
smart-collection rules stay unambiguous.

## Smart-collection rules, pre-configured

Each collection is created with rules that populate it automatically on import.
No manual curation, no collection left empty once products land.

| Collection | Rule |
|---|---|
| `women-new-in` | `tag = women` **AND** created within 30 days |
| `women-dresses` | `tag = women` **AND** `product_type = Dress` |
| `women-sale` | `tag = women` **AND** `variant_compare_at_price > variant_price` |
| `men-shirts` | `tag = men` **AND** `product_type = Shirt` |
| …and so on | same shape, `tag` + `product_type` |

The import must therefore tag every product `women` or `men` and set
`product_type`. That is the one contract between catalog import and navigation.

## The fifteen legacy collections — disposition

All fifteen currently hold zero products and describe a catalog that no longer
exists.

| Legacy handle | Maps to | Action |
|---|---|---|
| `womens-activewear` | `women-new-in` | **rename + rewrite** |
| `tops` | `women-tops` | **rename** — copy is activewear-specific, rewrite |
| `leggings` | `women-bottoms` | **rename**, broaden |
| `shorts` | `women-bottoms` | **merge** into the above |
| `dresses` | `women-dresses` | **rename**, rewrite |
| `knitwear` | `women-knitwear` | **rename**, rewrite |
| `coats-jackets` | `women-outerwear` | **rename**, rewrite |
| `outerwear-hoodies` | `women-outerwear` | **merge** |
| `sets` | `women-sets` | **rename**, rewrite |
| `loungewear` | `women-sets` | **merge** or retire |
| `denim` | `women-bottoms` | **merge** |
| `sports-bras` | — | **retire.** No equivalent in a general womenswear tree |
| `all` | keep | `/collections/all` is a real destination |
| `mens-golf-polos` | `men-shirts` | **retire the copy**, reuse the handle's traffic via redirect |
| `long-sleeve-golf-polos` | — | **retire.** Redirect to `men-shirts` |

Two retirements need URL redirects rather than deletion — `mens-golf-polos` and
`long-sleeve-golf-polos` are linked from every menu and from the blog's 501
articles. Deleting without a redirect creates E6 at scale.

## Blocked

Menu wiring, mega-menu publication, and collection-image assignment. All wait on
products. Recorded in `VERIFICATION-PARTIAL.md`.

---

# Two-path tree — specification, 2026-08-24

**Configuration and documentation only. Nothing was created.** Creating twenty
empty collections would add twenty empty surfaces to a store whose whole problem
is empty surfaces, and would tempt a future session into wiring navigation to
them. The six menus currently point only at live destinations and that state
survived this session intact.

## Naming rule

Namespaced handles, `women-*` / `men-*`. The current fifteen are unnamespaced,
which is why `/collections/damen` could ever have pointed at a men's collection
without looking wrong.

## The tree

| Path | Handle | Smart rule (pre-configured at creation) |
|---|---|---|
| Women › All | `women-all` | `TAG = womens` |
| Women › Tops | `women-tops` | `TAG = womens` AND `TAG = tops` |
| Women › Bottoms | `women-bottoms` | `TAG = womens` AND `TAG = bottoms` |
| Women › Dresses | `women-dresses` | `TAG = womens` AND `TAG = dresses` |
| Women › Knitwear | `women-knitwear` | `TAG = womens` AND `TAG = knitwear` |
| Women › Outerwear | `women-outerwear` | `TAG = womens` AND `TAG = outerwear` |
| Women › Denim | `women-denim` | `TAG = womens` AND `TAG = denim` |
| Women › Loungewear | `women-loungewear` | `TAG = womens` AND `TAG = loungewear` |
| Men › All | `men-all` | `TAG = mens` |
| Men › Tops | `men-tops` | `TAG = mens` AND `TAG = tops` |
| Men › Bottoms | `men-bottoms` | `TAG = mens` AND `TAG = bottoms` |
| Men › Knitwear | `men-knitwear` | `TAG = mens` AND `TAG = knitwear` |
| Men › Outerwear | `men-outerwear` | `TAG = mens` AND `TAG = outerwear` |
| Men › Denim | `men-denim` | `TAG = mens` AND `TAG = denim` |

**Rules are tag-based, not title-based.** The existing fifteen use
`TITLE CONTAINS`, which means a product's *name* decides its collection —
renaming "Ribbed Knit Tank Maxi Dress" moves it between collections silently.
Tags are explicit and set at import. This is the single most important change in
the tree.

Equal weight: Women and Men are siblings at the same level with the same depth
and the same child set where the category exists. No gender-picker interstitial.

## Reconciliation against the fifteen legacy collections

| Legacy | Disposition |
|---|---|
| `all` | **keep** — used by search, `/collections/all`, and the footer |
| `womens-activewear` | **redirect** → `women-all` once populated. Already tag-based (`TAG = womens`) |
| `tops` | **redirect** → `women-tops` + `men-tops` split. Currently `TITLE CONTAINS` |
| `leggings`, `shorts`, `sports-bras`, `sets` | **redirect** → `women-bottoms` / `women-tops`. Sub-category granularity below the new tree |
| `dresses` | **redirect** → `women-dresses` |
| `knitwear` | **redirect** → `women-knitwear` + `men-knitwear` |
| `coats-jackets`, `outerwear-hoodies` | **redirect** → `women-outerwear` + `men-outerwear` |
| `denim` | **redirect** → `women-denim` + `men-denim` |
| `loungewear` | **redirect** → `women-loungewear` |
| `mens-golf-polos` | **needs owner decision** — 0 redirects now point at it (cleared this session). Delete, or keep as a men's sub-collection |
| `long-sleeve-golf-polos` | **needs owner decision** — same |

**Three redirects already point into this space and must not be duplicated:**
`/collections/tops`, `/collections/womens-activewear` and
`/collections/outerwear-hoodies` are the three real-but-empty targets still
linked from 33 anchors in surviving articles. When they are redirected to the new
tree those anchors resolve. Do not create a second redirect for the same path —
see `PUBLISH-CHECKLIST.md` §1 for the collision mechanic.

## Wiring — deferred by design

Navigation is wired when collections hold products, not before. The check before
any menu edit: does every target return products? If not, it does not go in a
menu.
