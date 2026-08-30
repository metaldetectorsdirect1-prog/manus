# "Why is SEO not working?"

2026-08-12. It is working. It is 42 days old, and most of the traffic being
measured belongs to somebody else's business.

## The store is 42 days old and the content is 12

`shop.createdAt` is 2026-07-01. The 501 activewear articles went live 07-30.
A domain with no backlinks and no brand searches takes 6–12 months to compound.
Judging it at day 12 is judging it before it has run.

## The blog is indexed and ranking

32 search sessions in 30 days, spread across **25+ different articles**, 1–3
clicks each. That is not failure — it is the exact signature of a new site
sitting around position 30–80 on long-tail queries and catching a stray click.
Nothing is blocked, nothing is deindexed, nothing needs fixing. It needs time
and links.

## Most of the traffic is a previous business's

This Shopify store previously sold pheromone perfume (Roxelis / Auria),
collagen peptides, and children's math games (Focus Foxes), in German and
English. That demand is still arriving. Over 60 days:

| Source | Where it actually landed |
|---|---|
| Facebook, 387 sessions | **213 → `/products/roxelis-pheromone-roll-on`**, 33 → Focus Foxes math games, 10 → collagen. Only **66** → the Voltcore set. |
| Search | `/collections/damen`, `/collections/herren`, `/pages/ueber-uns`, `/pages/widerrufsbelehrung`, `/products/auria-pheromone-roll-on` |
| Search, blog | 9 deleted perfume articles still ranking — musk, sillage, "what does Roxelis perfume smell like", "do pheromone perfumes work" |

These people want perfume and math games. They will never buy leggings. It is a
large part of why the session count looks non-trivial while orders stay at zero,
and it is not a conversion problem — it is the wrong audience arriving.

Search sessions by week: 6, 2, **52, 51**, 14, 36, 5. The peak is mid-July —
**before the activewear blog existed**. So the peak was never our content, and
the decline is not a penalty against it. It is the old catalogue's residual
demand decaying, exactly as it should.

Strip it out and genuine activewear-intent traffic is a handful of sessions a
day. That is the same finding as the funnel diagnosis, arrived at from a
different direction: almost nobody who wants activewear is arriving.

## What was fixed

Eight dead URLs that Google still ranks now redirect to their real equivalent
instead of 404ing:

`/pages/contact` → contact-us · `/pages/ueber-uns` → about-us ·
`/pages/widerrufsbelehrung` → returns-refunds · `/pages/impressum` → contact-us ·
`/pages/versand-lieferung` → shipping-delivery · `/pages/about-focus-foxes` →
about-us · `/about` → about-us · `/collections/best-sellers` → all

`/pages/fit-quiz` was refused — the handle is still owned, so it is not a 404.

## What was deliberately not fixed

**The nine perfume articles keep 404ing.** Redirecting "what is sillage in
perfume" to an activewear page is a mismatch Google reads as a soft 404, and it
would pull in more of the exact visitor that is already failing to convert. A
404 tells Google the content is gone and to drop the URL, which is what should
happen. Twelve sessions over 60 days is not worth buying that signal.

## The three Google channels are all blocked owner-side

* **Merchant Center — hivolt-usa.com is not claimed or verified, and shipping is
  not configured.** Every one of the 113 offers is held until both are done, so
  Shopping serves nothing. Feed data is complete and the channel is installed
  and syncing. This is the single highest-value item outstanding and the fastest
  route to buyers who are actively searching to purchase.
* **Search Console is not verified** — `/google6945ed5c46bc40d8.html` 301s to a
  themed page and Google's file method will not follow a redirect. No sitemap
  submission, no indexation data.
* **The TikTok bio link is still not set**, so twelve live films cannot send
  anyone anywhere.

## The bottom line

SEO is the slowest channel available and it is running correctly. It will not
produce the first sale this month. Merchant Center verification plus shipping
config is the fastest realistic path, and the gateway itself has still never
been exercised — no card has ever been charged on this store.
