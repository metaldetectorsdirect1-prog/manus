# GENERAL-STORE-OWNER-PACKAGE.md — numbered owner actions, 2026-08-28

Everything below is an owner action or an owner-eyes verification. Items
marked **REMOTE PREVIEW REQUIRED** cannot be verified from the build
environment (no rendered Shopify runtime here) and need your browser on the
candidate theme: **Shopify admin → Online Store → Themes → "GENERAL STORE —
IMPULSE V1 CANDIDATE" → Customize/Preview.** The 4 products are DRAFT, so
PDP items must be previewed inside the theme editor (select one of the 4
draft products in the template picker); the plain preview link 404s drafts.

Nothing here publishes anything. MAIN (`158753652968`) is untouched; the
candidate stays UNPUBLISHED; PR #2 stays open and unmerged.

1. **Review the 31-image contact sheet** (`docs/review/hivolt-v3-contact-sheet.html`,
   also delivered in chat). Approve / reject / replace / regenerate /
   inpaint by number. Approved today: 0/31. — *This is the single NEXT TASK
   (lowest score: Visual Approval 0/100).*
2. **Mobile sticky add-to-cart bar** — open a draft PDP in theme-editor
   preview on a phone-width viewport, scroll past the buy button, confirm
   the bar appears, mirrors price/sold-out truthfully, and adds to cart.
   **REMOTE PREVIEW REQUIRED**
3. **Desktop sticky purchase panel** — same PDP at desktop width: the info
   column should pin at ~100px while long image stacks scroll (needs a
   modern browser; degrades to non-sticky on old ones). **REMOTE PREVIEW
   REQUIRED**
4. **Homepage rhythm** — hero → strip → trending → campaigns → category
   strip → collage → newsletter on both widths. **REMOTE PREVIEW REQUIRED**
5. **Sale display truth check** — settings fixed this pass
   (`product_save_type: percentage`, `product_save_amount: true`). Today no
   product carries a compare-at price, so **no sale UI should appear
   anywhere**; if you ever see a badge without a genuine markdown, report
   it. **REMOTE PREVIEW REQUIRED**
6. **In-grid campaign tile (optional trial)** — Customize → collection
   template → main-collection → Add block → "Campaign tile". It renders only
   with an image/heading, only on page 1, never under filters; empty by
   default today. **REMOTE PREVIEW REQUIRED** (needs live products to see it
   inside a real grid)
7. **Mega menu activation recipe (when real collections exist)** — build the
   2–3-level menu under Navigation → main-menu (real destinations only),
   then Customize → Header → Add block → "Mega menu", set "Menu item" to the
   exact top-level link name; optional: collection images + up to 2 promo
   units per menu. The theme ships this natively — no code work pending. Do
   not add menu items for collections that do not exist.
8. **Paste the store policies** — procedure and verification phrases in
   `HIVOLT-POLICY-LAUNCH-CHECKLIST.md` (connector-blocked: `shopPolicyUpdate`).
9. **Unpublish the 11 confirmed-empty collections** — 2-minute admin action;
   list and read-back evidence in `HIVOLT-EMPTY-COLLECTION-AUDIT.md`
   (connector-blocked: `publishableUnpublish`).
10. **Delete the 9 orphaned GemPages files** in the code editor of the OLD
    theme — proof in `HIVOLT-PERFORMANCE-DEBT.md` (connector-blocked:
    `themeFilesDelete`). Zero runtime cost if you skip it.
11. **GA4** — create/connect a real property; the 18-event design in
    `HIVOLT-ANALYTICS-IMPLEMENTATION.md` stays blocked until then
    (**GA4 OWNER CONNECTION REQUIRED**).
12. **Send the supplier data request** (`HIVOLT-SUPPLIER-DATA-REQUEST.md`) —
    composition/care/origin/measurements enter the store from CLASS A/B
    sources only.
13. **Size-chart data entry** once supplier data arrives
    (`HIVOLT-SIZE-DATA-ENTRY.md`) — no fake measurements ever.
14. **Keep the International market DISABLED** until the AutoDS
    Rest-of-World $0 shipping hazard is fixed
    (`HIVOLT-INTERNATIONAL-SHIPPING-HAZARD.md`).
15. **AutoDS payment due 2026-08-30** — fulfillment stops if it lapses.
16. **Judge.me** — nothing to do: zero-state stays honest (stars hidden at 0
    reviews); never seed fake reviews.
17. **Lighthouse/PageSpeed run** on the candidate preview URL when you next
    preview — performance is disciplined in code but unmeasured.
    **REMOTE PREVIEW REQUIRED**

Publish-day sequence (when every gate above is green) remains
`HIVOLT-US-PUBLISH-RUNBOOK.md` — publish authority is yours alone.
