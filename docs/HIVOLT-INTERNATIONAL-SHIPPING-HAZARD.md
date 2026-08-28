# HIVOLT-INTERNATIONAL-SHIPPING-HAZARD.md — 2026-08-28

## HARD GATE: INTERNATIONAL ACTIVATION = BLOCKED

New confirming fact this session: **all four catalog products sit in the
"AutoDS Free Shipping" delivery profile** (gid://shopify/DeliveryProfile/
111055044840) — verified per-variant.

| Profile | Rate(s) | Countries | Fulfillment source | App | Applies to catalog? | Customer impact if International were enabled |
|---|---|---|---|---|---|---|
| AutoDS Free Shipping | "Free Shipping" **$0** | **Rest of World** (= every unzoned country incl. US) | AutoDS routing | AutoDS | **YES — all 4 products** | Worldwide $0 shipping on every order — full freight cost absorbed on every international sale |
| Tapstitch: Special Line | $3.76–$22.24 tiered | per-country zones (DZ, AR, AU, AT, BH, …) | Tapstitch POD | Tapstitch | No (no Tapstitch products in catalog) | n/a today |
| General profile | FREE Tracked Shipping $0 | US only | manual/default | — | **Not applied to these products** (profile membership wins) | — |

Interaction rule: a product's own profile fully replaces the general
profile. So today's US checkout for these products shows rate name
**"Free Shipping" $0** from the AutoDS profile — consistent with the free-
shipping promise; only the rate *name* differs from the General profile's.

Why nothing is broken today: the only enabled market is the United States,
so Rest-of-World pricing is unreachable by customers. The hazard is latent,
armed the moment International is enabled.

Recommended fix (OWNER APPROVAL REQUIRED — shipping configuration is
commerce-critical; not executed):
1. In the AutoDS profile, either delete the Rest-of-World zone or price it
   at real freight — decide per market, never blanket-$0.
2. Optionally rename its US-visible rate to "FREE Tracked Shipping" for
   naming consistency with policy language.
3. Keep International market disabled until every gate below passes.

## Gate conditions for INTERNATIONAL ACTIVATION (all required)

- [ ] All shipping profiles reviewed and priced per market (the $0
      Rest-of-World zone resolved)
- [ ] Country of origin + HS codes populated per SKU (currently 0/70)
- [ ] Real packaged weights (3/4 products at 0)
- [ ] Duties strategy decided (DDP vs DDU) and configured
- [ ] Return logistics for international parcels decided (policy currently
      US-only returns)
- [ ] Payments validated per market
- [ ] Shipping SLA verified with the actual fulfillment routes
- [ ] Policies rewritten for the market and mirrored in GMC

No shipping profile was modified. International remains disabled.
