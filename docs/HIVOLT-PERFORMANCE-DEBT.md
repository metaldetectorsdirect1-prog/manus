# HIVOLT-PERFORMANCE-DEBT.md — 2026-08-28

From the dev-theme file inventory (250-file listing + layout read). No
files were deleted: several classifications need reference-proof that
requires the full template/page listing, and app infrastructure needs
owner approval.

| Asset | Size | Class | Evidence | Action |
|---|---|---|---|---|
| assets/theme.css | 777 KB | REQUIRED (Impulse core) | loaded by layout, preloaded | keep; no hand-editing of vendor CSS |
| assets/theme.css.liquid | 777 KB | DUPLICATE (build artifact pair) | .liquid source of the compiled asset — Impulse convention | keep (theme updates depend on it); zero runtime cost |
| assets/theme.js | 277 KB | REQUIRED | deferred | keep |
| assets/vendor-scripts-v11.js | 129 KB | REQUIRED | deferred | keep |
| assets/gp-global.css | 70 KB | LEGACY (GemPages) | loaded only by GemPages layouts, not by layout/theme.liquid | remove with GemPages decision (E) |
| layout/theme.gempages.*.liquid ×3 | ~45 KB | LEGACY (GemPages) | used only by pages assigned gp templates — none of the rebuilt templates use them; full page-template listing still required for proof | remove with Decision E after reference proof |
| sections/gp-variant-selected.liquid | 1 KB | LEGACY (GemPages) | same | same |
| assets/password-page-background.jpg | 1.45 MB | LEGACY | used by password page only (not the storefront path) | replace with small asset at next pass; zero shopper impact |
| assets/space.jpg / wave.svg / plants.svg / swirl.svg / marble.jpg / paper.jpg | ~750 KB total | UNUSED-LIKELY (Impulse demo textures) | not referenced by any rebuilt template; stock sections can reference them | verify references, then remove from workbench |
| country-flags.css/.png | 102 KB | REQUIRED-CONDITIONAL | loaded only when >1 currency — currently single-currency, so never loaded | keep (self-gating) |
| icon.* svgs | ~60 KB total | REQUIRED (sprite set) | referenced by stock sections | keep |
| Custom fashion-* sections | ~25 KB | REQUIRED | V3 system | keep |

Verified-good behaviors (no debt): JS deferred; fonts via
Shopify CDN with preconnect; custom sections use dimensioned responsive
images, hero eager+fetchpriority, everything below the fold lazy;
`{% style %}` blocks are per-section and small; no render-blocking
third-party scripts; no app pixel bloat (none installed).

Core Web Vitals targets (LCP <2.5s / INP <200ms / CLS <0.1): plausible
with this profile; measurable only on the rendered preview/live —
owner-side Lighthouse run at stage 15 of the publish runbook.

Cleanup rule applied: theme-local deletions only after proving zero
references; GemPages removal is app infrastructure → Decision E.

## Decision E execution record — 2026-08-28

Reference proof completed (full 2-page file inventory + template-suffix
read across all pages/collections/products):

| GemPages file | Class | Evidence |
|---|---|---|
| assets/gp-global.css (70KB) | UNREFERENCED | loaded only by gempages layouts; theme.liquid clean |
| layout/theme.gempages.{blank,footer,header}.liquid (~45KB) | UNREFERENCED | no template declares a gempages layout; no resource uses a gp template suffix |
| snippets/gp-head.liquid | UNREFERENCED | rendered only by gempages layouts |
| sections/gp-variant-selected.liquid | UNREFERENCED | referenced only by gp templates |
| templates/{collection,index,product}.gp-template-bk-default.json (~19KB) | UNREFERENCED | zero pages/collections/products carry suffix "gp-template-bk-default" (fresh read) |

Total: 9 files, ~135KB of theme residue.

**Deletion: BLOCKED BY CONNECTOR.** `themeFilesDelete` is refused by the
MCP server safety policy (all theme deletion operations blocked). No
workaround attempted. Owner action (~2 min): Online Store → Themes →
Copy of Impulse → Edit code → delete the 9 files listed.

Honesty note on impact: unreferenced theme files add **zero runtime page
weight** — Shopify serves assets on demand. This cleanup is theme hygiene
and editor clarity, not page speed. The password background and demo
textures likewise cost shoppers nothing while unreferenced; they remain
retained pending the same owner cleanup. Real page-speed posture is
governed by the verified-good behaviors above and can only be measured on
rendered pixels (owner Lighthouse at publish runbook stage 15).
