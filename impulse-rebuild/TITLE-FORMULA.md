# TITLE-FORMULA.md

Module 7.3 operationalized (full reference: the `google-product-titles` skill).

## The formula

`[First Name] [Audience] [ONE feeling] [3–4 stacked keywords]`

| Slot | SEO value | Rule |
|---|---|---|
| Keywords (green) | **the whole point** | 3–4, from the scored list, stacked to catch multiple queries |
| Feeling (purple) | medium | exactly one; prefer ones that are also queries (*relaxed, wide-leg, oversized, warm*) — those do both jobs |
| Name + audience (orange) | none | brand polish; never counts toward the keyword budget |

Enforced in `check-product-listing.py` as a **style layer** (warnings): >8 words,
≥2 feeling words, any word repeated. Compliance refusals stay separate.

## First-name rotation pools

Convention pools for the two markets (common names, rotated, never reused
across the catalog — the batch validator's title-uniqueness makes reuse visible):

- **US:** Olivia, Emma, Ava, Sophia, Mia, Harper, Evelyn, Luna, Hazel, Nora
- **UK:** Amelia, Isla, Ivy, Freya, Grace, Lily, Elsie, Florence, Poppy, Daisy

## The one keyword-stuffing boundary

`Maria Women's Knee-High Heeled Cowboy Boots` = 3 queries in 6 words — correct.
Adding a 5th keyword tips into stuffing and **lowers** rank. More is not better;
overlap is better.

## Honesty rule that outranks the formula

**The title must be true to the image.** A title change on an approved product
can retrigger review, and title–image mismatch is a misrepresentation flag — the
same suspension class this whole engagement exists to avoid. The validator's
trademark/medical screens apply to titles regardless of formula fit.
