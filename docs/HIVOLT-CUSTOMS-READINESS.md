# HIVOLT-CUSTOMS-READINESS.md — 2026-08-28

Read-back across all variants of all 4 products:

| Field | Coverage | Consequence |
|---|---|---|
| `inventoryItem.countryCodeOfOrigin` | **0/70 variants** | Cannot make any origin claim; blocks EU/UK listings and duties estimation |
| `inventoryItem.harmonizedSystemCode` | **0/70 variants** | No duty calculation possible; blocks DDP anywhere |
| Weight | 68/70 have 0.2 kg (Elena); 3 products at 0 | International rate calculation would be wrong for 3 SKUs |
| Duties configuration | none | — |

Rules applied: **never claim "duties included"** (nothing proves it), and
**never invent customs estimates**. The store ships US-only today
(International market disabled), so customs is a P2 concern — but any
market activation is blocked on: supplier-documented origin per SKU, HS
codes (knitwear generally under HS 6110 — classify per garment, do not
bulk-guess), real weights, and a DDP/DDU decision by the owner.

Data source: AutoDS supplier listings + supplier documentation. Owner
action; no code can produce these facts.
