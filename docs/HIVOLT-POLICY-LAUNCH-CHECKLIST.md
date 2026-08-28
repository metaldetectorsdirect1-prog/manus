# HIVOLT-POLICY-LAUNCH-CHECKLIST.md — 2026-08-28

Live policy bodies were re-read in full this session. **All four still carry
the ruled-out claims.** The corrected bodies exist in
`impulse-rebuild/policies/` and were never applied (`shopPolicyUpdate`
denied: `write_legal_policies` scope). No policy mutation was executed.

## Per-policy state

| Policy | Source file | Current Shopify status (verbatim findings) | Theme links to it | GMC expectation | Contradictions | Owner action |
|---|---|---|---|---|---|---|
| Refund / Return | `impulse-rebuild/policies/refund.html` | OLD: "5-7 business days", "reply within one business day with a prepaid return label", "within 30 days of delivery with photographs", "Order Cancellations… within 12 hours… enter production", bare "HIVOLT" entity | Announcement a1, PDP tab & info module, footer | Returns settings must state 60-day window / free label / no restocking fee, word-for-word | Refund timing (5-7 vs confirmed 5 + 5-10 bank), label SLA (1 vs 2 business days), unsourced 30-day/12-hour clauses, missing legal entity | Paste corrected body |
| Shipping | `impulse-rebuild/policies/shipping.html` | OLD: "2-4 business days" dispatch, "8-14 business days" delivery, "Why the Window Is Not Two Days", "USPS or UPS", "tracking within 24 hours", "no PO Boxes", "Wrong Address 12 hours… production", "dispatched from Illinois" | Announcement a0, brand strip, PDP tab & info module | Shipping settings must mirror: free US, supplier-grounded 2–6 / 10–15 windows | **Live 8-14 window vs theme/product claims of 2–6 US / 10–15 intl** — a live contradiction shoppers can see today on the dev preview; every unsourced operational claim above | Paste corrected body |
| Terms | `impulse-rebuild/policies/terms.html` | OLD: "single member limited liability company", "technical activewear and gym apparel: tops, bottoms, sports bras…", g/m² publication promise, "2-4/8-14" repeated, per-page size-guide promise | Footer (via /policies/terms-of-service) | Business identity consistent with GMC | Wrong category (activewear vs women's clothing), wrong entity presentation, dead promises | Paste corrected body |
| Contact information | `impulse-rebuild/policies/contact.html` | OLD: "a person will answer", "Within one business day", hours block, "dispatched from Illinois", "2-4 / 8-14" repeated, bare "HIVOLT" entity | Footer contact column context | Contact path consistent | Unsourced SLAs; entity | Paste corrected body |
| Privacy | — none (deliberate) | Shopify template with Liquid variables — correct, no HIVOLT-authored claims | Newsletter, footer | — | none | **Do not touch** |

## OWNER PROCEDURE — ~5 minutes total (do not execute via connector)

For each row: **Shopify Admin → Settings → Policies**, open the named
editor, select ALL existing text, delete it, paste the ENTIRE contents of
the named file (open the file, Ctrl/Cmd-A, Ctrl/Cmd-C — paste with
formatting), then **Save**.

1. **Refund policy** ← paste whole of `impulse-rebuild/policies/refund.html` → Save → verify: page shows "5 business days" + "further 5-10 days" and "within 2 business days" label promise; the words "5-7", "30 days", "12 hours", "production" must no longer appear.
2. **Shipping policy** ← `impulse-rebuild/policies/shipping.html` → Save → verify: "2–6 business days" / "10–15 business days" windows present; "8-14", "2-4", "PO Boxes", "USPS or UPS", "24 hours", "12 hours" gone.
3. **Terms of service** ← `impulse-rebuild/policies/terms.html` → Save → verify: §1 says women's clothing and "Dn Global Trading LLC (trading as HIVOLT)"; "activewear", "single member", "g/m²" promise gone.
4. **Contact information** ← `impulse-rebuild/policies/contact.html` → Save → verify: entity correct; "one business day", "a person will answer", "2-4", "8-14" gone.
5. Verification for all: open `/policies/refund-policy`, `/policies/shipping-policy`, `/policies/terms-of-service` on the storefront and reload.

**Then mirror into GMC (same sitting, word-for-word promises):**
Merchant Center → Settings:
- *Shipping* service: United States, cost $0, handling + transit consistent with "2–6 business days (US-warehouse items)" — do not enter a faster window than the policy.
- *Returns*: 60 days from delivery, free return shipping, no restocking fee.
The commercial promise in GMC and on `/policies/*` must be the same
sentence-level facts; any mismatch is misrepresentation fuel.

## Theme-claim consistency scan (dev theme sources, this session)

| Claim | Source file | Wording | Policy source | Match? | Risk |
|---|---|---|---|---|---|
| Free tracked shipping / no minimum | header-group.json (a0) | "Free tracked shipping — On every US order, no minimum" | shipping.html + $0 rate (CONFIG) | ✓ vs draft; live policy also says free | none |
| 60-day returns / free label / no restocking | header-group.json (a1), fashion-strip, PDP tab, pdp-info | consistent phrasing | refund.html (OWNER) | ✓ | none until paste (live policy agrees on 60-day/free/no-fee) |
| Delivery windows 2–6 US / 10–15 intl | product.json tab + implied | "2–6 business days… 10–15 business days" | shipping.html (SUPPLIER-grounded) | ✓ vs draft; **✗ vs LIVE policy (8-14)** | HIGH until paste |
| No restocking fees | fashion-strip | "No restocking fees" | refund.html | ✓ (live agrees) | none |
| Secure checkout wallets | fashion-pdp-info | "Shop Pay · Apple Pay · Google Pay" | paymentSettings (CONFIG) | ✓ | none |
| Newsletter promise | index.json | "New drops, restocks and HIVOLT edits" + privacy link | owner-supplied copy | ✓ | none |
| Copyright entity | footer-group.json | "Dn Global Trading LLC (trading as HIVOLT)" | brand block (OWNER) | ✓; live policies still show bare "HIVOLT" | fixed by paste |
| Duties/taxes | pdp/policies | no duty claims anywhere in theme | US-only market | ✓ | none |
| Guarantees/urgency | all theme sources | none present | — | ✓ | none |

Zero material contradictions **inside the dev theme**. The only material
contradiction is live-policy-vs-everything — resolved entirely by the paste.

Checkout rate-name note: the 4 products sit in the "AutoDS Free Shipping"
profile, so checkout shows the rate name **"Free Shipping"** at $0 (not the
General profile's "FREE Tracked Shipping"). $0 matches every claim; AutoDS
supplies tracking numbers, so "tracked" remains true. No contradiction, but
the owner may want the AutoDS profile's rate renamed for consistency
(global change — listed in the approval package).
