# HIVOLT favicon — 2026-08-30

## Where it came from

Nothing here is invented. The mark, the accent and the ground all come from
`site/brand/hivolt-badge.png`, supplied by the owner on 2026-08-23 and
designated in `site/brand/README.md` for favicon use.

An earlier attempt in this session drew a geometric serif "H" before that
README was read. It was discarded: HIVOLT already has an authoritative mark,
and inventing a second identity in the browser tab would fragment the brand.

## Why the badge could not be used as-is

The badge is a circular composition — volt ring, volt swoosh, "HIVOLT"
wordmark, and the tagline line beneath it. The wordmark and tagline are
illegible below roughly 64px, which is above every size a browser renders a
favicon at.

So the swoosh is isolated from the badge and re-set on the brand ground. This
is ordinary practice: a favicon takes the icon, not the lockup.

## How it is built

`site/brand/make-favicon.py`, deterministic, no image generation involved.

1. Volt pixels are found by colour match against `#DAF305`.
2. The search window is masked to a circle at 80% of the badge radius, so the
   ring — whose inner edge sits near 87% — cannot leak into the crop.
3. The window stops at 62% of height, above the wordmark and tagline.
4. The resulting mark is 826×383, a ratio of 2.16.
5. It is scaled on **width** to 86% of the canvas, not on the longest edge.
   Scaling on the longest edge leaves a 2.16:1 mark stranded in vertical
   whitespace, and it disappears at 16px. This was the first attempt's defect.

Ground is `#090909`, the brand ground named in README.md.

## Verification

Both defects were caught by rendering a contact sheet at 512 / 64 / 48 / 32 /
16px and looking at it, not by assuming the output was right. The first pass
showed two stray volt fragments in the upper corners — ring leakage — and a
mark too small to read. Both are fixed in the committed version.

The mark holds at 48 and 32. At 16px it reads as a volt shape rather than a
legible swoosh; that is the honest limit of any 2.16:1 mark in a square canvas.

## On Shopify

Uploaded and confirmed `READY`, 512×512:

- `gid://shopify/MediaImage/40506617889000`
- `hivolt-favicon_ff4f5ce0-aa22-4355-a956-2168dcd15062.png`

Shopify appended a UUID to the filename — the same suffix pattern that defeated
the first catalogue image dedup, recorded in `docs/CLONE-CONSOLIDATION.md`.

## Not applied to the theme, deliberately

`favicon` lives in `config/settings_data.json` alongside 111 other settings, and
`themeFilesUpsert` replaces whole files rather than patching keys. A rebuilt
copy of that file came out ~1,700 bytes larger than the stored one, so it was
not a faithful reproduction and was discarded rather than pushed. Replacing 112
verified settings with an unverified reconstruction to change one key is not a
trade worth making.

**Set it in the theme editor instead:** Online Store → Themes → Customize →
Theme settings → Favicon → choose `hivolt-favicon`. Three clicks, no risk to
the other settings.
