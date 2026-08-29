# REVENUE-PLAN-500K.md — 2026-08-28

Target: **$500,000 in sales.** This is the honest path, the arithmetic
behind it, and what is currently blocking it. Every number comes from
live Shopify data pulled this session, not estimates.

---

## 1. Where the store actually stands

| Fact | Value |
|---|---|
| Orders, all time | **0** |
| Products live right now | **0** (879 total, all DRAFT) |
| Shopify plan | Advanced (~$399/mo already burning) |
| Checkout | Functional — US free tracked shipping, SSL, USD |
| Sales channels installed | Online Store, Google & YouTube, Meta, TikTok, Shop |
| Homepage | Still serving the rejected six-torso category tile |

The store can take money. Nothing is sending anyone to it. $500k is not
blocked by a missing feature — it is blocked by having no traffic engine
and, more urgently, by the cost data being wrong (§3).

## 2. What $500k actually requires

Revenue = sessions × conversion rate × AOV. There is no fourth lever.

At a realistic 2% conversion rate:

| AOV | Orders for $500k | Sessions needed |
|---:|---:|---:|
| $50 | 10,000 | 500,000 |
| $70 | 7,143 | 357,000 |
| **$100** | **5,000** | **250,000** |
| $130 | 3,846 | 192,000 |

Paid traffic at a ~$30 cost per acquisition is the only way to buy
250,000+ sessions on this timeline. So every product must survive a $30
CPA **and** payment fees (~3%) **and** a refund reserve (~4%).

### The measured reality (sample of 200 live-candidate products)

| Metric | Value |
|---|---:|
| Median retail | $69.95 |
| Median tagged COGS | $23.11 |
| Median gross margin | $43.97 |
| Median retail/cost multiple | **2.86×** |
| **Median contribution after $30 CPA + fees** | **$8.96** |
| Products that clear a $30 CPA solo | 142 / 200 (71%) |
| GREEN (≥3.5×) / YELLOW / **RED (<2.5×)** | 76 / 42 / **82** |

**$8.96 per order does not build a business.** At that contribution,
$500k of revenue produces roughly $64k of gross contribution against
~$214k of ad spend — a blended ROAS near 2.3, below the 2.5–3.0 band a
store needs to survive returns, chargebacks and overhead.

**41% of the catalogue loses money on paid traffic.** The worst are not
marginal, they are inverted:

| Product | Multiple | Contribution per order |
|---|---:|---:|
| Willa Half Zip Ribbed Knit Pullover | 1.12× | **−$28.19** |
| Chic Kitten Heel Pointed Ankle Boots | 1.14× | −$26.69 |
| Vera Cashmere Blend Crewneck Sweater | 1.22× | −$23.89 |
| Serena Pleated Midi Dress with Belt | 1.22× | −$23.89 |

Advertising those at scale converts ad budget into losses, faster the
better they perform.

## 3. THE BLOCKER: the cost data is corrupted

This is the finding that invalidates the profitability model.

**Four different coats share one Amazon ASIN and one $2.99 cost:**

| Product | Retail | Tagged COGS | Source |
|---|---:|---:|---|
| Sienna Military Wool Coat | $99.95 | $2.99 | `src-amazon-B081YTSN4N` |
| Harper Faux Leather Trench Coat | $94.95 | $2.99 | `src-amazon-B081YTSN4N` |
| Evelyn Short Trench Jacket | $79.95 | $2.99 | `src-amazon-B081YTSN4N` |
| Luna Hooded Waterproof Trench Coat | $89.95 | $2.99 | `src-amazon-B081YTSN4N` |

A wool coat does not cost $2.99, and four distinct garments do not share
one ASIN. These are mis-mapped supplier matches. They also happen to be
the **top-ranked products by apparent margin** (20×–33×), which means any
launch that trusts this data will pour spend into the products whose
economics are the most wrong.

Every "winner" in the current catalogue needs its cost re-verified
against the actual supplier listing before a dollar of ad spend follows
it.

**Second risk in the same data:** a large share of the catalogue is
sourced `src-amazon-*`. Buying from Amazon retail to fulfil customer
orders violates Amazon's policies, delivers parcels in Amazon packaging
to your customers, and exposes you to price and stock changes you do not
control. This is not a viable fulfilment base for a $500k run.

## 4. The sequence that actually gets to $500k

**Phase 0 — Fix the foundation (this week, no ad spend)**
1. Re-verify COGS on the top 100 products against real supplier listings;
   delete or re-source anything that cannot be verified.
2. Replace Amazon-retail sourcing with AliExpress/CJ/US-warehouse
   suppliers that permit dropship fulfilment.
3. Zero or untrack the 1,000-unit phantom inventory on every product.
4. Publish MASTER r2 so the homepage stops serving the rejected image.

**Phase 1 — Launch small and clean (weeks 1–4)**
5. Take **40–60 products** live, not 800: only verified-cost, ≥3.5×,
   ≥$35 contribution items. Google Merchant Center approves small clean
   catalogues far more readily than large messy ones.
6. Claim the GMC domain, connect the feed, trigger and clear the
   misrepresentation review on a €5/day campaign while the store is small.
7. Install GA4 + conversion tracking before the first click is bought.

**Phase 2 — The freeze (weeks 5–8)**
8. After GMC approval: change nothing for 4 weeks. Keep ads live at
   minimum spend. This is the step that protects the asset.

**Phase 3 — Scale (months 3–12)**
9. Raise AOV to $100+: lead with the $80–130 outerwear anchors, attach
   $25–45 accessories. AOV is the profit line, not product count.
10. Import 50/week from the verified backlog.
11. Hand ads to a media buyer at ~10% of spend once spend justifies it.

### What $500k looks like when the economics are fixed

| Lever | Target |
|---|---:|
| AOV | $100 |
| Blended gross margin | 68% |
| Gross profit per order | $68 |
| CPA | $30 |
| **Contribution per order** | **~$33** |
| Orders for $500k | 5,000 |
| Total ad spend | ~$150k |
| **Gross contribution** | **~$165k** |
| Realistic timeline | **9–12 months**, ramping ~$25k/mo to ~$80k/mo |

## 5. Honest expectations

- $500k is achievable in 9–12 months with roughly $150k of ad spend and
  disciplined economics. It is not achievable this quarter, and it is not
  achievable at all on the current cost data.
- The binding constraints are, in order: **verified supplier costs**,
  **GMC approval**, **AOV**, then product count. Adding more products to
  an unverified catalogue moves none of them.
- Two automated processes are currently writing to this catalogue at the
  same time (879 products, changing by the hour). Sequence the work or
  they will keep overwriting each other.
