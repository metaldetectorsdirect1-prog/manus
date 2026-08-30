# HIVOLT — Internationalization

Verified against Shopify Admin API, 2026-08-20.

## Current state — the blocking fact

```
Market "United States"  → enabled: true,  regions: [US]           ← only this sells
Market "International"  → enabled: false, regions: [GB FR IT ES NL BE CH IE
                                                   PL PT CZ SE NO DK FI CA AU …]
```

**Canada (Tier 1) and every Tier 2 European market are inside the disabled
market.** Nothing outside the United States can transact today.

Both markets report `webPresence: null` — no locale root URLs, no
country-specific domains or subfolders. `localCurrencies: true` is set on both,
so once a market is enabled Shopify handles presentment currency natively; no
frontend conversion should ever be built (§32).

## The ordering that matters

Enabling the market alone produces a **worse** experience, not a better one:

1. `General profile` (which new products join by default) has exactly one
   shipping zone — **United States** — with one rate, *FREE Tracked Shipping
   (8–14 business days)*, $0.00.
2. A German shopper in an enabled market reaches checkout and receives
   **"no shipping rates available"**.
3. That is a hard blocker, after they have entered an address — the most
   expensive possible place to fail.

So the sequence is: **shipping rates → then enable market → then currency/tax
review → then localized content.** Not the reverse.

A second profile, `Tapstitch: Special Line`, *does* carry international zones
with real rates (Austria $8.96–11.43, Belgium $8.83–11.36, Canada $4.66–7.74,
Bulgaria $11.94–14.97, Australia $3.76–6.04 …). It belongs to the previous POD
supplier and has no products attached since the catalogue deletion. Those rates
are a **reference for magnitude, not a source of truth** for a new polo
fulfilment partner.

## What is required, by owner

| # | Requirement | Why it blocks | Owner / Claude |
|---|---|---|---|
| 1 | Fulfilment partner for polos — origin country, carrier, cost and transit per zone | Cannot invent delivery times or rates (§36) | **OWNER** |
| 2 | Duties model: DDP or DAP for UK/EU | "No duties" may not be promised unless the model guarantees it (§37) | **OWNER** |
| 3 | UK/EU VAT registration status | Determines tax-inclusive pricing display | **OWNER / LEGAL** |
| 4 | EU/UK returns policy | 14-day statutory withdrawal ≠ current 60-day US promise | **OWNER / LEGAL** |
| 5 | Shipping zones + rates built in Shopify | Once (1) is known | Claude (config) |
| 6 | Market enablement + CAD/GBP/EUR presentment | After (5) | Claude (config) |
| 7 | Country selector in theme | After (6) | Claude (code) |
| 8 | Cookie consent for EU traffic | Before any EU paid traffic | Claude (code) + **LEGAL** review |

## Currency plan (once markets are live)

| Market | Presentment | Notes |
|---|---|---|
| US | USD | Primary, base currency |
| Canada | CAD | Tier 1 — currently unreachable |
| UK | GBP | VAT-inclusive display expected |
| Eurozone (DE FR IT ES NL BE AT IE PT FI) | EUR | Do **not** show EUR to non-euro countries |
| Switzerland | CHF | Only if business/platform setup allows |
| Sweden / Norway / Denmark / Poland / Czechia | SEK NOK DKK PLN CZK | Local currency — never default these to EUR |

## Localization

Translation-ready architecture only. **Do not machine-translate and publish.**
Priority order when content is commissioned: German, French, Spanish, Italian,
Dutch. hreflang, canonical and localized metadata are implemented **only for
locales that have genuine translated content** — never to manufacture thin
pages (§35).
