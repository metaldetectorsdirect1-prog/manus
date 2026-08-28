# HIVOLT — current state

**Operational source of truth for future sessions. Not a history.**

Queried: **2026-08-28T21:15Z**. Store `f36zps-yd.myshopify.com` / `hivolt-usa.com`.

**Cutover status:** MASTER r2 is certified READY and owner-authorized, but
`themePublish` is categorically blocked by the MCP connector ("must be done
manually in Shopify admin") — verified by an actual refused attempt at
21:15Z with roles re-verified unchanged afterwards. **The owner publishes
r2 manually**, then follows `docs/PRODUCTION-CUTOVER-PLAN.md`.

**Theme-admin activity 21:33–21:52Z (observed via role/updatedAt reads):**
the old MAIN was unpublished ~21:33:01, r2 was touched ~21:33:42 (briefly
published, most likely), IMPULSE-REBUILD ~21:35:58, and at **21:36:35 the
STOCK "Impulse" demo theme (`158743363816`) became MAIN — the live
storefront is running an uncustomized demo theme**. A fifth theme,
"Horizon" (`158882693352`), was added ~21:52 — the owner appears to be
actively exploring themes. r2 re-verified checksum-intact at 21:45Z (all 8
certified files identical); owner push-notified at 21:45Z naming the exact
theme to publish. The certified storefront remains one click away:
**Themes → "GENERAL STORE — MASTER r2 (approved image swaps)" → Publish.**
**Catalog at 21:15Z:** 819 products (344 ACTIVE, rest DRAFT), **0 published
to the Online Store channel** — the storefront still shows zero products.
Theme publication ≠ commerce launch: analytics NOT CONFIGURED, do not send
paid traffic.

> ## This file is a convenience, not an authority.
>
> It was written by a past session and goes stale the moment anything changes
> in Shopify. **Every session must re-query theme roles and product status
> before any write.** If this file disagrees with Shopify, Shopify is right and
> this file is wrong.

---

## Shopify themes

| Theme ID | Role now | Name (descriptive only) |
|---|---|---|
| `158753849576` | **`MAIN`** | "GENERAL STORE — IMPULSE MASTER CANDIDATE" — owner self-published 2026-08-28 15:41 UTC |
| `158874960104` | `UNPUBLISHED` | "GENERAL STORE — MASTER r2 (approved image swaps)" — the working candidate; carries image swaps, JSON-LD system, nav, favicon, hardened sticky ATC, honest page templates. Owner publishes r2 to ship. |
| `158743363816` | `UNPUBLISHED` | "Impulse" (stock) |
| `158753652968` | `UNPUBLISHED` | "IMPULSE-REBUILD-2026-08-24" |

The v3x/v7 HIVOLT theme line listed in earlier versions of this file no
longer exists on the store.

**The IDs and names in this table are informational only. Re-query roles before
writes.** A name records what a theme *is for*; only Shopify's `role` field
records what it currently *does*. See `CLAUDE.md`, *Shopify production-state
rule*.

### The two contradictory names were removed on 2026-08-22

Until then `158653808872` was named "HIVOLT v7 — **DRAFT**: PDP data layer (do
not publish)" while holding role `MAIN`, and `158482727144` was named "HIVOLT
v35 — **LIVE**" while holding role `UNPUBLISHED`. Both were renamed to
role-neutral descriptions in a metadata-only change: no file was written, no
role changed, and MAIN re-verified at 15/15 byte-identical afterwards.

**The rename proved its worth within the hour.** Both themes swapped roles again
at `12:29:08Z`, and neither name became a lie, because neither name makes a role
claim. Had the old names survived, the store would now have a theme called
"HIVOLT v35 — LIVE" that is live — accidentally correct — and one called "v7 —
DRAFT … do not publish" that is a draft, also accidentally correct. Both would
have been right by luck and wrong again on the next publish.

Note what this did **not** fix. The remaining names still carry imperatives —
"PUBLISH ME", "PUBLISH:" — on five themes nobody intends to publish. They are
weaker traps than a false role claim, but they are the same kind of mistake, so
they are recorded here rather than silently tolerated. **The guard does not read
names at all, which is why none of them can actually cause a wrong write.**

### The live theme changed again on 2026-08-22

**The roles swapped a second time at `2026-08-22T12:29:08Z`.** Both themes carry
that identical timestamp, which is the signature of a publish: v35 took `MAIN`
and v7 dropped to `UNPUBLISHED` in one operation.

Sequence so far:

| When | MAIN became | Carries the PDP data layer? |
|---|---|---|
| before 2026-08-21 | `158570021096` (v6) | no |
| `2026-08-21T04:11:02Z` | `158653808872` (v7) | **yes** |
| `2026-08-22T12:29:08Z` | `158482727144` (v35) | **no** |

**The PDP data layer is no longer on the live storefront.** v35 carries none of
the nine `hivolt-*` files; it is the 2026-08-14 returns-copy correction, and its
`templates/product.liquid` still checksums `4ca61e89…`, matching commit
`e560953`. So v35 is intact and doing what it was built for — it simply predates
the spec table, size guide, swatches and structured data.

Nothing customer-facing broke: H01 and both sibling polos are `DRAFT` and
published to zero sales channels, so no shopper could reach a PDP that depended
on those files either way.

Whether this was intentional is the owner's call, not a defect to fix. It is
recorded here rather than acted on.

While v7 held `MAIN`, its integrity was verified twice — after the 2026-08-21
publish and after the 2026-08-22 rename: **15/15 repo-owned files byte-identical
to `site/theme-v7/`** by `checksumMd5` both times. The rename moved the theme's
own `updatedAt` while every file timestamp stayed at `2026-08-20`, which is what
a metadata-only write looks like.

### Before a theme write

```
# 1. fetch with the MCP connector (no script can do this - no credentials,
#    and egress to the admin host is 403 at CONNECT)
#    query: themes(first: 25) { edges { node { id name role updatedAt } } }
# 2. adjudicate
python3 site/check-hivolt-theme-target.py --themes state.json --report
python3 site/check-hivolt-theme-target.py --themes state.json \
        --target <gid> --expect-role UNPUBLISHED
```

Exit 1 means refused. Do not work around a refusal.

---

## Catalog

| | |
|---|---|
| Active products | 20 (curated 2026-08-16; 114 archived, reversible) |
| HIVOLT polo drafts | 3, all `DRAFT`, none published to any channel |
| Orders, all time | **0** |
| Target product **H01** | `gid://shopify/Product/9603121774824` — `DRAFT` |

H01 publication state, verified 2026-08-22: `status DRAFT`, `publishedAt null`,
`onlineStoreUrl null`, `resourcePublicationsCount 0` across all 7 sales
channels. The theme going live did **not** expose it.

---

## H01 current real data

`HIVOLT Classic Cotton Polo — Men's Short Sleeve`, 20 variants, 6 colours × 5 sizes.

| Field | Value | Class |
|---|---|---|
| `spec.composition` | `100% Cotton` | **B** — supplier-stated, **needs physical label check before publish** |
| `spec.fit` | `Regular` | **B** — supplier-stated |
| `spec.size_chart` | `null` | no measurements exist |

All other `spec.*` fields are deliberately blank: `gsm`, `knit`, `collar`,
`placket`, `cuff`, `hem`, `finish`, `seams`, `opacity`, `care`, `origin`,
`benefits`, `model_height_cm`, `model_wears_size`. Reasons per field are in
`docs/HIVOLT-PRODUCT-DATA-PROVENANCE.md`. `hivolt_size_chart` metaobject count:
**0**.

> **A blank metafield is better than a polished lie.** Do not fill these in
> without evidence for this exact garment.

---

## Known unresolved issues

| # | Issue | State |
|---|---|---|
| 1 | **H01 Size option order is wrong** — `S → M → XL → XXL → L` | `productOptionsReorder` returns `userErrors: []` and writes nothing. **Do not retry it.** Needs a manual drag in the Shopify admin |
| 2 | **No garment measurements exist** | Supplier gives recommended body weight only. No size chart can be built. Request drafted: `docs/HIVOLT-POLO-MEASUREMENT-REQUEST.md` |
| 3 | **`100% Cotton` is unverified** | Supplier dropdown value, not a label reading. Fibre content is regulated (16 CFR Part 303). **Blocks publication** — see `docs/HIVOLT-H01-PUBLISH-GATE.md` |
| 4 | **Two detail images unreadable** | `hv-h01-detail-1.webp`, `hv-h01-detail-2.webp`. Every retrieval path denied by network policy; 7 attempts recorded |
| 5 | **Live policy contradictions unresolved** | 7 items awaiting owner decisions — `docs/HIVOLT-POLICY-CORRECTIONS.md` |
| 6 | **`/pages/fabric-weight-index` still live** with ~109 dead product links | Independent production incident, unrelated to the PDP work. Untouched |
| 7 | ~~Live theme name is misleading~~ | ✅ **RESOLVED 2026-08-22.** `158653808872` → "HIVOLT v7 — Production Baseline — PDP Data Layer"; `158482727144` → "HIVOLT v35 — Returns Copy Correction". Metadata only; roles and files untouched |

---

## Environment facts that shape what is possible

- Shopify is reachable **only** through the MCP connector. No credentials in the
  environment, no Admin API call in any script, egress to the admin host is 403
  at CONNECT. A standalone script cannot query Shopify.
- `site/build-theme.py` builds a local zip. It performs **no** network I/O and
  targets **no** theme ID. There is no automated deployer in this repo, and one
  must not be created casually.
- `site/theme/article.liquid` fails `parse-liquid.py` because python-liquid
  treats `offset` as reserved and Shopify Liquid does not. Harness limitation,
  not a defect. All 9 liquid files in `site/theme-v7/` parse cleanly.
