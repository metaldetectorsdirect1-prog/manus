# HIVOLT storefront

**Live preview:** https://claude.ai/code/artifact/2457c34e-d06c-46a2-af97-a73b28a7a22b

## Files

| File | What it is |
|---|---|
| `index.html` | The design, as a standalone page. Open it in a browser. |
| `index.liquid` | Shopify homepage template. Replaces `templates/index.liquid`. |
| `theme-hivolt.css` | Stylesheet. Goes in `assets/` as `hivolt.css`. |
| `shot-*.png` | Rendered screenshots (desktop light, desktop dark, mobile). |

## Installing on Shopify

1. Online Store → Themes → **Duplicate** your live theme first. Never edit the live one.
2. On the duplicate: Edit code → `assets/` → **Add a new asset** → upload `theme-hivolt.css`,
   renaming it `hivolt.css`.
3. In `layout/theme.liquid`, before `</head>`:
   ```liquid
   {{ 'hivolt.css' | asset_url | stylesheet_tag }}
   ```
4. Replace the contents of `templates/index.liquid` with `index.liquid`.
5. **Preview before publishing.** Check one product page on a phone.

## The two metafields

The catalogue tiles show fabric weight and composition when these exist.
Settings → Custom data → Products → Add definition:

| Namespace & key | Type | Example |
|---|---|---|
| `spec.gsm` | Integer | `220` |
| `spec.composition` | Single line text | `75% nylon / 25% spandex` |

Where a product has no `spec.gsm`, the badge is omitted rather than guessed.
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

## Verified

Rendered in Chromium at 1440px and 390px, light and dark. No horizontal overflow
at either width. Keyboard focus visible, `prefers-reduced-motion` respected, no
external fonts or images so nothing can silently fail to load.

Untested against a live Shopify store — the Shopify connector was expired when
this was built, so the Liquid has not been run through a real render. Preview
before publishing.
