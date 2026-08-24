# REVIEW-SYSTEM.md

Status of §1. **The capture mechanism cannot be installed by this integration.**

---

## What was asked, and what is actually possible

| Asked | Status |
|---|---|
| Review capture installed and wired | 🔴 **Owner-side.** See below |
| Verified-buyer-only submission | 🔴 Owner-side — it is an **app setting**, not a theme setting |
| Honest empty state | 🟠 Deferred — see §4, building it without a backend is a shell |
| Post-purchase request flow | 🔴 Owner-side — app feature |
| `AggregateRating` suppressed until real reviews exist | ✅ **Verified. Nothing emits it.** |
| Zero seeded reviews | ✅ Zero reviews exist, because no review system exists |

## §1 Why installation is owner-side

Three independent facts:

1. **`appInstallations` is denied to this connector.** Queried again 2026-08-24 — `access denied`. That is the seventh consecutive session it has been refused. I cannot enumerate installed apps, let alone install one.
2. **App installation is an OAuth grant.** It happens in the Shopify admin, by a human with the merchant account. There is no Admin API mutation that installs an app.
3. **Shopify's own Product Reviews app was sunset.** There is no first-party review product to enable. Every option is a third-party install.

There is no path from here to an installed review app. Reporting it as buildable would be false.

## §2 `AggregateRating` — verified absent, method stated

Read every file in the product rendering path and every file that can emit markup into `<head>`:

| File | JSON-LD emitted |
|---|---|
| `sections/main-product.liquid` | none — delegates to the snippet |
| `snippets/product-template.liquid` (26,851 b, read in full) | **none.** No `<script type="application/ld+json">` at all |
| `layout/theme.liquid` (15,319 b, read in full) | none |
| `snippets/social-meta-tags.liquid` | OG and Twitter meta only |
| `sections/faq.liquid` | `FAQPage` only |

**Conclusion: the theme emits no `Product`, no `Offer`, no `availability`, and no `AggregateRating` anywhere.** There is nothing to suppress — the requirement is already satisfied, and now it is documented so a future session does not assume otherwise.

`snippets/structured-data.liquid` was added this session and emits `Organization` only. Its comment header records `aggregateRating` and `sameAs` as **deliberate absences** with the reason, so re-adding either is a conscious act rather than an oversight.

## §3 Verified-buyer enforcement — what the owner must confirm

This is the load-bearing setting, and in every major review app it is a **toggle, not a plan tier**:

| App | Setting | Notes |
|---|---|---|
| Judge.me | "Verified buyers only" on the review form | Free plan includes it |
| Okendo | Review request tokens are order-scoped | Enforced by design |
| Loox | Verified-purchase-only submission | Paid plans |
| Yotpo | Verified-buyer badge + restrict submission | Setting |

**The question to answer at install time is precise:** *can a review be created by anyone who is not attached to a real order?* In most apps the default is **no restriction** — an open review form. That default is the exact failure mode this store already has history with.

**Paths by which an unverified review could still be created, which must each be closed:**

1. **Open web review form** — the app default in several products. Must be set to verified-buyer-only.
2. **Manual review entry in the app admin** — a human can type a review. Cannot be disabled in most apps; it is a process control, not a setting.
3. **CSV / supplier review import** — the mechanism by which dropship stores acquire fake reviews wholesale. Must never be run.
4. **Theme-side hardcoded testimonials** — how this store's five fabricated reviews were shipped. They were in a theme file, not a review app, so **no review app setting would have prevented them.** Only the `sections/testimonials.liquid` section being unused prevents a repeat.

Point 4 is the important one: the original incident bypassed review infrastructure entirely. `sections/testimonials.liquid` still exists in this theme and is referenced by no template on the dev theme — but it remains available in the theme editor.

## §4 Why no empty-state UI was built

An empty state is the visible part of a system whose invisible part is the submission and verification flow. Building the visible half against no backend produces a section that says reviews will appear, on a store where nothing can produce one. That is a claim about capability.

It is also currently unrenderable: with zero products there is no product page to place it on.

**Copy is specified and ready** for the moment an app is installed:

> This piece is new. Reviews appear here once verified buyers leave them.

Design: body face, `--element-text-font-size--body-sm`, `color_body_text` at full opacity on `color_body_bg`, no star outlines, no placeholder avatars, no "be the first" prompt — a prompt implies a submission route that does not yet exist.

## §5 Live theme status — unchanged, owner-side

`158743363816` (MAIN) still carries in `templates/product.json` and `templates/collection.json`:

- five fabricated testimonials (Leslie M./Toronto, Rachel F./LA, Sam R./Brooklyn, Sharon S./New Orleans, Matt C./Montreal)
- an "Organic cotton" sales point
- a "Save on Select Styles / extra 10% off — limited time" banner

Live-theme file writes are blocked at the connector. With zero products these render on templates nobody can reach, so the exposure is latent rather than active. **Removal is owner-side.**
