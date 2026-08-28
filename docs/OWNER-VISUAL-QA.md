# OWNER-VISUAL-QA.md — review the dev theme

**Preview URL:** https://f36zps-yd.myshopify.com/?preview_theme_id=158753849576
(also: Shopify admin → Online Store → Themes → *Copy of Impulse* → Preview)

Send screenshots at **390px, 430px, 1440px** (browser devtools device mode).
Nothing else needed.

## 390px — check these
1. Hero: portrait campaign image (woman, cream cable knit, ivory studio) fills the first screen; headline "Made for the cold months" + one CTA readable at the bottom, not covering her face.
2. Header: compact; HIVOLT wordmark, menu, search, cart. Announcement bar shows the two true claims (free shipping / 60-day returns).
3. Scroll: brand statement → two full-width campaign tiles (Women / New in) → knit editorial with "Read the care guide" → ivory newsletter with the knitwear still-life → obsidian footer.
4. No product grid appears (catalog is draft — intentional). No horizontal scroll anywhere. No empty gaps.

## 430px — same page; verify nothing overflows and the hero crop still frames the model with the text-safe top third.

## 1440px — check these
1. Hero: wide 16:9 campaign, left-third negative space carrying the overlay text, ~78vh tall under the header.
2. Gateway tiles side-by-side at full width; editorial image right / text left; newsletter image right.
3. Nav: KNITWEAR · NEW IN · JOURNAL · ABOUT · HELP (uppercase, centered). Footer: three real menus + newsletter, payment icons, "Dn Global Trading LLC (trading as HIVOLT)".

## While you're in there (separate from screenshots)
- Image pixel QA: admin → Content → Files — check the active assets (campaign-hero desktop/mobile, dept-women, tile-new-in, campaign-editorial-desktop, hivolt-brand-editorial) for stray lettering, logos, bad hands. All statuses are OWNER VISUAL APPROVAL REQUIRED until you clear them.
- The four men's assets and master campaign are wired into DISABLED sections — visible only in the Theme Editor, one toggle each for later.
