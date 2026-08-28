# HIVOLT-V3-IMAGE-REVIEW.md — owner review index (V3 active program)

Generated 2026-08-28 after the owner's pixel rejection of V2 (rendered text
artifacts). **Every V2 active asset is demoted to NOT ACTIVE.** Supersedes
`HIVOLT-V2-IMAGE-REVIEW.md`.

Program: 31 images, Higgsfield, model requested `nano_banana_2` (2k) —
**platform served all 31 on `nano_banana_flash`** (recorded truthfully).
31/31 completed, 0 failures. Plus one targeted regeneration on 2026-08-28
(image 24, cat-04 replacement, also served on `nano_banana_flash`).

## 2026-08-28: full technical pixel QA completed in-session

Pixel inspection **became possible** this pass: assets are fetched at native
resolution through the Higgsfield cloud sandbox (which has internet access —
sanctioned tooling, same class as Shopify's server-side `fileCreate` fetch),
re-encoded to size-capped WebP, returned through the tool-result channel and
decoded locally with md5 verification, then reviewed with actual vision.
All 31 originals were reviewed; nine flagged risk zones (hands, faces,
interlaced fingers, knit macro texture) were re-inspected as native-resolution
crops (up to 2528 px sources). In-context rendering at 390/1440 px ran in the
local harness (`qa/home-harness-v3.html`) with the real pixels.

**Outcome: 27 of 31 pass technical QA; 4 rejected; 1 replacement generated,
QA'd and uploaded (verified pixel-identical, RMSE 0).**

**2026-08-28 ~15:50 UTC — OWNER APPROVAL EVENT.** The owner selected
"Approve shortlist, fix, then I publish" — this **owner-approves the
12-image primary set** (shortlist numbers 1–12: files hero-desktop,
portrait-01, trend-01..04, campaign-a, portrait-02, campaign-b,
portrait-03, campaign-c-alt-b, cat-04-b). The 11 supporting assets remain
TECHNICALLY APPROVED and are publish-cleared by the owner's publish
instruction; backups stay unapproved candidates; the 4 pixel-QA rejects
stay rejected.

**Publication state:** the owner self-published the MASTER CANDIDATE
(`158753849576`) from admin at 15:41 UTC — **it is now MAIN** — before the
approved swaps (14→24, 17→A9) could land, so the live homepage briefly
carries rejected image 14. Live-theme writes are connector-blocked (not
worked around). Remediation done per the established deploy route: live
theme duplicated to **`GENERAL STORE — MASTER r2 (approved image swaps)`
(`158874960104`, UNPUBLISHED)**, swaps applied and checksum-verified
(`templates/index.json` = 1ec45ae6…). **Owner action: publish MASTER r2**
to take the defective tile off the live storefront.

**The owner now reviews only 12 images**, in
`docs/review/GENERAL-STORE-FINAL-SHORTLIST.html` (primary set + 5 backups,
rendered from the Shopify CDN in the browser). The full 31-frame sheet
remains at `docs/review/hivolt-v3-contact-sheet.html` for spot-checks.

## Commands (no ambiguity)

- **"Approve: 1, 3, 5…" / "Reject: 2, 7"** — shortlist numbers.
- **"replace image N with BX"** — backup swap from the shortlist.
- **"regenerate image N: <reason>"** — new generation for that slot's brief,
  gallery first, no auto-wire.
- **"inpaint image N: <defect>"** — localized mask correction.

## A. Preview-active (wired into visible homepage, page order)

GAL = frame number in the rendered gallery. SL = number in the FINAL
SHORTLIST. File IDs are `gid://shopify/MediaImage/<id>`.

| INDEX | ASSET | SECTION | D/M | JOB | GAL | SL | FILE ID | STATUS |
|---|---|---|---|---|---|---|---|---|
| 1 | hivolt-v3-hero-desktop | hero | Desktop | 4debf814 | 1 | 1 | 40461663240424 | RECOMMENDED FOR OWNER APPROVAL (8.7) |
| 2 | hivolt-v3-portrait-01 | hero | Mobile | 2b0692b3 | 4 | 2 | 40461663338728 | RECOMMENDED FOR OWNER APPROVAL (8.8) |
| 3 | hivolt-v3-trend-01 | trending tile 1 | Both | ba81039e | 16 | 3 | 40461663731944 | RECOMMENDED FOR OWNER APPROVAL (8.8) |
| 4 | hivolt-v3-trend-02 | trending tile 2 | Both | 68b7c08a | 17 | 4 | 40461663764712 | RECOMMENDED FOR OWNER APPROVAL (8.8) |
| 5 | hivolt-v3-trend-03 | trending tile 3 | Both | 07cfc4a2 | 18 | 5 | 40461663797480 | RECOMMENDED FOR OWNER APPROVAL (8.7) |
| 6 | hivolt-v3-trend-04 | trending tile 4 | Both | 0187a46b | 19 | 6 | 40461663830248 | RECOMMENDED FOR OWNER APPROVAL (8.8) |
| 7 | hivolt-v3-campaign-a | campaign-a | Desktop | ab2e1403 | 7 | 7 | 40461663437032 | RECOMMENDED FOR OWNER APPROVAL (8.7) |
| 8 | hivolt-v3-portrait-02 | campaign-a | Mobile | 9c8d336c | 5 | 8 | 40461663371496 | RECOMMENDED FOR OWNER APPROVAL (9.0) |
| 9 | hivolt-v3-campaign-b | campaign-b | Desktop | a1ab7fcb | 10 | 9 | 40461663535336 | RECOMMENDED FOR OWNER APPROVAL (8.8) |
| 10 | hivolt-v3-portrait-03 | campaign-b | Mobile | 6c3e24be | 6 | 10 | 40461663404264 | RECOMMENDED FOR OWNER APPROVAL (8.7) |
| 11 | hivolt-v3-cat-01 | category tile 1 (Knitwear) | Both | 24033f6a | 20 | — | 40461663863016 | TECHNICALLY APPROVED (8.8) |
| 12 | hivolt-v3-cat-02 | category tile 2 (Sweaters) | Both | 4fe8303e | 21 | — | 40461663895784 | TECHNICALLY APPROVED (8.8) |
| 13 | hivolt-v3-cat-03 | category tile 3 (Cardigans) | Both | 345b1579 | 22 | — | 40461663928552 | TECHNICALLY APPROVED (8.8) |
| 14 | hivolt-v3-cat-04 | category tile 4 (New in) | Both | dbd60999 | 23 | — | 40461663961320 | **REJECTED — PIXEL QA** (AI defect: frame is a 3×2 grid of six repeated identical torsos). Replaced by image 24 |
| 15 | hivolt-v3-cat-05 | category tile 5 (Essentials) | Both | ce646d17 | 24 | — | 40461663994088 | TECHNICALLY APPROVED (8.6) |
| 16 | hivolt-v3-cat-06 | category tile 6 (Layers) | Both | 225b0af8 | 25 | — | 40461664026856 | TECHNICALLY APPROVED (8.8) |
| 17 | hivolt-v3-campaign-c | campaign-c | Both (3:2) | a3dd2dc0 | 13 | B5 | 40461663633640 | BACKUP (8.2) — slot primary is now A9; far-hand fingertips not fully crop-verifiable |
| 18 | hivolt-v3-collage-anchor | collage anchor | Both | 51505423 | 26 | — | 40461664059624 | TECHNICALLY APPROVED (8.7) — interlaced hands crop-verified |
| 19 | hivolt-v3-collage-01 | collage tile 2 | Both | a5504d50 | 27 | — | 40461664092392 | TECHNICALLY APPROVED (8.4) — cable structure verified at native 2048 px |
| 20 | hivolt-v3-collage-02 | collage tile 3 | Both | f4f07f2f | 28 | — | 40461664125160 | TECHNICALLY APPROVED (8.6) — hand macro: five digits, correct articulation |
| 21 | hivolt-v3-collage-03 | collage tile 4 | Both | 3a9668bc | 29 | — | 40461664157928 | TECHNICALLY APPROVED (8.6) |
| 22 | hivolt-v3-collage-04 | collage tile 5 | Both | eb2b7151 | 30 | — | 40461664190696 | TECHNICALLY APPROVED (8.8) |
| 23 | hivolt-v3-newsletter | newsletter | Both | 028a3ab5 | 31 | — | 40461664223464 | TECHNICALLY APPROVED (9.1) — no humans, zero anatomy risk |
| 24 | hivolt-v3-cat-04-b | category tile 4 (New in) — **unwired** | Both | f4b17de2 | — | 12 | 40464845897960 | RECOMMENDED FOR OWNER APPROVAL (8.6) — regenerated 2026-08-28, pixel-QA'd pre-upload, CDN copy verified RMSE 0 vs source |

## B. Alternate candidates (uploaded, unwired — instant swap)

| INDEX | ASSET | REPLACES | JOB | GAL | SL | FILE ID | STATUS |
|---|---|---|---|---|---|---|---|
| A1 | hivolt-v3-hero-desktop-alt-b | image 1 | fab0badc | 2 | — | 40461663273192 | **REJECTED — PIXEL QA** (redundant: static energy, weakest hero candidate) |
| A2 | hivolt-v3-hero-desktop-alt-c | image 1 | cbe3261a | 3 | B1 | 40461663305960 | BACKUP (8.5) |
| A3 | hivolt-v3-portrait-02 (as hero mobile) | image 2 | 9c8d336c | 5 | =8 | 40461663371496 | duplicate of image 8 — covered by its approval |
| A4 | hivolt-v3-portrait-03 (as hero mobile) | image 2 | 6c3e24be | 6 | =10 | 40461663404264 | duplicate of image 10 — covered by its approval |
| A5 | hivolt-v3-campaign-a-alt-b | image 7 | 7503ba4f | 8 | B2 | 40461663469800 | BACKUP (8.3) |
| A6 | hivolt-v3-campaign-a-alt-c | image 7 | fd3b5b49 | 9 | — | 40461663502568 | **REJECTED — PIXEL QA** (crop risk: blurred foreground pillar eats right edge; warm film tone off-program) |
| A7 | hivolt-v3-campaign-b-alt-b | image 9 | 93b0d04f | 11 | B4 | 40461663568104 | BACKUP (8.6) |
| A8 | hivolt-v3-campaign-b-alt-c | image 9 | 0df69c79 | 12 | B3 | 40461663600872 | BACKUP (8.8) |
| A9 | hivolt-v3-campaign-c-alt-b | image 17 | 7ee0bdaf | 14 | 11 | 40461663666408 | **PROMOTED to campaign-c primary** — RECOMMENDED FOR OWNER APPROVAL (8.6); hands/face crop-verified at native res |
| A10 | hivolt-v3-campaign-c-alt-c | image 17 | 46514e60 | 15 | — | 40461663699176 | **REJECTED — PIXEL QA** (redundant: third stride frame, lower slot fit) |

Rewiring note: image 14 is still the file wired into category tile 4 and A9
is still unwired. **No theme rewiring has been done this pass** — swaps
(14→24, 17→A9) happen only after owner approval of the shortlist.

## C. Demoted / dormant

- **All V2 actives (22 `hivolt-*` files of 2026-08-28T06:07Z): NOT ACTIVE**
  — no section references them. History in `HIVOLT-V2-IMAGE-REVIEW.md`.
- **All V1 files (`campaign-*`, `tile-*`): NOT ACTIVE** (rejected earlier).
- Batch-2 men's/master files: wired only inside `"disabled": true` sections
  (zero exposure); `hivolt-master-hero-desktop` still carries the
  `image: null` read-back anomaly — re-verify before that section is ever
  enabled.
