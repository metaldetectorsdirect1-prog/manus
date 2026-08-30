# Clone-listing consolidation — 2026-08-30

## What was found

57 title-groups held 152 active listings that differed only by a leading
adjective ("Premium", "Cozy", "Refined"…) and, in some groups, a colour word.
Each group therefore sold one garment 2–6 times.

They survived the earlier image dedup (`docs/CATALOG-IMAGE-DEDUP.md`) because
Shopify's re-upload suffix takes more shapes than the regex covered. The sweep
matched only a trailing `_<uuid>`; these carry:

- `<name>.<hash>_<uuid>.jpg`
- `<name>_<uuid>.<hash>.jpg`

Both resolve to a single source file once the hash and uuid are stripped.

Two groups made the case unambiguously:

| Group | Listings | Single underlying source image |
|---|---|---|
| men's stretch smart shirt | 6 | `Ben-Hogan-Men-s-…-Short-Sleeve-Polo-Shirt-up-to-5XL` |
| men's linen blend shirt | 5 | `OALUXE-Flannel-Shirt-for-Men-…-Plaid-Shirts-with-Pocket` |
| women's double-breasted formal coat | 5 | `isa_beige.png` |

They were initially mistaken for a genuine colourway range — Navy, Charcoal,
Dark Brown, Forest Green, Burgundy, Stone — precisely the shape a real range
takes. Pulling the image URLs disproved it.

## Separate defect surfaced by the same evidence

The photographs do not match the titles, and several are branded goods:

- "Stretch Smart Shirt" → a **Ben Hogan** polo shirt
- "Linen Blend Shirt" → an **OALUXE flannel plaid** shirt
- "Poplin Formal Shirt in Sage" → `4000316843-847_blue_1.jpg`
- "Double Pocket Utility Shirt" → `levi-cargo-shirt-178860`

This is product misrepresentation independent of the duplication, it is not
confined to these groups, and it needs its own sweep. Not addressed here.

## Plan correction at write time

The plan was built earlier in the session; the authoritative read taken
immediately before the write found 8 of the 152 listings already deleted, and
they did not fall where the plan assumed:

| Group | Change | Effect on the plan |
|---|---|---|
| men's stainless rope chain necklace | both members gone | dropped, no-op |
| women's layered chain necklace set | both members gone | dropped, no-op |
| men's colour block retro sweatshirt | all 3 excess gone, keeper alive | dropped, no-op |
| men's heavyweight pullover hoodie | **keeper gone**, both excess alive | keeper re-elected |

Applying the plan unamended would have drafted every surviving listing in the
hoodie group, leaving it with none. The keeper was re-elected by the same
lowest-id rule (`9615528001768`).

## Applied

89 listings set to DRAFT. Nothing deleted — DRAFT is reversible and preserves
handles, ids and history.

- Reversal record: `qa/catsweep/clone-drop-final.json` (89 ids)
- Retained: `qa/catsweep/clone-keep.json`, plus the re-elected hoodie keeper

## Verified

`succeeded: 89` from the bulk tool is the tool's own claim and is not evidence.
Independently re-queried after the mutations returned:

- 89/89 `status: DRAFT`, every `updatedAt` moved into the write window
- 55/55 keepers still `ACTIVE`
- invariant re-checked: every surviving group retains exactly one live listing

## Collateral observed, not caused

Four keepers carry `updatedAt` later than the pre-write read while sitting
outside the write set entirely:

| id | before | after |
|---|---|---|
| 9615482323176 | 04:27:20 | 04:55:06 |
| 9615497560296 | 04:28:44 | 04:57:00 |
| 9615525150952 | 03:47:51 | 04:57:22 |
| 9615524823272 | 04:32:04 | 04:57:54 |

A concurrent writer is active. It had been reported stopped; it is not.
