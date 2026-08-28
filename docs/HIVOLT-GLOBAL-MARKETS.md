# HIVOLT-GLOBAL-MARKETS.md — 2026-08-28

Fresh read-back: markets, currencies, locales, delivery profiles, wallets.

## Current state

| Item | Value |
|---|---|
| Active market | United States (primary; handle `united-states-and-canada`) |
| Disabled market | International (34075607272) — **do not enable without owner approval** |
| Presentment currencies | USD only |
| Locales | en (published) · **de (exists, unpublished)** |
| Wallets | Shop Pay · Apple Pay · Google Pay |
| Domains | hivolt-usa.com canonical |
| US shipping | FREE Tracked Shipping $0, General profile, US zone (verified) |
| Hazard | **"AutoDS Free Shipping" profile: Rest of World → $0** + Tapstitch per-country "Special Line" rates. If International is ever enabled without reviewing profiles, worldwide free shipping applies to AutoDS-profile products — a margin hazard. Review before any market activation. |
| Duties/taxes | US sales tax at checkout (config); no duties config, no HS codes, no origin data |

## Market matrix

| Market | Active? | Currency | Language | Pricing | Tax/Duty | Shipping | Payments | Returns | Localization | Ready? |
|---|---|---|---|---|---|---|---|---|---|---|
| USA | YES | USD | en | USD base | Sales tax ✓ / n/a | Free $0 ✓ | Shopify Payments + wallets | 60-day ✓ | native | **YES (only market)** |
| Canada | Partially in market handle | USD only | en | not localized | unconfigured | unreviewed | untested | policy says US-only | none | NO |
| UK | no | — | en | — | VAT/duty undefined | none reviewed | untested | — | none | NO |
| EU | no | — | de exists unpublished | — | VAT/OSS undefined | — | — | — | RTL n/a | NO |
| UAE / Saudi | no | — | ar not added | — | duty undefined | — | — | — | **RTL untested** | NO |
| Australia | no | — | en | — | GST undefined | — | — | — | none | NO |

## Architecture rules for expansion (no redesign required)

- Use Shopify-native Markets pricing/currency; **no JS converter** (none
  exists in the theme — verified; keep it that way).
- Theme is RTL-capable at the root (`dir="{{ settings.text_direction }}"`)
  but untested; full RTL QA required before any Arabic market.
- Shipping policy currently states US-only shipping — matches the enabled
  market. Any market activation requires: profile review (see hazard),
  policy rewrite, duties stance, localized sizing units.
- Translation pipeline: master English → machine assist → terminology check
  → human review → publish. No auto machine-translation publication.
