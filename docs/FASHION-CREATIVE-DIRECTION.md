# FASHION-CREATIVE-DIRECTION.md — the visual bible

Governs every generated image and every art-direction choice on the HIVOLT
fashion rebuild (dev theme `158753849576`). One brand, one camera, one grade.
Written 2026-08-27. Sits under the store's honesty rules: campaign imagery
represents categories the store actually sells; product cards and PDP
galleries use real product media only.

## Scope honesty — read first

The live catalog today is **4 women's knitwear drafts**. Therefore:

- All launch campaigns are **women-led**. The men's department exists as
  built architecture (sections, navigation slots, creative direction below)
  and its campaigns are generated **when men's inventory exists** — a men's
  hero over zero men's products is a product-truth violation, and every
  "SHOP MEN" CTA would be a dead link (forbidden).
- Category campaigns are generated only for categories with real or
  imminent Phase-5 inventory: knitwear (live), coats/denim/dresses (Phase-5
  allocation, PRODUCT-RESEARCH §8) — generated when their first batch lands.

## The one look

**Camera:** full-frame editorial, 50–85mm feel, shallow-but-honest depth
(f/4 feel — garment texture always resolved, backgrounds soft but legible).
Eye-level or slightly low. No fisheye, no drone, no tilt gimmicks.

**Lighting:** directional soft daylight. Studio: single large key, gentle
falloff, real shadows with soft edges. Location: overcast daylight or
golden-side window light. Never ring-light flatness, never HDR crunch.

**Color grade:** warm neutral. Ivory/stone environments, deep blacks that
hold detail, skin slightly warm, whites never blown. Restraint: the frame's
only saturated notes come from the garments. No teal-orange, no neon.

**Skin & anatomy:** realistic skin with visible texture — no plastic
smoothing. Hands either fully visible and correct or composed out of frame.
Faces sharp or intentionally cropped at the eyeline for texture-focus shots.

**Composition:** subject occupies 60–75% of frame height. Negative space is
deliberately placed on ONE side for the theme's HTML text overlay — the
text-safe zone is part of the brief for every hero/banner. Never place
copy zones over a face.

**Backgrounds:** three approved worlds, nothing else —
1. Warm ivory/stone seamless studio (`#F6F2EB`/`#D8D0C5` family)
2. Minimal contemporary architecture: pale concrete, limestone, soft plaster
3. Muted urban winter street, overcast, defocused

**Styling — women's (active now):** elevated-minimal. The garment is the
subject; styling supports it: straight-leg trousers or clean denim under
knits, minimal gold-tone jewelry (echoes the champagne accent), no visible
third-party logos ever. Hair clean, makeup minimal-editorial.

**Styling — men's (dormant until inventory):** smart-casual minimal;
overcoats, knits, clean denim; same worlds, same grade, same restraint.

**Casting:** contemporary international cast, varied but coherent — the
same campaign family across the site. Believable anatomy, no celebrity
likeness, no exaggerated body types played for effect.

## Aspect-ratio matrix

| Slot | Desktop | Mobile |
|---|---|---|
| Hero | 21:9 (≈2.33:1) | 4:5 |
| Department gateway tiles | 3:4 each | 4:5 |
| Trend-report cards | 3:4 | 3:4 |
| Editorial full-width banner | 2:1 | 4:5 |
| Category tiles | 1:1 | 1:1 |

Every hero/banner is generated twice — desktop AND mobile framing — never
cropped from one master. Mobile frames the subject for a narrow screen with
the text-safe zone top or bottom third.

## Text rule

Generated images contain **no text, no logos, no lettering** anywhere —
headlines, CTAs and prices are theme HTML overlays. A generation with
accidental lettering is rejected regardless of other quality.

## Rejection gate (applied to every candidate before upload)

Reject on any of: wrong finger count / fused hands · warped garment
construction (impossible seams, melted knit structure) · plastic skin ·
asymmetric or dead eyes · lettering or logo artifacts · watermark ghosts ·
background object nonsense · blown highlights on skin · a look that reads
"AI fashion render" rather than photograph. Regenerate, do not repair.

## Palette (theme-side, from the build directive)

Obsidian `#0A0A0B` · Warm Ivory `#F6F2EB` · White `#FFFFFF` · Stone
`#D8D0C5` · Graphite `#2A2928` · Champagne `#B99A6A` (jewelry-rare) ·
Bordeaux `#A01732` / `#7E1327` (sale & urgency only) · Text Grey `#6B6863`.
Main CTA obsidian/white; sale CTA bordeaux/white; secondary transparent
ivory with dark border. Champagne never covers areas larger than a button
border or a thin rule.
