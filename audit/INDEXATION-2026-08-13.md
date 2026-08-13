# Why the catalogue is not in Google — and the question it raises about a second HIVOLT

2026-08-13.

## First, the correction to the question

The store **is** indexed. 501 blog articles are in Google and they rank — one
of them is the top result for its own topic. What is not indexed is the part
that sells anything: **zero product pages and zero collection pages surface, in
five independent searches now**, across two days.

So the problem is not "the site isn't indexed." It is that Google has indexed
the 501 articles and not the 113 products.

Method note: this search tool does not reliably honour the `site:` operator —
`site:hivolt-usa.com/products` returned four unrelated companies called Hivolt.
A single empty result is not evidence, so the finding rests on five searches
using different phrasings, every one of which returned `/blogs/news/…` URLs
from the domain and nothing else.

## What is NOT the cause, verified rather than assumed

* **Not the theme.** `layout/theme.liquid` emits a canonical, Open Graph tags
  and Product JSON-LD on every page. The only `noindex` in the entire theme is
  on the Search Console verification page, which is correct — it is a token,
  not a destination.
* **Not publication state.** All 113 active products are published to the
  Online Store channel.
* **Not a penalty.** There is no evidence of one, and I am not going to invent
  one.

## The four plausible causes, most likely first

**1. Domain age and zero authority.** The domain is ~42 days old with
essentially no inbound links. Google indexes new low-authority sites slowly and
selectively. This alone explains a lot and needs no other mechanism.

**2. Crawl budget went to the blog.** 501 articles were published in a **1h54m
window** — roughly 4.4 per minute. A new domain gets a small crawl allowance,
and 501 URLs arriving at once absorb it. The products were competing with 501
newer, text-denser pages for the same budget, and lost.

*This is a correction of a correction, and the distinction matters.* I once
claimed "the blog is suppressing the domain," then withdrew it as a timeline
error. The withdrawal was right about **penalty** — there is no sign of one.
But crawl-budget dilution is a different mechanism entirely, and it fits the
evidence exactly: the thing that got crawled is the thing that flooded in.
Withdrawing the penalty claim should not have taken the budget question with
it.

**3. The brand name is contested, badly.** Searching *"HIVOLT activewear brand
official site"* returns **no hivolt-usa.com result at all**. What it returns
instead:

| domain | what it is |
|---|---|
| hivolt.de | German electronic components, Hamburg |
| hivoltcapacitors.com | high-voltage capacitors, founded 1967 |
| hivoltenergy.com | off-grid power generation, Midland TX |
| hivoltadvanced.com | electrical services |
| HiVolt Power I, LLC | Midland TX |
| **hivoltstore.com** | **"Hivolt Store", Chicago Ridge, Illinois** |

For a new store, its own brand name is normally the one query it owns
outright. Here it is being outranked by B2B firms with decades of authority.
That is why a customer who hears the name and searches it does not find the
shop.

**4. Nobody has read the report that would settle this.** Search Console's
**Indexing → Pages** distinguishes *Discovered – currently not indexed* (Google
knows the URL, has not crawled it — a budget/authority signal) from *Crawled –
currently not indexed* (crawled and judged not worth indexing — a quality
signal). Those two point at completely different fixes. The report has never
been read, and no amount of reasoning here substitutes for it.

## The thing worth chasing, stated as a hypothesis and not a finding

**hivoltstore.com is listed in Chicago Ridge, Illinois — about ten miles from
the Willowbrook address on this store's own contact policy.** Its published
contact is `Dnglobaltrading@gmail.com`.

I could not determine what it sells. The domain is blocked by this container's
egress proxy, and search did not expose its catalogue. **So this is a question,
not a conclusion.**

The reason it is worth asking: on 08-13 the owner pasted
`https://admin.shopify.com/store/hivolt-3`, which is a **different Shopify
store** from the `f36zps-yd.myshopify.com` this week's work targets. A second
Shopify store would have its own primary domain. If `hivolt-3`'s domain is
`hivoltstore.com`, then there are two HIVOLT storefronts, Google is surfacing
the other one, and they are competing for the same brand query — which would be
a far larger problem than crawl budget.

Both facts are known. The link between them is not. **Opening hivoltstore.com
in a browser answers it in about five seconds**, and that is the owner's to do.

## What would actually move it

In order of value, and only the first is fast:

1. **Read Indexing → Pages in Search Console.** It names the real reason.
   Everything above is inference; that report is evidence.
2. **Resolve the two-store question.** If the brand is split across two
   domains, nothing else in this list matters much.
3. **Submit `hivolt-usa.com/sitemap.xml`.** Does not force indexing, but it is
   how Google is told the 113 products exist as a set rather than discovered
   one link at a time.
4. **Get any inbound links at all.** Zero is the number that explains most of
   this, and it is the one nothing on the site can fix.

## The honest framing

Indexation is a **slow** channel. Even fully fixed, a 42-day-old domain earning
its first product rankings is a matter of months, not days. It is worth fixing
because it compounds, but **it is not the route to a first sale.** eBay has
buyers today and needs no authority, no crawl budget, and no brand recognition.
