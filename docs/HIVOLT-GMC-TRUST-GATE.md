# HIVOLT-GMC-TRUST-GATE.md — misrepresentation defense, 2026-08-28

GMC 5838274874 is verified; verification is not misrep clearance, and the
appeal budget is assumed exhausted (3/3). **No feed syncs until every row
below passes.** Per the playbook the first feed sync is the
misrepresentation trigger — it happens once, clean.

## Consistency gate (all must match, sentence-level)

| Check | Passes when | Current |
|---|---|---|
| Website ↔ policies | theme claims = /policies/* text | ❌ until owner pastes the 4 bodies (live 8-14 window contradicts 2–6/10–15 claims) |
| Policies ↔ GMC settings | shipping + returns settings mirror the policy promises word-for-word | ❌ blocked on the paste |
| Product price ↔ feed | Shopify price = feed price, USD both ends | ✓ structurally (single currency) |
| Availability ↔ feed | in_stock only for sellable variants | ✓ structurally (tracked inventory, DENY oversell) |
| No fake discounts | no compare-at unless a real prior price existed | ✓ (bogus 0.00 cleared; no sale claimed anywhere) |
| Currency | USD only, everywhere | ✓ |
| Business identity | GMC business info = Dn Global Trading LLC (trading as HIVOLT), Willowbrook IL = policies = footer | Verify in GMC UI (owner) |
| Contact path | visible email/phone/contact page on site | ✓ on dev theme |
| Product claims | every feed/PDP claim traceable (CLASS A/B) | ❌ "extrafine merino" and cardigan composition await supplier confirmation |
| Dead links | zero 404s from any customer-visible surface | dev ✓ / live footer ❌ (two golf links — see EMPTY-COLLECTION-AUDIT) |
| Return window | one number everywhere: 60 days | ✓ in theme + drafts; live refund body agrees on 60 |
| Delivery window | one pair everywhere: 2–6 US-warehouse / 10–15 international | ❌ until paste |

## Per-product feed data package

| Attribute | Elena | Nora | Ivy | Cardigan |
|---|---|---|---|---|
| brand (HIVOLT) | READY | READY | READY | READY |
| title | READY | READY | READY | READY |
| description | READY (unique lede recommended) | READY | READY | READY |
| google category (via taxonomy) | READY (Sweaters) | READY | READY | READY (Cardigans) |
| gender | MISSING (set `female` — factual) | MISSING | MISSING | MISSING |
| age_group | MISSING (set `adult`) | MISSING | MISSING | MISSING |
| color | READY (names need base-color mapping) | READY | READY | READY |
| size | READY (casing normalize in feed) | READY | READY | READY |
| material | NEEDS VERIFICATION (merino claim) | MISSING | MISSING | NEEDS VERIFICATION (listing composition) |
| pattern | NOT APPLICABLE | NA | NA | NA |
| item_group_id | READY (native) | READY | READY | READY |
| GTIN | NEEDS VERIFICATION (barcode present, unproven) | NEEDS VERIFICATION | NEEDS VERIFICATION | NEEDS VERIFICATION |
| MPN | MISSING (may not exist) | MISSING | MISSING | MISSING |
| price / availability / condition | READY | READY | READY | READY |
| shipping (US $0) | READY after GMC mirror | — | — | — |
| return policy (60d) | READY after GMC mirror | — | — | — |

Identifier rule: if GTIN verification fails → `identifier_mode = none` +
`mm-google-shopping.custom_product = TRUE`; **never send an unverified
barcode as gtin, never invent an MPN.**

## Sync preconditions (ordered)

1. Policy paste + GMC mirror (owner)
2. gender/age_group populated (safe once ratified — factual values)
3. Material/GTIN verification or explicit none-stance
4. Products published (owner authorization)
5. Live dead-link fixes approved
6. Simprosys connected as the single feed owner (never in parallel with the
   Google & YouTube channel feed — one feed source only; note: three empty
   activewear collections are still published to the Google & YouTube
   channel and should be unpublished before feed work)
