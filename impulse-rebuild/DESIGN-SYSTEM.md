# DESIGN-SYSTEM.md — HIVOLT

Governed by the **HIVOLT Design Standard Directive**. Where that conflicts with
an Impulse preset, the directive wins; where it conflicts with §3 Hard Rules,
§3 wins.

Applied to **`158753652968` (UNPUBLISHED)** and verified by value read-back.

## The dual-register rule

Two kinds of surface, designed differently. This is recorded first because
getting it backwards is the failure mode the directive singles out.

| | **Brand surfaces** | **Decision surfaces** |
|---|---|---|
| Where | hero, editorial, About, lookbook, collection banners, blog | product page, size guide, cart, shipping/returns, FAQ |
| Goal | restraint | **completeness** |
| Copy | sparse | dense, scannable |
| Whitespace | generous | subordinate to information |
| Test | does the photography carry it? | can she buy without hunting? |

A sparse product page reads as hiding something. Density there is confidence.

## Palette

| Token | Hex | Role |
|---|---|---|
| ink | `#141414` | Body text, dark grounds. **Not** `#000` |
| ground | `#F8F6F2` | Page. Warm off-white. **Not** `#fff` |
| **volt** | `#DAF305` | **The accent — primary CTA and nothing else** |
| muted | `#5E5A54` | Secondary text |
| hairline | `#8E8880` | Borders. Hairline only |
| sale | `#9B2C2C` | Genuine compare-at markdowns only. Separate from the accent |

### Accent discipline

Volt appears on exactly **two** settings — `color_button` and
`color_drawer_button`. Both are the primary CTA. It is on no heading, no icon,
no border, no announcement bar, no sale tag.

### Contrast — measured

| Pair | Ratio | Min | |
|---|---:|---:|---|
| ink on ground | 17.07:1 | 4.5 | PASS |
| muted on ground | 6.34:1 | 4.5 | PASS |
| ground on ink | 17.07:1 | 4.5 | PASS |
| **ink on volt (the CTA)** | 14.74:1 | 4.5 | PASS |
| hairline on ground | 3.25:1 | 3.0 | PASS |
| sale on ground | 6.97:1 | 4.5 | PASS |

## Typography

Two families, two weights — well under the 4-weight cap.

| Role | Family | Notes |
|---|---|---|
| Display | **`instrument_serif_n4`** | High-contrast display serif. Carries the fashion-house register |
| Body / UI | **`fustat_n4`** | Neutral grotesque |

| | Value |
|---|---|
| Body | **17px**, line-height **1.6**, tracking 0 |
| H1 | **60px**, line-height 1.1 |
| Nav | body face, 13px, **uppercase** |
| Buttons | body face, uppercase |

**H1/body contrast: 3.5×.**

### Two schema clamps worth knowing

Impulse constrains what the directive asks for:

- `type_header_base_size` — a 1.333-scale H1 of **72px was rejected outright**
  (`can't be greater than 60`). Set to the 60 maximum. Hero sections carry their
  own larger `title_size`, so the hero can still exceed the global H1.
- `type_header_line_height` — **1.05 was silently clamped to 1.1.** No error was
  returned. This is precisely why verification here is by value read-back and
  never by checksum.

## Space, form, motion

- **8pt grid.** Section padding 120–160px desktop / 56–72px mobile is a
  section-level setting and is applied per template as those are built.
- **Sharp radius (0)** on every button, input, card and image container.
  Hairline borders. No shadows, no gradients, no glow.
- Motion: `animate_sections` (rise-up) and `animate_images` (fade-in) on;
  **page-transition animation off** so nothing delays the hero.
  `type_header_capitalize: false`, `quick_shop_enable: false` — no badge or
  overlay clutter on the product card.

## Corrections made to my own earlier pass

The first Phase 2 build failed this directive on six points. Recorded because
the settings were live on the dev theme before being corrected:

| Was | Now | Why it failed |
|---|---|---|
| ink `#0B0B0B` | `#141414` | Below the `#111` floor — effectively pure black |
| ground `#FAFAF8` | `#F8F6F2` | Cool, not warm |
| CTA `#0B0B0B` (ink) | `#DAF305` (volt) | **Accent must be the CTA.** I had it inverted |
| sale tag = volt | `#9B2C2C` | Sale must be separate from the accent |
| volt on cart dot + announcement | ink / ground | Accent was leaking beyond the CTA |
| line-height 1.5 | 1.6 | Below the 1.55 floor |
| heading = `host_grotesk` | `instrument_serif_n4` | No display/body family contrast |

## Not set — waiting on the catalog (§9)

Photographic language, hero, category tiles, collection banners, and the
supplier-image normalization pass. The visual language must match the real
garments, not precede them.

---

## Binding constraint on imagery (§2.2)

**Volt only works if everything around it stays chromatically quiet.** `#DAF305`
is inherited from HIVOLT's performance-brand identity. Confined to the primary
CTA at under 5% of a viewport, against near-black and warm paper, it reads as a
signature. Put it against saturated photography and it stops being a signature
and becomes a sports brand imitating a fashion house.

This is a **constraint on Phase 6, not a preference:**

- Product and editorial photography **must be neutral or low-saturation.**
- **One chromatic event per screen, and it is the button.**
- No saturated backgrounds. No coloured gradients. No secondary bright accents.

If imagery comes back saturated, the accent has to be reconsidered before the
imagery ships — not after. The palette and the photographic direction are one
decision, and this is the half that is already locked.
