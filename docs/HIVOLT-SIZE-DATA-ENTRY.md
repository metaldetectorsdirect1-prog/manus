# HIVOLT-SIZE-DATA-ENTRY.md — 2026-08-28

Activation map for the already-built fit system. **No values are populated;
the PDP stays blank-safe until CLASS A/B data arrives** (see
HIVOLT-SUPPLIER-DATA-REQUEST.md).

## What activates what (no theme changes needed)

| Shopper feature | Data required | Where it goes |
|---|---|---|
| FIT row on PDP | supplier fit wording | `spec.fit` |
| MODEL row | model height AND size worn (both) | `spec.model_height_cm`, `spec.model_wears_size` |
| Composition / care / origin rows | label-verified values | `spec.composition`, `spec.care`, `spec.origin` |
| SIZE GUIDE | one chart per shared block | `hivolt_size_chart` metaobject + `spec.size_chart` reference |

## Per-product entry sheet

| Product | Chart needed | Fields to fill (all CLASS A/B) |
|---|---|---|
| Elena (M/L/XL/XXL × 17 colors) | YES — 4-size chart | composition (confirm "extrafine merino"), care, fit, chest/length/sleeve per size, model pair if known |
| Nora (2XL only) | single-size measurements still useful | composition, care, fit, garment measurements for 2XL |
| Ivy (S only) | same | composition, care, fit, measurements for S |
| Cardigan (L only) | same | composition (confirm listing claim), care, fit, measurements for L |

## Import-ready metaobject skeleton (structure only — do not create with fake numbers)

```json
{
  "type": "hivolt_size_chart",
  "fields": {
    "title": "Elena mock neck sweater — womens M-XXL",
    "measurement_basis": "garment",
    "source_unit": "cm",
    "columns": ["Size", "Chest", "Length", "Sleeve"],
    "rows": [["M", "", "", ""], ["L", "", "", ""], ["XL", "", "", ""], ["XXL", "", "", ""]],
    "note": "Garment measured flat; measurements from supplier chart.",
    "source_reference": "<supplier document reference>"
  }
}
```

Rules: store the supplier's unit as given (`source_unit`) and never
hand-convert; render US/EU conversions in Liquid at display time. One chart
serves every product cut from the same block. If a chart is absent the size
guide renders nothing — no placeholder, no generic table (enforced by the
existing `spec.size_chart` gating). Impulse also offers a page-based
`size_chart` PDP block; the metaobject path is preferred because it is
per-block structured data, not a shared page.
