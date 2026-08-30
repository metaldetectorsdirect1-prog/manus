# HIVOLT - Unit Economics

> **Every input below is an ASSUMPTION and is editable.** None is HIVOLT
> observed data. Replace each with a real figure as it becomes known; the
> conclusions change with them.

## Editable assumptions

| Input | Value | Status |
|---|---|---|
| Blended discount rate | 5% | ASSUMPTION |
| Landed COGS as % of retail | 22% | ASSUMPTION - no supplier quote exists |
| Pick/pack per order | $2.00 | ASSUMPTION |
| Outbound shipping subsidy per order | $7.00 | ASSUMPTION - store promises free US shipping |
| Payment processing | 2.9% + $0.30 | Shopify Payments US published rate |
| Returns/refunds allowance | 8% of net revenue | ASSUMPTION |
| Other variable (packaging/insert) | $0.50 | ASSUMPTION |

## Formulas

```
Net revenue          = Revenue - Discounts
Contribution BEFORE  = Net revenue - COGS - Pick/pack - Shipping subsidy
  acquisition          - Payment processing - Returns allowance - Other variable
Contribution AFTER   = Contribution BEFORE acquisition - CAC
  acquisition
Contribution margin  = Contribution AFTER acquisition / Revenue
  AFTER acquisition

BREAK-EVEN CAC       = Contribution BEFORE acquisition
                       (the CAC at which post-acquisition contribution = $0)
MAX CAC at margin M  = Contribution BEFORE acquisition - (M x Revenue)
```

## Single unit - full line-item P&L

| Line | $59 | $69 | $79 | $89 | $99 |
|---|---|---|---|---|---|
| 1. Revenue | $59.00 | $69.00 | $79.00 | $89.00 | $99.00 |
| 2. Discounts | -$2.95 | -$3.45 | -$3.95 | -$4.45 | -$4.95 |
|    = Net revenue | $56.05 | $65.55 | $75.05 | $84.55 | $94.05 |
| 3. Product landed COGS | -$12.98 | -$15.18 | -$17.38 | -$19.58 | -$21.78 |
| 4. Pick/pack | -$2.00 | -$2.00 | -$2.00 | -$2.00 | -$2.00 |
| 5. Outbound shipping subsidy | -$7.00 | -$7.00 | -$7.00 | -$7.00 | -$7.00 |
| 6. Payment processing | -$1.93 | -$2.20 | -$2.48 | -$2.75 | -$3.03 |
| 7. Returns/refunds allowance | -$4.48 | -$5.24 | -$6.00 | -$6.76 | -$7.52 |
| 8. Other variable | -$0.50 | -$0.50 | -$0.50 | -$0.50 | -$0.50 |
| **9. Contribution BEFORE acquisition** | $27.16 | $33.43 | $39.69 | $45.95 | $52.22 |
| **Contribution rate before acq.** | 46.0% | 48.4% | 50.2% | 51.6% | 52.7% |

## CAC ceilings - single unit

| Retail | BREAK-EVEN CAC | Max CAC @10% | @15% | @20% | @25% |
|---|---|---|---|---|---|
| $59 | $27.16 | $21.26 | $18.31 | $15.36 | $12.41 |
| $69 | $33.43 | $26.53 | $23.08 | $19.63 | $16.18 |
| $79 | $39.69 | $31.79 | $27.84 | $23.89 | $19.94 |
| $89 | $45.95 | $37.05 | $32.60 | $28.15 | $23.70 |
| $99 | $52.22 | $42.32 | $37.37 | $32.42 | $27.47 |

**Break-even CAC is the maximum spend at which the order contributes $0.**
Any CAC above it loses money on that order. The margin columns show what
is left for acquisition once a post-acquisition contribution target is held back.

## Two units per order - the AOV lever

| Retail x2 | Order value | Contribution BEFORE acq. | BREAK-EVEN CAC | Max CAC @10% | @15% | @20% | @25% |
|---|---|---|---|---|---|---|---|
| $59 x2 | $118.00 | $64.12 | $64.12 | $52.32 | $46.42 | $40.52 | $34.62 |
| $69 x2 | $138.00 | $76.65 | $76.65 | $62.85 | $55.95 | $49.05 | $42.15 |
| $79 x2 | $158.00 | $89.18 | $89.18 | $73.38 | $65.48 | $57.58 | $49.68 |
| $89 x2 | $178.00 | $101.71 | $101.71 | $83.91 | $75.01 | $66.11 | $57.21 |
| $99 x2 | $198.00 | $114.24 | $114.24 | $94.44 | $84.54 | $74.64 | $64.74 |

Fixed per-order costs (pick/pack, shipping subsidy, payment fixed fee, packaging)
are absorbed once rather than twice, so break-even CAC rises faster than order
value. **This is the arithmetic case for bundles**, independent of any benchmark.

## External benchmarks - clearly separated

| Benchmark | Value | Source class | Status for HIVOLT |
|---|---|---|---|
| Apparel CAC on paid social | commonly cited $25-60 | **EXTERNAL BENCHMARK** | **Not a HIVOLT fact.** No HIVOLT acquisition data exists. |
| Apparel CVR | commonly cited 1.5-3.0% | **EXTERNAL BENCHMARK** | Not a HIVOLT fact. |
| Apparel return rate | commonly cited 8-30% | **EXTERNAL BENCHMARK** | The 8% assumption above is the optimistic end. |

**HIVOLT observed data: none yet (0 orders).** The moment real CAC, CVR and
return figures exist, they replace every benchmark above and override any
external guidance.

## How to read this without over-claiming

At $69 single-unit under these assumptions, break-even CAC is about
$33.43 and CAC at a 20% post-acquisition margin target is about
$19.63. Whether that is viable depends entirely on HIVOLT's
actual CAC, which is unknown. The external benchmark suggests it would be
difficult; **that benchmark is not evidence about HIVOLT** and must be tested
with real spend before any conclusion is drawn.

## Inputs that would replace assumptions

| Input | Replaces | Source |
|---|---|---|
| Supplier quote | COGS rate | Supplier |
| 3PL/fulfilment quote | Pick/pack, shipping | Fulfilment partner |
| Processor schedule | Payment rates (incl. cross-border) | Payment provider |
| First 100 orders | Return rate, AOV, units/order | HIVOLT data |
| First ad spend | CAC by channel | HIVOLT data |