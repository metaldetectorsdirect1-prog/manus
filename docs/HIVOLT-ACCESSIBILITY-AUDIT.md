# HIVOLT-ACCESSIBILITY-AUDIT.md — 2026-08-28

Method: code inspection (dev theme). Rendered keyboard/screen-reader passes
require a browser — owner/preview task; not claimed here.

## Verified in code

- Skip link to #MainContent (layout) ✓
- `lang` attribute from request locale; `dir` from text_direction (RTL-capable root) ✓
- Custom sections: alt text on every image (falls back to label text);
  explicit width/height (CLS); native `<details>/<summary>` for PDP
  accordions (keyboard + SR semantics for free); labels are real text, not
  images ✓
- Focus styles: Impulse ships `--element-button-color-focus` /
  focus-visible handling ✓
- Tap targets: hero CTAs min 46px; nav 14px uppercase with padding ✓
- Reduced motion: V3 sections ship no autoplaying motion at all; Impulse
  exposes `data-disable-animations` ✓
- Contrast: obsidian #0A0A0B on white and white on obsidian both far exceed
  WCAG AA; muted grey #6D6D6D on white = ~4.6:1 (passes AA for normal
  text); hero white-on-photo relies on the 35–40% gradient overlay —
  **contrast over imagery must be judged in the screenshot review** |

## Open items (not verifiable from code alone)

- Drawer focus trapping and Escape behavior (Impulse-native — test in
  preview)
- Variant-button SR announcements on sold-out states
- Form error announcements (newsletter/contact)
- Full-page keyboard walk at 390px and 1440px

## Known risks

- Uppercase-everything headings (type_header_capitalize) can reduce
  readability for dyslexic readers — acceptable trade at current sizes
  (16px+ body, 34px+ headings), monitor in review.
- Category-strip horizontal scroll on mobile: native scroll (keyboard
  scrollable, no JS hijack) ✓.
