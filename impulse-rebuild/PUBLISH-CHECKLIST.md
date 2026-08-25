# PUBLISH-CHECKLIST.md

Pre-publish checks for dev theme `158753652968`. The owner publishes; this build
does not. Run every check below **before** any publish or any page publish.

---

## 🔴 1. Redirect ↔ page handle collisions — check before publishing ANY page

A Shopify URL redirect fires **only on a 404**. Three handles currently have
*both* a live redirect and a real (unpublished) page. Publishing the page makes
the redirect **silently stop firing**. No error, no warning, no log line.

| Page handle | Redirect currently fires | Target | On publish |
|---|:--:|---|---|
| `size-chart` | ✅ | `/pages/size-guide` | redirect dies silently |
| `fabric-weight-index` | ✅ | `/pages/materials-sustainability` | redirect dies silently |
| `voltcore` | ✅ | `/pages/about-us` | redirect dies silently |

**This will bite when the size guides return with real measurements.** Someone
publishes `size-chart`, and inbound links that had been resolving to `size-guide`
for months start landing on a different page. The cause is invisible from the
page editor.

**Check:** before publishing any page, query
`urlRedirects(query: "path:/pages/<handle>")`. If a redirect exists, decide
deliberately: delete the redirect, or leave the page unpublished.

The same mechanic applies in reverse and is **useful**: 85 dead product and
collection URLs now redirect to `/pages/about-us`. When the catalog lands and a
real product occupies that handle, the redirect stops firing on its own. That is
self-healing and intentional — do not delete those redirects preemptively.

---

## 🔴 2. THE ROLES SWAPPED. `158753652968` IS NOW LIVE.

**Read this before any theme write. The build target became production on
2026-08-25T01:37Z.** The owner published it.

| Theme | Role as of 2026-08-25 | Was |
|---|---|---|
| `158753652968` IMPULSE-REBUILD-2026-08-24 | **MAIN — LIVE** | UNPUBLISHED |
| `158743363816` Impulse | UNPUBLISHED | MAIN |
| `158753849576` Copy of Impulse | UNPUBLISHED | UNPUBLISHED |

**Every prior session's standing instruction said "dev theme `158753652968`
only, no live-theme writes." That instruction is now self-contradictory —
`158753652968` IS the live theme.** Following it literally would write straight
to production.

Consequences, all of them live now:

- A write to `158753652968` is a **production modification** and needs explicit
  authorization for one. The connector also blocks `themeFilesUpsert` against
  MAIN, so it will be refused at the tool layer regardless.
- The homepage, header, footer, 404, cart, About and Help Center built on
  2026-08-24 are **live**.
- **The three known live-theme defects came off with the swap.** The five
  fabricated testimonials, the "Organic cotton" sales point and the "extra 10%
  off" banner were in `158743363816`'s `product.json` / `collection.json`. That
  theme is now unpublished, and the newly-live theme's own `product.json`
  (2,148 b) and `collection.json` (1,448 b) were read in full and contain none
  of them.
- **Collection pages now render live with zero products.** No menu links to
  them, so they are reachable only by direct URL or search — but analytics
  recorded real sessions on `/collections/leggings`, `/collections/tops` and
  others. This is the "empty collection is worse than a 404" problem, now on
  the live storefront. It resolves only by importing the catalogue.

**This is the third role swap in this engagement.** It is exactly why role is
read live and never inferred from a theme's ID, name, or a prior session's note.

### Theme role — verify immediately before every write

Never infer role from a theme ID or name. Query `themes { role }` in the same
session as the write.

---

## 3. Live theme still carries defects — owner-side removal

`158743363816` (MAIN) still has, in `templates/product.json` and
`templates/collection.json`:

- **Five fabricated testimonials** (Leslie M./Toronto, Rachel F./LA, Sam R./Brooklyn, Sharon S./New Orleans, Matt C./Montreal)
- **"Organic cotton"** sales point
- **"Save on Select Styles / extra 10% off — limited time"** banner

Live-theme writes are blocked at the connector. With zero products these render
on templates nobody can reach, so the exposure is latent — but it is still there.

---

## 4. Blocked, do not attempt

| Item | Reason |
|---|---|
| Shop policies | `write_legal_policies` denied. Corrected bodies in `policies/` for the owner to paste. |
| Logo | Light-ground lockup must come from the owner. `logo: ""` stays. Do not generate a wordmark. |
| Live theme file writes | Blocked at connector. |

---

## 5. Before publishing the theme

- [ ] Catalog imported — four homepage slots still absent by design (see `CHANGELOG.md` for insert positions)
- [ ] Navigation wired to populated collections, never empty ones
- [ ] Shop policies pasted by owner
- [ ] Light-ground logo lockup supplied and set
- [ ] Size guides re-published only after the collision check in §1
- [ ] `/pages/shipping-delivery` — still unpublished; no menu references it
