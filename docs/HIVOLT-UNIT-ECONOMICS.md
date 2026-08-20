# HIVOLT — Unit Economics

## Status: baseline invalidated

The measured baseline in `audit/FIVE-HUNDRED-K-2026-08-12.md` was computed
against the catalogue that was **deleted on 2026-08-19**. It is retained as
method, not as current fact.

What it established, and what carries forward:

| Metric (old catalogue, 541 variants) | Value |
|---|---|
| Catalogue-weighted gross margin | 65.7% |
| Avg price / cost / gross profit | $46.90 / $16.08 / $30.82 |
| Variants priced below cost | 0 |
| Contribution after COGS + $7 ship + 2.9%+30¢ | 47.2% at 1 item, 55.0% at 2 items |
| Breakeven ROAS | 2.12 (1 item) → 1.82 (2 items) |

**The method is the asset:** every variant carried `inventoryItem.unitCost`,
which is what made margin scoreable at all. That practice must continue on the
polo catalogue — it is the difference between a measurable business and a guess.

## The contribution equation

```
Revenue
  − discounts
  − returns/refunds
  − COGS
  − inbound freight
  − outbound fulfilment
  − payment processing (2.9% + $0.30 US; higher cross-border)
  − platform + app fees
  − advertising
  − affiliate/influencer commissions
  = CONTRIBUTION PROFIT
```

Revenue is never reported as profit.

## Polo-specific factors not present in the old model

| Factor | Why it differs for polos | Data needed |
|---|---|---|
| Cross-border payment fees | UK/EU cards cost more than domestic US | Processor schedule |
| Duties / VAT | DDP absorbs into COGS; DAP pushes to customer and raises refusal rate | Fulfilment model |
| Return rate by size | Polos are fit-sensitive; sizing quality directly moves contribution | Post-launch data |
| Multi-unit AOV | A polo customer can own many — the strongest AOV lever available | Bundle test results |

## Required inputs — OWNER

1. Landed cost per polo SKU (unit + inbound freight)
2. Target retail band and margin floor
3. Fulfilment cost per order by zone
4. Processor rates (domestic and cross-border)
5. Expected return rate assumption for launch modelling

Until 1–5 exist, contribution cannot be modelled honestly and no ROAS floor
should be quoted.
