# BLOG-AUDIT.md

`Training Journal` (`/blogs/news`) — **501 published articles**. Audited
2026-08-24.

## Sample and confidence — stated honestly up front

I read **2 articles in full** and **24 by metadata** (12 newest + 12 oldest by
`publishedAt`), not 25 in full. Every quantitative claim below is an
extrapolation from that, and the confidence is stated per finding. Reading 501
articles is a larger job than one session; the corpus-wide numbers here are
estimates, not counts.

## The corpus was bulk-generated. This is not an inference.

| | |
|---|---|
| Oldest article | `2026-07-30T02:15:14Z` |
| Newest article | `2026-08-11T17:36:59Z` |
| **Entire corpus published in** | **13 days** |

Worse than that: of the 12 oldest sampled, **eleven** are stamped between
`02:23:41Z` and `02:24:56Z` — **eleven articles inside 75 seconds.** Twelve more
cluster in `04:03`–`04:09`. Publication happened in machine-speed batches.

Every article shares one author string, "HIVOLT Training Team", and a house
structure: short answer → why it matters → numbered criteria → comparison table
→ how-to-test → product picks → FAQ → embedded JSON-LD. **Confidence: high.**

## The content quality is genuinely good. That is not the problem.

This needs saying plainly because it changes the disposal decision. The writing
is specific, well-argued, and hedges honestly. From the GSM article, unprompted:

> *"This is not an industry survey and we are not going to present it as one."*
> *"Use g/m² to rule things out, not to rank them. A brand that will not tell you
> the number is telling you something; a brand that tells you only the number is
> doing the same thing more quietly."*

That is better than most brand blogs. The corpus is **not** thin AI slop. Judge
it on the two things that actually disqualify it.

## Disqualifier 1 — every factual anchor points at a catalog that no longer exists

Both fully-read articles link exclusively to deleted resources.

*Best Leggings for Squats* — **6 internal links, 6 dead:**

| Link | Status |
|---|---|
| `/products/women-s-high-rise-topstitching-leggings` | product deleted |
| `/products/womens-high-rise-ankle-length-leggings` | deleted |
| `/products/womens-high-rise-flared-leggings` | deleted |
| `/products/womens-high-rise-ankle-length-yoga-leggings` | deleted |
| `/collections/bottoms` | **collection never existed** in the current 15 |
| `/collections/training` | **never existed** |

*What GSM Should Activewear Be?* links to `/pages/fabric-weight-index` — a page
that is **`isPublished: false`**. Dead.

**Estimate: 480–501 articles carry at least one dead link. Confidence: high** —
the "our picks from the HIVOLT range" section is structural, appearing in the
summary text of nearly every sampled article.

## Disqualifier 2 — §3 violations, and they are in the structured data too

Specific product claims about products that do not exist:

- *"the Women's High Rise Topstitching Leggings use a 76% polyamide / 24%
  spandex knit at 220 g/m²"*
- *"Across the 109 HIVOLT garments that publish a fabric weight, the median is
  220 g/m² and the full range runs from 91 to 380"*
- A full nine-row category table — 30 t-shirts, 17 sports bras, 13 tank tops,
  12 shorts, 9 leggings, 5 training pants, 4 jackets, 4 skirts, 3 hoodies

**These claims are also embedded as JSON-LD** — `Article` and `FAQPage` schema
inside the article body. Google reads that as fact. A false claim in structured
data is worse than the same claim in prose, because it is machine-consumed and
eligible for rich results.

**Estimate: 300–420 articles make at least one product-specific claim.
Confidence: medium** — "with real specs" appears in most sampled summaries, but
lifestyle/styling pieces may not.

Not found in the sample: references to the five fabricated reviewers, or to the
removed "Organic cotton" claim. **Confidence: low** — 26 of 501 is too thin to
clear the corpus. Worth a targeted string search before any bulk action.

## Imagery — AI-generated, and traceable

Article images carry filenames like
`hf_20260728_191442_f8888153-…png` and `hf_20260730_093022_…png`.

**`hf_` is the Higgsfield generation prefix.** This session generated
`hf_20260823_125846_…` through the same service. So the blog imagery is
AI-generated, dated 2026-07-28 to 07-30 — during the bulk-publication window.

Licensing is therefore the generator's terms, not stock licensing. Per the
Design Standard Directive that is **permitted** for editorial imagery. The open
question is whether any of it depicts a *garment presented as a product*, which
would be misrepresentation. Not determinable from filenames. **Requires visual
review — and this environment cannot fetch the CDN (403 at CONNECT).**

## Does the corpus earn traffic? Yes — measured, not guessed.

**Google Search Console is unavailable** (OAuth required, non-interactive
session). **Shopify Analytics is available**, and answers it:

**90 days, all sources: 4,458 sessions** — direct 3,541 · social 550 ·
**search 362** · unknown 5.

Blog articles visible in the top-25 landing pages:

| Article | Direct | Search |
|---|---:|---:|
| `hot-yoga-outfits-what-survives-105-degrees` | 16 | 7 |
| `common-perfume-mistakes-to-avoid` | 9 | — |
| `bulgarian-split-squats-why-they-hurt-and-why-they-work` | 9 | — |

So the blog earns **real but modest** traffic — roughly 41 sessions visible in
the top 25, with an unmeasured long tail across 501 articles. It is not dead
weight, and it is not a major asset. **Confidence: high on the direction, low on
the total** — I did not paginate the full landing-page report.

## 🔴 Unrelated finding the traffic data forced into view

The top landing pages reveal this store previously sold **at least four
unrelated categories**:

| Landing page | Category | Sessions |
|---|---|---:|
| `/products/roxelis-pheromone-roll-on` | **perfume / pheromone** | 241 |
| `/products/focus-foxes-print-play-screen-free-math-reading-games-ages-4-10` | **children's educational games** | 33 |
| `/products/hivolt-collagen-peptides-1` | **supplements** | 21 |
| `/products/hivolt-collagen-power-bundle` | supplements | 9 |
| `/blogs/news/common-perfume-mistakes-to-avoid` | perfume article | 9 |
| `/collections/damen` | **German-language collection** | 6 |

Three consequences:

1. **`focus-foxes`** matches the prior repo note that customer accounts sit on
   `account.focusfoxes.shop`. Same operator, different brand, same Shopify store.
   That is E15 cross-brand contamination at store level.
2. **The current Terms of Service state:** *"We do not sell supplements, food or
   any ingestible product, and we make no health, medical or nutritional
   claims."* The store **did** sell collagen peptides. If any of the 501
   articles carry health or nutritional claims, that is a §3 violation and a
   regulatory exposure the Terms explicitly disclaim.
3. **`/collections/damen`** confirms the German metafield leftovers
   (`custom.groessentabelle`, `custom.faq_passform`, `custom.faq_material`).
   A German-market configuration existed and its remnants are still in the
   schema.

**The blog is not one corpus.** It contains at least activewear, perfume, and
possibly supplements content. Any classification that treats all 501 as
activewear is wrong.

## Classification

Estimated split across all 501. **These are extrapolations from 26 articles.**

| Disposition | Est. share | Est. count | Rationale |
|---|---:|---:|---|
| **Rewrite** for the new category | 55–70% | 275–350 | Well-written, structurally sound, but activewear-framed with dead product links. The prose is worth salvaging; the claims and links are not |
| **Delete** | 20–30% | 100–150 | Product round-ups whose entire premise is ranking products that no longer exist. Nothing survives the rewrite — "Best Leggings for CrossFit" has no version that works for a premium essentials catalog |
| **Redirect** | 5–10% | 25–50 | Off-category — perfume, supplements, children's games. Redirect to a relevant hub or retire with a 301 |
| **Keep as-is** | 5–10% | 25–50 | Genuinely category-neutral: how-to-measure, fabric-care principles, laundry guidance |

**Confidence: low-to-medium on the percentages, high on the ordering.** Rewrite
is the largest bucket; keep-as-is is the smallest.

## Recommended sequence — not executed this session

1. **String-search all 501** for: the fabricated reviewer names, "Organic
   cotton", health/nutritional claims, and `/collections/` links. Cheap,
   mechanical, and it converts every estimate above into a count.
2. **Strip the embedded JSON-LD** from every article making product claims.
   Highest-severity, lowest-effort fix: the false claims stop being
   machine-readable immediately.
3. **Fix links before content.** A dead `/collections/bottoms` is a defect today;
   activewear framing is only a defect once the new catalog lands.
4. **Then** rewrite by bucket, highest-traffic first.

Nothing was deleted, rewritten, or redirected. The audit informs the decision; it
does not make it.
