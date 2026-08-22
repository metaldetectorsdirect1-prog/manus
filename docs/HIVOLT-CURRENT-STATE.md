# HIVOLT — current state

**Operational source of truth for future sessions. Not a history.**

Queried: **2026-08-22**. Store `f36zps-yd.myshopify.com` / `hivolt-usa.com`.

> ## This file is a convenience, not an authority.
>
> It was written by a past session and goes stale the moment anything changes
> in Shopify. **Every session must re-query theme roles and product status
> before any write.** If this file disagrees with Shopify, Shopify is right and
> this file is wrong.

---

## Shopify themes

| Theme ID | Role now | Name (stale — ignore it) |
|---|---|---|
| `158653808872` | **`MAIN` — LIVE** | "HIVOLT v7 — DRAFT: PDP data layer (do not publish)" |
| `158570021096` | `UNPUBLISHED` | "HIVOLT v6 — PUBLISH ME: logo in header" |
| `158482727144` | `UNPUBLISHED` | "HIVOLT v35 — **LIVE** (returns copy fixed)" |
| `158563467496` | `UNPUBLISHED` | "HIVOLT v37 — PUBLISH: 15% two-item upsell" |
| `158568906984` | `UNPUBLISHED` | "HIVOLT v5 — PUBLISH ME: favicon + full footer" |
| `158347559144` | `UNPUBLISHED` | "HIVOLT v30 — product schema. PUBLISH ME" |
| `158001037544` | `UNPUBLISHED` | "Impulse" |
| `158568546536` | `UNPUBLISHED` | "Copy of Impulse" |

**The IDs in this table are informational only. Re-query roles before writes.**

Two names in that table are the opposite of the truth: `158653808872` says
DRAFT and is live; `158482727144` says LIVE and is not. **Theme role must never
be inferred from an ID or a name** — see `CLAUDE.md`, *Shopify production-state
rule*.

The role swap happened `2026-08-21T04:11:02Z`, when the owner published v7.
Live theme integrity was verified afterwards: **15/15 repo-owned files
byte-identical to `site/theme-v7/`** by `checksumMd5`. No drift.

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
| 7 | **Live theme name is misleading** | `158653808872` is named "DRAFT … do not publish" but is `MAIN`. Renaming is safe and cosmetic; not done without instruction |

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
