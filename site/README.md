# HIVOLT storefront

**Live previews**
- Homepage — https://claude.ai/code/artifact/2457c34e-d06c-46a2-af97-a73b28a7a22b
- Product page — https://claude.ai/code/artifact/bd82f8ee-0b41-4f4e-a80f-4277e8fa67b3

## Files

| File | What it is |
|---|---|
| `index.html` | Homepage design, standalone. Open in a browser. |
| `product.html` | Product page design, standalone. |
| `index.liquid` | Shopify homepage template. Replaces `templates/index.liquid`. |
| `product.liquid` | Shopify product template. Replaces `templates/product.liquid`. |
| `theme-hivolt.css` | Stylesheet for both. Goes in `assets/` as `hivolt.css`. |
| `product-preview.html` | Self-contained PDP (CSS inlined) — for the artifact only. |
| `shot-*.png` | Rendered screenshots, light and dark, desktop and mobile. |

## Installing on Shopify

1. Online Store → Themes → **Duplicate** your live theme first. Never edit the live one.
2. On the duplicate: Edit code → `assets/` → **Add a new asset** → upload `theme-hivolt.css`,
   renaming it `hivolt.css`.
3. In `layout/theme.liquid`, before `</head>`:
   ```liquid
   {{ 'hivolt.css' | asset_url | stylesheet_tag }}
   ```
4. Replace `templates/index.liquid` with `index.liquid`, and
   `templates/product.liquid` with `product.liquid`.
5. **Preview before publishing.** Check one product page on a phone.

## The two metafields

The catalogue tiles show fabric weight and composition when these exist.
Settings → Custom data → Products → Add definition:

| Namespace & key | Type | Example |
|---|---|---|
| `spec.gsm` | Integer | `220` |
| `spec.composition` | Single line text | `75% nylon / 25% spandex` |
| `spec.rise` | Single line text | `High · 11.5"` |
| `spec.inseam` | Single line text | `31" (size M)` |
| `spec.seams` | Single line text | `Flatlock, 4-thread` |
| `spec.gusset` | Single line text | `Yes, diamond` |
| `spec.opacity` | Single line text | `Opaque under stretch` |
| `spec.care` | Single line text | `Cold wash · hang dry` |

The first two drive the homepage tiles; all eight drive the product page
specification sheet. **A row with no value is not rendered** — never filled with
a placeholder.
That is deliberate — the page's entire claim is that every number on it is real,
and a placeholder would break it on the first product a customer checks.

## What this design does, and why

HIVOLT has no editorial photography, no reviews, and no order history. ICON
Amsterdam — the reference — buys trust with expensive photo shoots. That route is
closed here, and trying to fake it is what produced the 80 fabricated product
images found in the audit.

So this design earns trust the other way: by publishing specifics nobody else in
the category publishes. Fabric weight in g/m², fibre composition, the actual
dispatch location, the real delivery window.

Devices borrowed from ICON that don't need photography:
- Products named to a formula. ICON uses `THE VITO OVERSHIRT`; HIVOLT names by
  fabric weight — `THE 220 FLARE LEGGING`, `THE 165 TRAINING TEE`. Same
  discipline, and the name states a fact.
- All-caps display type, tight tracking, restrained palette, clear price ladder.

The signature element is the **opacity comparator** — drag a slider from 150 to
220 g/m² and the print behind the fabric disappears. It is labelled as a diagram,
not a photograph, on the face of it. It is interactive, it is true, and a
competitor who hasn't specified their fabric cannot copy it.

## What is deliberately absent

No star ratings, no review count, no "12 people are viewing", no countdown, no
stock scarcity, no health claims. A store with zero orders cannot honestly show
social proof, and fabricating it is the same error as the fabricated images —
with more legal exposure, not less.

The "What we publish" section turns those absences into the argument. It is the
only trust play available to a 36-day-old store that is also true.

## The product page

The specification sheet is the top third of the buy column — above the size
picker, above the button. That is deliberate. On a store with no reviews, the
spec sheet is the only evidence a stranger has, so it does the work a review
carousel does elsewhere.

Below the button, a block headed **"What this product is"** states plainly that
these are manufacturer blanks, that the photographs are the supplier's own of
that exact garment, and that there is no logo on it. Most stores hide this.
Saying it is what makes the specification credible — and it is the sentence that
would have prevented the 80 fabricated images.

## Verified

Rendered in Chromium at 1440px and 390px, light and dark, both pages. No
horizontal overflow at either width. Keyboard focus visible,
`prefers-reduced-motion` respected, no external fonts or images so nothing can
silently fail to load.

One real bug was caught this way: the product gallery blew out to 462px inside a
390px viewport — `min-width: auto` on a grid item letting an aspect-ratio'd tile
force the track wider than the screen. Fixed with `min-width: 0`, re-measured,
clean.

Untested against a live Shopify store — the Shopify connector was expired when
this was built, so the Liquid has not been run through a real render. Preview
before publishing.
