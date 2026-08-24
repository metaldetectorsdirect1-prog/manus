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
