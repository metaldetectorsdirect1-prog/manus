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

## Applied

Set on draft `158911987944` in `config/settings_data.json`:

```
"favicon": "shopify://shop_images/hivolt-favicon_ff4f5ce0-aa22-4355-a956-2168dcd15062.png"
```

**Correction.** An earlier pass declined to write this file, reasoning that a
rebuilt copy came out ~1,700 bytes larger than the stored one and so could not
be faithful. That reasoning was wrong: Shopify's `size` field is not the byte
length of the content string, so the comparison meant nothing. Counting the
real file, `current` holds exactly 112 keys — the same 112 the rebuild
produced. The file was faithful and was rejected for a bad reason.

Verified after the write:

| Check | Result |
|---|---|
| `current.favicon` | set to the uploaded asset |
| File size | 5,840 → 5,920 bytes, **+80** — one string inserted, not a rewrite |
| `checksumMd5` | `14d0154877…` → `ddacc48979…` |
| `presets.Impulse.favicon` | still `""`, untouched |
| Unrelated settings | palette, typography, cart, checkout, social, inventory all preserved |
| Draft role | still `UNPUBLISHED` |

The +80 delta is the load-bearing check. A clobbered file would move by
thousands of bytes; a single inserted path moves it by the length of that path.

## The published theme refuses this write

Writing the same file to `158911561960` (role `MAIN`) was attempted and
refused server-side:

```
blocked: true   matched: themeFilesUpsert
category: live_theme   kind: targets_live
"Theme file writes against the live storefront are blocked."
```

This is an observed refusal, not a quoted policy. No theme was published or
unpublished to work around it. Confirmed afterwards: the live theme's
`settings_data.json` is byte-identical to before the attempt — same 5,840
bytes, same `14d0154877ee2c295c9ec1fdf38aa14f` — and its `updatedAt` did not
move.

The favicon reaches the storefront when draft `158911987944` is published,
along with every other staged fix.
