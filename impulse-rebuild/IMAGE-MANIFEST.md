# IMAGE-MANIFEST.md

Non-product imagery generated 2026-08-24. All uploaded to Shopify Files, all
`fileStatus: READY`, all referenced as `shopify://shop_images/<filename>`.

## Constraints applied

Neutral, low-saturation, no faces, no text baked in, no logos. The generation
palette was pinned to six values — `#F8F6F2 #E8E4DC #B8B2A7 #6E6A63 #2A2724
#141414` for the light set and `#141414 #1F1D1B #2A2724 #4A4640 #8A8378 #C9C2B6`
for the dark — and **volt `#DAF305` was deliberately excluded from every prompt**.
It survives as a signature only because nothing around it is chromatic. One
chromatic event per screen, and it is the button.

Visual language: **material and light** — undyed cloth, seam and stitch detail,
plaster and paper surfaces, low raking daylight. Chosen because it is the honest
register for a store whose position is "we publish what we know": it shows the
thing itself rather than a lifestyle around it, and it needs no model release,
no invented customer, and no claim.

## Assets in use

| File | Used by | Dimensions | Alt text |
|---|---|---|---|
| `hivolt-hero-dark-desktop.png` | homepage hero (`slideshow`) | 2688×1536 | Pale undyed cloth catching a narrow shaft of low side light in a deep charcoal studio interior |
| `hivolt-editorial-seam-detail.png` | homepage `editorial-construction` | 896×1152 | Macro detail of a flat-lock seam and topstitching on undyed knit fabric |
| `hivolt-editorial-folded-stack.png` | homepage `editorial-fit` | 896×1152 | Folded undyed garments stacked on a pale plaster shelf in directional daylight |
| `hivolt-newsletter-plaster-bg.png` | homepage `newsletter` | 1344×768 | Warm off-white plaster wall with a soft gradient of directional daylight |
| `hivolt-404-thread.png` | `templates/404.json` | 1024×1024 | A single charcoal thread lying in a loose curve on an empty warm off-white paper surface |

## Assets generated, on the store, not yet wired

| File | Intended slot | Why not wired |
|---|---|---|
| `hivolt-hero-dark-mobile.png` (1792×2304) | mobile hero | The Impulse `slideshow` image block exposes a single `image` key. Section runs `mobile_height: auto`, so the 16:9 desktop frame shows whole on mobile rather than centre-cropping away the text area. Asset is ready if a mobile key exists. |
| `hivolt-og-share.png` (1344×768) | OG / social share | Shopify derives the share image from theme settings or per-page SEO; no `og_image` key exists in this theme's `settings_schema`. Needs an owner-side social-sharing setting or a `layout/theme.liquid` meta edit. |
| `hivolt-journal-default-cover.png` (1280×832) | blog default cover | Impulse falls back per-article, not per-blog. Applies when articles get featured images. |

## Superseded — generated, uploaded, now unused

`hivolt-hero-cloth-desktop.png`, `hivolt-hero-cloth-mobile.png`.

Both are light-ground. **White text failed contrast on them at any usable scrim** —
at 45% overlay the ratio is ~1.9:1, at 65% ~2.8:1, and only past 85% does it clear
4.5:1, by which point the photograph is destroyed. Replaced with the dark pair.
Kept on the store as candidates for light-ground sections where text sits beside
the image rather than over it.

**Measured contrast on the shipped hero:** theme renders slideshow text as
`color_image_text #F8F6F2` over `color_image_overlay #141414` at 25%, plus the
block's own `overlay_opacity: 30`. Against a charcoal image (~0.06 relative
luminance) that is comfortably past 9:1 — AAA. The volt CTA `#DAF305` on that
ground is ~15:1.

## Format

Sources are PNG. Shopify's CDN performs WebP conversion and responsive resizing
at delivery via Impulse's `image_url` filters, so WebP-primary with fallback is
handled at the delivery layer rather than by shipping two files.

## 🔴 Brand-file reconciliation — the 2-of-4 gap

Earlier records claimed four brand files were uploaded. **Two exist:**

| File | On store | Status |
|---|:--:|---|
| `hivolt-badge.png` | ✅ | in use — theme `favicon` |
| `hivolt-lockup-dark.png` | ✅ | **on store but no longer referenced** |
| `hivolt-lockup-light.png` | ❌ | never uploaded |
| `hivolt-lockup.png` | ❌ | never uploaded |

`hivolt-lockup-dark.png` is a lockup built for dark grounds. The theme header is
`color_header: #F8F6F2` — light. It would have rendered as either an invisible
mark or a dark block. Theme `logo` is now `""`, so the header renders the shop
name as text in Instrument Serif, which is legible and on-brand.

**No logo was generated.** A wordmark is text baked into an image, which §4
forbids, and inventing a mark risks diverging from the owner's real one.
**A light-ground lockup has to come from the owner.**
