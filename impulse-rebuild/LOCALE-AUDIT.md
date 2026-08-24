# LOCALE-AUDIT.md

Established 2026-08-24. **Nothing was changed.**

## Headline: there is no GDPR exposure, because there is no EU personal data

This was the question that mattered most. It resolves cleanly.

| Fact | Value |
|---|---|
| Orders, all time | **0** |
| Draft orders | 0 |
| Customers | **2** |
| Customer 1 | United States — Austin, Texas. `DISABLED`, `NOT_SUBSCRIBED` |
| Customer 2 | **No address recorded at all.** `DISABLED`, `NOT_SUBSCRIBED` |
| Abandoned checkouts | 2 — the same two customers; one US billing address, one with none |
| EU customer records | **none** |
| EU orders fulfilled | **none — no order has ever been placed** |

**No EU order was ever fulfilled. No EU address is stored. No EU customer exists.**

The Privacy page therefore carries **no retention obligation, no data-subject
backlog, and no deletion requests** arising from past trading. GDPR still applies
prospectively to EU *visitors* — cookies, analytics, and the German pages below
draw real German traffic — but that is standard forward-looking compliance, not
remediation of a live breach. This is the difference between a compliance
section and a compliance incident, and it is the former.

## The German locale is configured but unpublished

| Locale | Primary | Published |
|---|:--:|:--:|
| English (`en`) | ✅ | ✅ |
| **German (`de`)** | ✗ | **✗ not published** |

Both markets:

| Market | Enabled | Regions |
|---|:--:|---|
| United States | ✅ primary | US only |
| International | ✗ **disabled** | ~71 countries |

Neither market has a configured `webPresence`, so there is no active
domain-or-subfolder routing for `de`.

## But German URLs still drew traffic

| Path | Sessions / 90d |
|---|---:|
| `/de/blogs/news/jump-rope-workouts-from-first-skip-to-10-minute-rounds` | 5 |
| `/collections/damen` | 7 |
| `/collections/herren` | 5 |

**Reconciling the two:** the locale is unpublished *now*; these are sessions from
the last 90 days against paths that were live earlier in that window, plus search
engines still holding the URLs. Shopify's analytics records the **requested**
path, so a request that now 404s or redirects still appears here.

**What this means for the prune:** the German article corpus is **not a live
mirror** requiring parallel maintenance. `de` is unpublished, so `/de/*` is not
being served from a translation set today. The redirect map does **not** need a
full second locale arm — but `/de/blogs/news/*` should still be covered for the
handful of paths search engines retain.

**Confidence: medium.** I could not fetch a URL to see what `/de/...` actually
returns — storefront egress is 403 at CONNECT. The conclusion rests on
`shopLocales.published = false` plus the absence of a market web presence, which
is strong but not the same as observing the response.

## 🔴 331 redirects already exist — and they reveal six prior businesses

`urlRedirectsCount: 331`. A sample:

| Path | Target | Business |
|---|---|---|
| `/products/hivolt-collagen-peptides` | `/collections/all` | supplements |
| `/products/auria-pheromone-roll-on` | `/collections/all` | perfume |
| `/products/auralux-wake-silent-alarm-watch` | `/collections/all` | **watches** |
| `/products/auralux-vault-anti-theft-sling-bag` | `/collections/all` | **bags** |
| `/products/hilvolt-vault-anti-theft-sling-bag` | `/collections/all` | bags |
| `/collections/wake-up-better` | `/collections/all` | watches |
| `/collections/carry-smarter` | `/collections/all` | bags |
| `/pages/100-day-wake-up-guarantee` | `/pages/60-day-love-it-guarantee` | — |
| `/pages/30-day-risk-free-guarantee` | `/pages/60-day-love-it-guarantee` | — |

Three consequences:

1. **At least six businesses have run on this Shopify store**: apparel (HIVOLT),
   perfume (Roxelis / Auria), children's games (Focus Foxes), supplements
   (HIVOLT Collagen), watches (Auralux), bags (Auralux / Hilvolt Vault).
2. **A redirect discipline already exists.** 331 redirects is a real
   infrastructure, and the convention is `→ /collections/all`. The blog prune
   should follow the established pattern rather than invent one.
3. **The guarantee has been republished at three different lengths** — 100-day,
   30-day, now 60-day. Both older versions redirect to the current one. Worth
   knowing before touching guarantee copy: this commitment has moved before.

## Verdict on the blocked items

| Question | Answer |
|---|---|
| Does the prune need a two-locale redirect map? | **No full second arm.** `de` is unpublished. Cover `/de/blogs/news/*` for retained search paths only |
| Does Privacy carry real GDPR obligations? | **Prospective only.** No EU data exists to remediate. Section still required for EU visitors |
| Is `/collections/damen` a real collection? | Not in the 15 catalogued. It draws traffic, so it is either redirect-covered by one of the 331 or a 404. **Not verifiable without storefront access** |

## What I could not establish

- Whether `/de/...` currently returns 200, 301, or 404 — no storefront egress.
- Whether German translations exist as `translatableContent` — not queried;
  `shopLocales.published = false` made it moot for the blocking questions.
- Whether any of the 331 redirects already cover blog paths — only 10 sampled.
  **The full 331 must be pulled before the prune's redirect map is built**, or
  it will duplicate or conflict with existing entries.
