# DESIGN-SYSTEM.md — HIVOLT

Derived from the owner-supplied logo, not invented. The accent is sampled from
`site/brand/hivolt-badge.png`; nothing here is a guess at the brand's colour.

## Palette

| Token | Hex | Role |
|---|---|---|
| `ink` | `#0B0B0B` | Ground for dark surfaces, all body text on light |
| `paper` | `#FAFAF8` | Page background. Warm off-white, not pure `#fff` |
| `volt` | `#DAF305` | **The** accent. CTAs, focus rings, sale tag |
| `muted` | `#5A5A56` | Secondary text, captions |
| `border` | `#90908C` | Rules, input borders, dividers |
| `sale` | `#B3261E` | Sale/markdown only |

### Contrast — measured, all pass

| Pair | Ratio | Min | |
|---|---:|---:|---|
| body on paper | 18.83:1 | 4.5 | PASS |
| muted on paper | 6.63:1 | 4.5 | PASS |
| paper on ink | 18.83:1 | 4.5 | PASS |
| ink on volt (button) | 15.75:1 | 4.5 | PASS |
| volt on ink | 15.75:1 | 4.5 | PASS |
| border on paper | 3.07:1 | 3.0 | PASS |
| sale on paper | 6.25:1 | 4.5 | PASS |

### The one rule about volt

**Volt is never text on a light background.** `#DAF305` on `#FAFAF8` measures
**1.20:1** — effectively invisible. It is only ever:

- a **fill** with ink text on top (buttons, tags), or
- **text on ink** (footer, dark sections).

The first border I specified (`#D8D7D2`) failed at 1.38:1 and was replaced by
`#90908C` — the first value on a warm grey ramp that clears 3:1.

## Typography

Impulse ships `host_grotesk` / `fustat`. Keeping the pairing — both are
variable, well-hinted, and already loaded, so swapping costs two font downloads
for no legibility gain.

| | Setting |
|---|---|
| Heading | `host_grotesk_n5`, line-height 1.1, tracking 25 |
| Body | `fustat_n4`, **17px** base, line-height **1.5** |
| Nav | heading face, 14px, uppercase, tracking 25 |

Base 17px clears the ≥16px mobile floor. Body line-height moved 1.4 → 1.5 to sit
inside the required 1.5–1.65 band.

## Layout

- Spacing on a **4/8pt** scale.
- **Square** buttons and inputs — radius 0. Matches the logo's hard geometry.
- Product imagery **portrait 3:4**, enforced everywhere. `product_grid_image_size: portrait`.
- Collection tiles portrait, text below the image, not overlaid — overlaid text
  on unknown supplier photography is a contrast gamble.

## Motion

Impulse's animation stack is left **off**: `animate_page_transitions`,
`animate_sections`, `animate_images` all `false`. On a dropship catalog with
mixed-quality supplier photography, entrance animation draws the eye to the
weakest asset. `prefers-reduced-motion` is respected by the theme regardless.

## What is deliberately not set

- **Hero, category tiles, collection banners** — product-dependent. Image
  direction has to match real garments, and there are none yet.
- **Free-shipping progress bar** — off. It may only be enabled against a real
  threshold, and shipping terms are unresolved pending supplier selection.
