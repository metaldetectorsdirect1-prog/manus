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

## 2. Theme role — verify immediately before every write

Never infer role from a theme ID or name. Query `themes { role }` and confirm the
target is `UNPUBLISHED` in the same session as the write. As of 2026-08-24:

| Theme | Role |
|---|---|
| `158743363816` Impulse | **MAIN** |
| `158753652968` IMPULSE-REBUILD-2026-08-24 | UNPUBLISHED ← build target |
| `158753849576` Copy of Impulse | UNPUBLISHED |

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
