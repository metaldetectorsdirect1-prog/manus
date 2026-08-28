# HIVOLT-SUPPLIER-DATA-REQUEST.md — 2026-08-28

Ready-to-send information request for the suppliers behind the 4 catalog
products (AutoDS sources: Walmart ×2, Amazon ×1, AliExpress-replacement ×1
— see PRODUCT-RESEARCH.md §4.3.1). Nothing below may be filled by
inference: not from photos, not from the supplier's location, not by AI.

## Trust-classification model (acceptance rule — binding)

- **CLASS A** — physically verified on the garment / official documentation
  (label photo, commercial invoice, origin declaration).
- **CLASS B** — supplier written documentation (spec sheet, size table,
  packing list, direct written answer).
- **CLASS C** — supplier marketing description (listing copy).
- **CLASS D** — inference / AI / guess.

**Customer-facing factual specification fields (composition, care, origin,
measurements, GTIN, HS, weight) require CLASS A or B.** CLASS C may inform
subjective merchandising copy only ("relaxed drape") and may seed a request
for B-class confirmation. CLASS D is never acceptable for any factual
field. Note: the cardigan's listing text includes a composition line —
that is CLASS C until the supplier confirms it or a care-label photo
(CLASS A) is provided.

## Request table (one block per product; send as-is)

For **each** product / its single variant (Elena: per size-color run):

| Field required | Why | Example format | US launch? | International? | Evidence expected |
|---|---|---|---|---|---|
| Fibre composition | PDP spec + fiber-labeling rules | "70% acrylic / 30% wool" | **MANDATORY** (Textile Act labeling) | MANDATORY | care-label photo or spec sheet |
| Care instructions | PDP + claims accuracy | "Machine wash cold, lay flat to dry" | MANDATORY | MANDATORY | care-label photo |
| Country of origin | labeling + customs | "Made in China" | MANDATORY (US origin labeling) | MANDATORY | origin declaration / label photo |
| Garment measurements per size | size guide | chest/length/sleeve in cm, per size | STRONG | MANDATORY | measurement chart |
| Fit description | PDP fit row | "Relaxed fit" (their words) | RECOMMENDED | RECOMMENDED | spec sheet |
| Packaged weight | shipping accuracy | "0.45 kg" | RECOMMENDED (3/4 currently 0) | MANDATORY | packing list |
| GTIN/UPC confirmation | GMC identifier | "Barcode 313044363315 is a registered UPC: yes/no" | MANDATORY before feed | MANDATORY | barcode record |
| Manufacturer + MPN (if any) | GMC brand_mpn path | "Style #KN-2241" | Conditional | Conditional | spec sheet |
| HS code | customs | "6110.30" (their classification) | not needed (US-only) | MANDATORY | commercial invoice |
| Model height + size worn (their photos) | PDP model row | "175 cm, wears S" | OPTIONAL | OPTIONAL | shoot notes |

Products to reference in the request:
1. Elena relaxed merino wool mock neck sweater (17 colors, M–XXL) — also confirm "extrafine merino" composition claim explicitly.
2. Nora oversized chunky knit winter sweater (Wine Red, 2XL)
3. Ivy soft chunky knit turtleneck sweater (Dark Brown, S)
4. Warm cable knit cardigan with pockets (Grey, Women's L) — confirm the composition stated in the listing.

On receipt: data is entered verbatim into `spec.*` /
`inventoryItem.countryCodeOfOrigin` / `harmonizedSystemCode` / weights,
each tagged with its class in the entry commit; anything still CLASS C
stays out of the spec table.
