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

---

# Data-driven classification — 2026-08-24 (Phase 5)

The sampling estimates above are superseded by measured data.

## Embedded JSON-LD — scanned, quantified, not yet stripped

First 50 articles by publish date, machine-scanned:

| | |
|---|---|
| Articles carrying embedded JSON-LD | **50 / 50 — 100%** |
| ...of which make product / spec / material claims | **42 / 50 — 84%** |
| Schema types per article | `Article` ×1, `Organization` ×2, `FAQPage` ×1, `Question` ×3, `Answer` ×3 |

**Extrapolated to the corpus: ~501 articles carry embedded JSON-LD; ~420 make
claims about products that no longer exist.** Confidence high — the pattern is
100% consistent across the batch, which is what a template-driven generation run
produces.

## Traffic — the whole corpus, measured

90 days, all landing pages. Blog articles appearing above 4 sessions:

| Article | Sessions |
|---|---:|
| `hot-yoga-outfits-what-survives-105-degrees` | 23 |
| `common-perfume-mistakes-to-avoid` | 9 |
| `bulgarian-split-squats-why-they-hurt-and-why-they-work` | 9 |
| `best-gym-clothes-that-hide-sweat` | 7 |
| `should-you-put-gym-clothes-in-the-dryer` | 7 |
| `how-long-do-leggings-last-lifespan-and-replacement-signs` | 5 |
| `/de/blogs/news/jump-rope-workouts-from-first-skip-to-10-minute-rounds` | 5 |
| `how-to-dry-gym-clothes-fast-when-you-train-daily` | 4 |
| `thermal-regulation-how-fabric-keeps-you-cool-and-warm` | 4 |
| `washing-white-activewear-keeping-it-bright-without-bleach` | 4 |
| `best-color-block-activewear-bold-without-clashing` | 4 |
| `removing-deodorant-stains-from-black-workout-tops` | 4 |
| `breathing-while-running-rhythms-that-prevent-side-stitches` | 4 |
| `what-time-is-the-gym-least-busy-data-backed-windows` | 4 |

**~93 sessions across 14 articles. Total site: 4,151. The blog is 2.2% of
traffic.**

The report cut off at 4 sessions. **So 487 of 501 articles drew 3 or fewer
sessions in 90 days** — under 0.03/day each. The prune-heavy call is correct,
and the data supports it more strongly than the sampling did.

### 🔴 A German storefront locale is live

`/de/blogs/news/jump-rope-workouts-…` — **5 sessions.** Alongside
`/collections/damen` (7) and `/collections/herren` (5).

This is not just leftover metafields. **A `/de/` locale is serving pages and
earning traffic.** Any prune that ignores it will orphan German URLs, and any
redirect map must cover both `/blogs/` and `/de/blogs/`. Recorded in
`APP-CONFLICTS.md`.

## Survivor set — 13 candidates

`common-perfume-mistakes-to-avoid` is **deleted regardless of its 9 sessions**,
per §3.5: off-category, perfume.

The strongest survivors are not the product round-ups — they are the
**garment-care** pieces, which are close to category-neutral and survive a
repositioning with light editing:

| Candidate | Why it survives |
|---|---|
| `should-you-put-gym-clothes-in-the-dryer` | Care principle, applies to any knit |
| `how-to-dry-gym-clothes-fast-when-you-train-daily` | Same |
| `washing-white-activewear-keeping-it-bright-without-bleach` | Same |
| `removing-deodorant-stains-from-black-workout-tops` | Same |
| `how-long-do-leggings-last-lifespan-and-replacement-signs` | Garment-lifespan principle |
| `thermal-regulation-how-fabric-keeps-you-cool-and-warm` | Fabric science, fully category-neutral |
| `hot-yoga-outfits-what-survives-105-degrees` | Highest traffic; needs heavy rewrite |
| `best-gym-clothes-that-hide-sweat` | Rewritable as a fabric-behaviour piece |
| `bulgarian-split-squats-…`, `breathing-while-running-…`, `what-time-is-the-gym-least-busy-…` | Training content, no product claims — **keep as-is** candidates |

**These six care pieces are queue item 10.** The care guide should be built by
consolidating them rather than written from scratch — they already earn traffic
and already rank.

## Not executed this session

**No article was deleted, redirected, or edited.** The prune is designed, not
performed.

Reason, stated plainly: §3.4 requires redirects created **before** deletion.
Doing 487 deletions plus a redirect map across two locales is a batch job larger
than the budget left in this session, and a half-finished prune — some articles
gone, some redirects missing — is materially worse than an untouched corpus. It
would create exactly the E6 defects at scale that this build has been closing.

**Recommended execution order for the next session:**

1. Build the redirect map first, covering `/blogs/news/*` **and** `/de/blogs/news/*`.
2. Create every redirect. Verify.
3. Delete in batches of 50, re-counting `articlesCount` after each.
4. Strip embedded JSON-LD from the ~13 survivors only — deleting the other ~488
   removes their bad schema at no cost.
5. Consolidate the six care articles into the care guide.
