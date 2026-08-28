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

## Component test matrix (P0 pass, code-level; rendered checks = OWNER VISUAL QA REQUIRED)

| Component | Keyboard path | Focus state | Label/role/name | Contrast target | Escape / focus return | Tap size | Code verdict |
|---|---|---|---|---|---|---|---|
| Header | native links | theme focus-visible | text links ✓ | ink on white ✓ | n/a | 14px links + padding | PASS (code) |
| Mobile menu (drawer) | Impulse drawer-menu.liquid | theme | nav semantics | ✓ | Impulse-managed — **verify in preview** | ✓ | OWNER QA |
| Hero (fashion-hero) | CTAs are real anchors when present; none today | theme | img alt ✓, decorative overlay aria-hidden ✓ | white on 35–40% gradient — **verify on pixels** | n/a | 46px CTA | PASS (code) + OWNER QA (contrast) |
| Collection filter | S&D form (collection-grid-filters-form) | theme | labeled inputs | ✓ | drawer behavior — verify | ✓ | OWNER QA |
| Product card | anchor-wrapped | theme | alt = product title | ✓ | n/a | full-card target | PASS (code) |
| Quick Add | Impulse quick-shop | theme | button + modal | ✓ | modal focus trap — verify | ✓ | OWNER QA |
| PDP variants | button-type picker (real buttons) | theme | variant labels on ✓ | ✓ | n/a | button pads | PASS (code) |
| PDP details (fashion-pdp-info) | native `<details>` — Enter/Space toggles | browser-native | `<summary>` accessible name ✓, dl/dt/dd semantics ✓ | #6D6D6D dt ≈4.6:1 AA ✓ | native | 44px+ summary rows | PASS (code) |
| Size guide | not rendered (no data) — blank-safe | — | — | — | — | — | N/A until charts exist |
| Cart drawer | Impulse cart-drawer | theme | dialog semantics | ✓ | Impulse-managed — verify | ✓ | OWNER QA |
| Search (predictive) | Impulse predictive-search | theme | combobox pattern — verify announcements | ✓ | Esc closes — verify | ✓ | OWNER QA |
| Newsletter | native form + label | theme | email input labeled (Impulse) | ink on #F7F7F5 ✓ | n/a | ✓ | PASS (code) |
| Footer | native links on obsidian | theme | text links | white on #0A0A0B ✓ | n/a | ✓ | PASS (code) |
| Category strip (custom) | native horizontal scroll (keyboard-scrollable), links only when set | theme | img alt + text labels ✓ | ✓ | n/a | 38vw tiles | PASS (code) |

## Known risks

- Uppercase-everything headings (type_header_capitalize) can reduce
  readability for dyslexic readers — acceptable trade at current sizes
  (16px+ body, 34px+ headings), monitor in review.
- Category-strip horizontal scroll on mobile: native scroll (keyboard
  scrollable, no JS hijack) ✓.
