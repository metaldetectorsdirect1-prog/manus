# The policies landed — and they contradict the storefront

2026-08-11T04:45Z. First owner-gated item to move in twenty-five check-ins.

All four policies have been replaced. The supplement business is gone from
every one of them:

| Policy | Was | Now |
|---|---|---|
| REFUND | "We stand behind the quality of HIVOLT Collagen Peptides", 90-day, customer pays return shipping | "HIVOLT Return & Refund Policy — 60-Day Love-It Guarantee", free prepaid label, no restocking fee |
| TERMS §1 | "HIVOLT sells dietary supplement products" | "We sell technical activewear… We do not sell supplements, food, or any ingestible product" |
| TERMS §3 | subscriptions | §7 is now "No Subscriptions — HIVOLT sells one-time purchases only" |
| CONTACT | wrong Addison address | Willowbrook, IL 60527 |
| SHIPPING | — | free tracked US, 2–4 dispatch, 8–14 delivery, Willowbrook |

Internally consistent: 60 days, free return shipping, 8–14 business days and
the Willowbrook address agree across all four. PRIVACY is still Shopify's
default template, which is fine — it was never one of the four.

## But it is not the text in `audit/policies/`

The prepared file opens:

> 60-Day Love-It Guarantee. You have 60 days from delivery to return any item,
> **including items you have worn and washed.**

What went live says the opposite:

> Items must be **unworn** and returned with the original tags attached. Trying
> a garment on is fine. **Training in it, washing it, or removing the tags
> places it outside the window.**

That is the owner's call to make and a perfectly normal apparel policy. The
problem is that the store had already been built on the other one, and the
marketing is still making the promise the policy now denies.

## Where the contradiction is live

| Surface | Claim | Status |
|---|---|---|
| **TikTok `returns` film** | "Sixty days. **Worn and washed.** … Train in them. Wash them. **Send them back.** Free prepaid US label. No restocking fee." | **Published, public, cannot be edited** — only deleted |
| `product.liquid:195` | "Return — 60 days, **including worn and washed**." | On **every product page** |
| `page.returns.liquid` | "Worn and washed is fine", three times, **plus FAQPage JSON-LD** asserting it | A whole page, and structured data Google reads |
| `page.voltcore.liquid` ×2 | "60-day returns, and you can have trained in it." | #2 landing page |
| Voltcore product description | "60-day returns — and you can have trained in it." | **Fixed** — now "60 days to return it, unworn with tags" |

Only the last one was live product *data* rather than theme, so it is the only
one this container could correct. It now reads "Free US shipping. 60 days to
return it, unworn with tags — see our Return & Refund Policy."

The rest are theme files. `MAIN` is v32 and writes to the live theme are
blocked, so aligning them means editing `site/` and publishing — which is the
same owner action already outstanding for v33.

## Why this matters more than a copy mismatch

A published promise the binding policy denies is not a stale number. The
`returns` film is a live advertisement telling people they can train in the
garment and send it back; the refund policy linked from checkout says doing
exactly that voids the return. Whichever way it gets resolved, it should not
stay open — a customer who buys on the film's promise and is refused under the
policy has a legitimate complaint, and the FAQ JSON-LD on the returns page
publishes the same claim in a format Google reads and may surface.

Two ways to close it, and it is a commercial decision rather than a technical
one:

1. **Keep the strict policy** (industry-normal, lower return costs). Then the
   theme copy has to come down to match on all four surfaces, and the `returns`
   film should be deleted from TikTok.
2. **Restore the worn-and-washed policy** from `audit/policies/refund-policy.html`.
   Then nothing else has to change, the film stays up, and the differentiator
   survives — it was one of the few things the store said that no competitor
   was saying.

Worth noting which way the evidence points: worn-and-washed returns were the
single most concrete trust claim in the catalogue, on a store with no reviews,
no order history and a checkout that has never been exercised. But it is also
the more expensive promise, and nobody has tested how expensive.
