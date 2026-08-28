# HIVOLT-V2-IMAGE-REVIEW.md — owner review index

Verified against fresh Shopify read-backs 2026-08-28 (theme files, Files API).
Scope: dev theme `158753849576` (UNPUBLISHED) only. Live theme untouched.

**Every image below is PREVIEW ACTIVE — OWNER VISUAL APPROVAL REQUIRED.**
Approved: 0. Pixel verification has not been performed by the builder (image
CDNs are egress-blocked from the build environment). No image may become part
of a published HIVOLT storefront until it passes owner visual review for:
logos, fake logos, lettering, watermarks, anatomy, hands, faces, clothing
artifacts, and overall premium quality.

## How to command changes (no ambiguity)

- **"replace image 4 with alternate A2"** → the file wired in slot 4 is
  swapped for the alternate's filename in the theme template. Alternates can
  replace only the slot listed in their "Replaces" column.
- **"regenerate image 7"** → a new Higgsfield generation is run for that
  slot's brief (same model, hardened zero-logo battery), rendered to your
  gallery for approval before any upload.
- **"inpaint image 7: <defect>"** → localized correction via `nano_banana_2`
  mask inpaint on that job's frame.

## A. Preview-active images (visible homepage, in page order)

All V2, generated 2026-08-28 on Higgsfield `soul_2` (2k). File IDs are
`gid://shopify/MediaImage/<id>`.

| INDEX | ASSET NAME | HOMEPAGE SECTION | DESKTOP / MOBILE | MODEL | JOB ID | SHOPIFY FILE ID | STATUS |
|---|---|---|---|---|---|---|---|
| 1 | hivolt-home-hero-desktop | hero | Desktop | soul_2 | 5dd3aa55 | 40461484097768 | OWNER VISUAL APPROVAL REQUIRED |
| 2 | hivolt-home-hero-mobile | hero | Mobile | soul_2 | 89735897 | 40461484196072 | OWNER VISUAL APPROVAL REQUIRED |
| 3 | hivolt-trend-knitwear | trend-row tile 1 · also campaign-01 mobile | Both | soul_2 | 57002ff2 | 40461484327144 | OWNER VISUAL APPROVAL REQUIRED |
| 4 | hivolt-trend-new-season | trend-row tile 2 · also campaign-02 mobile | Both | soul_2 | 100faf73 | 40461484359912 | OWNER VISUAL APPROVAL REQUIRED |
| 5 | hivolt-trend-essentials | trend-row tile 3 | Both | soul_2 | a0faa3a4 | 40461484392680 | OWNER VISUAL APPROVAL REQUIRED |
| 6 | hivolt-trend-outerwear | trend-row tile 4 | Both | soul_2 | 4567a1c1 | 40461484425448 | OWNER VISUAL APPROVAL REQUIRED |
| 7 | hivolt-women-campaign-01 | campaign-01 | Desktop | soul_2 | 1bee9348 | 40461484261608 | OWNER VISUAL APPROVAL REQUIRED |
| 8 | hivolt-cat-knitwear | category-strip tile 1 | Both | soul_2 | 2c871dbf | 40461484654824 | OWNER VISUAL APPROVAL REQUIRED |
| 9 | hivolt-cat-cardigans | category-strip tile 2 | Both | soul_2 | e445022e | 40461484687592 | OWNER VISUAL APPROVAL REQUIRED |
| 10 | hivolt-cat-sweaters | category-strip tile 3 | Both | soul_2 | 4b3b3671 | 40461484720360 | OWNER VISUAL APPROVAL REQUIRED |
| 11 | hivolt-cat-new-in | category-strip tile 4 | Both | soul_2 | bdf5efa9 | 40461484753128 | OWNER VISUAL APPROVAL REQUIRED |
| 12 | hivolt-women-campaign-02 | campaign-02 | Desktop | soul_2 | c23a892f | 40461484294376 | OWNER VISUAL APPROVAL REQUIRED |
| 13 | hivolt-collage-anchor | collage tile 1 (anchor) | Both | soul_2 | 70d8f468 | 40461484490984 | OWNER VISUAL APPROVAL REQUIRED |
| 14 | hivolt-collage-01 | collage tile 2 | Both | soul_2 | e8a1dca5 | 40461484523752 | OWNER VISUAL APPROVAL REQUIRED |
| 15 | hivolt-collage-02 | collage tile 3 | Both | soul_2 | bffb2954 | 40461484556520 | OWNER VISUAL APPROVAL REQUIRED |
| 16 | hivolt-collage-03 | collage tile 4 | Both | soul_2 | 7fa93f7b | 40461484589288 | OWNER VISUAL APPROVAL REQUIRED |
| 17 | hivolt-collage-04 | collage tile 5 | Both | soul_2 | b8971ba8 | 40461484622056 | OWNER VISUAL APPROVAL REQUIRED |
| 18 | hivolt-featured-evening | featured-evening | Both (same file) | soul_2 | fd0df807 | 40461484458216 | OWNER VISUAL APPROVAL REQUIRED |
| 19 | hivolt-brand-moment | newsletter | Both | soul_2 | 6c7cf058 | 40461484785896 | OWNER VISUAL APPROVAL REQUIRED |

19 distinct files wired into visible sections. Images 3 and 4 each serve two
slots (their trend tile plus a campaign section's mobile crop) — replacing or
regenerating them changes both slots unless a dedicated mobile campaign frame
is commissioned.

## B. Alternate candidates (uploaded, not wired — instant swap)

| INDEX | ASSET NAME | REPLACES | MODEL | JOB ID | SHOPIFY FILE ID | STATUS |
|---|---|---|---|---|---|---|
| A1 | hivolt-home-hero-desktop-alt2 | image 1 | soul_2 | 80a88caf | 40461484130536 | OWNER VISUAL APPROVAL REQUIRED |
| A2 | hivolt-home-hero-desktop-alt3 | image 1 | soul_2 | dd049de5 | 40461484163304 | OWNER VISUAL APPROVAL REQUIRED |
| A3 | hivolt-home-hero-mobile-alt2 | image 2 | soul_2 | f9a527b3 | 40461484228840 | OWNER VISUAL APPROVAL REQUIRED |

19 wired + 3 alternates = the 22-image V2 program. No other alternates exist
in Shopify Files; additional candidates from the generation session live only
in the Higgsfield gallery already rendered to your chat.

## C. Disabled-section assets (batch 2, 2026-08-27 — zero customer exposure)

Wired only inside `"disabled": true` homepage sections held for the future
men's / mixed-gender launch. Same approval gate applies before any of these
sections is ever enabled.

| INDEX | ASSET NAME | SECTION (disabled) | MODEL (served) | JOB ID | SHOPIFY FILE ID | STATUS |
|---|---|---|---|---|---|---|
| D1 | hivolt-master-hero-desktop | master-hero-disabled | nano_banana_2 | 186202dc | 40460456558824 | OWNER VISUAL APPROVAL REQUIRED — read-back anomaly, see note |
| D2 | hivolt-master-hero-mobile | master-hero-disabled | nano_banana_2 | a76c5945 | 40460456591592 | OWNER VISUAL APPROVAL REQUIRED |
| D3 | hivolt-men-editorial-desktop | men-hero-disabled | soul_2 | d7332b58 | 40460456624360 | OWNER VISUAL APPROVAL REQUIRED |
| D4 | hivolt-men-editorial-mobile | men-hero-disabled | soul_2 | 855fd3da | 40460456657128 | OWNER VISUAL APPROVAL REQUIRED |
| D5 | hivolt-men-new-season | men-trends-disabled tile 1 | soul_2 | 994fb4f1 | 40460456689896 | OWNER VISUAL APPROVAL REQUIRED |
| D6 | hivolt-men-smart-casual | men-trends-disabled tile 2 | soul_2 | 86e3f371 | 40460456722664 | OWNER VISUAL APPROVAL REQUIRED |
| D7 | hivolt-men-street-style | men-trends-disabled tile 3 | soul_2 | 7b4e99d5 | 40460456755432 | OWNER VISUAL APPROVAL REQUIRED |
| D8 | hivolt-men-denim | men-trends-disabled tile 4 | soul_2 | e3f00de7 | 40460456788200 | OWNER VISUAL APPROVAL REQUIRED |

**D1 note:** the 2026-08-28 Files read-back returned `image: null` for
`hivolt-master-hero-desktop` (40460456558824) — the file record exists but
Shopify reports no image URL (possible processing failure on the 21:9 4K
source). No customer impact (its section is disabled). If the master section
is ever approved for activation, this file must be re-verified or re-uploaded
first.

## D. Uploaded but not wired anywhere (batch 2 — NOT ACTIVE)

hivolt-men-essentials (a6b704e5 / 40460456820968) ·
hivolt-women-denim (10e4b4ed / 40460456853736) ·
hivolt-women-evening (aa92c92d / 40460456886504) ·
hivolt-brand-editorial (9d82692c / 40460456919272).

## E. V1 program — NOT ACTIVE (rejected)

All batch-1 files (`campaign-*`, `tile-*`, 2026-08-28T02:36Z uploads) were
demoted after the owner's visual rejection and are referenced by no section.
They remain in Files as history only. Job-id map: `docs/AI-IMAGE-PRODUCTION.md`.
