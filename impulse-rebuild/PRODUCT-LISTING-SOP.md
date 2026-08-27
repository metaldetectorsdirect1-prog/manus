# PRODUCT-LISTING-SOP.md

> **Internal operating document.** Distilled from paid course material for this
> store's own operations and its product listers — the use the course licenses.
> Do not redistribute, publish, or share outside the team.

The per-product compliance SOP for Google Merchant Center, as supplied by the
owner 2026-08-26. **Enforced mechanically by `site/check-product-listing.py`**
(12/12 self-tests) — run it against every product JSON before publishing; exit 1
is a refusal, not a suggestion.

## What the validator enforces

| Area | Refused |
|---|---|
| Titles | >150 chars · ALL CAPS (whole or per-word) · promo language ("free shipping", "% off", "sale", "best seller") · emoji, ★, ™, ✓ |
| Descriptions | `<img>` tags · external links · CTAs ("click here", "buy now") · urgency ("limited stock", "flash sale", "only N left") · medical/health claims · **✓ characters** (use bullets) |
| Pricing | EUR/USD/GBP/CAD/CHF/NZD not ending **.95** · DKK/PLN not rounded to 0/5 · discount >50% vs compare-at |
| Organization | missing vendor · supplier-named vendor (AliExpress/CJ/Temu…) · no category · handle with trailing numbers (`dress-231`) · **handle ≠ title slug** (the top automatic trigger) |
| Images | none · supplier-CDN URLs (alicdn etc.) · missing alt text (warning) |

## Details this SOP added beyond the module notes

- **Price psychology per currency**: .95 endings for EUR/USD/GBP/CAD/CHF/NZD; whole 0/5 for DKK/PLN.
- **Discount tiers follow product quality**: high-quality products up to 50%, average 20–40%, poor images **no discount** — a bad photo with a big discount reads as bait.
- **Vendor = the store name**, not merely "not the supplier."
- **No checkmark characters inside descriptions** — bullets only. (Note: on this store's own product pages the spec sections use tables anyway.)
- **No collages / multi-view composites** as a single image — one product, one frame.
- Metafields completed, **especially size options** — which is also what feeds the ~33-SKUs-per-product variant math.

## The one unspecified value

The checklist says *"price meets minimum threshold"* but the SOP text does not
state the number. `[[NEEDS: minimum price threshold]]` — do not invent it; take
it from the course's pricing module or the owner.

## Pipeline position

Master list → Planner bands → Trends curves → gap test → `scored-list.csv` →
supplier mapping → **this validator, per product** → import batch (5 first;
then 25/day or 50/week per the calendar).

## Interpretations from the walkthrough (what the rules mean, not just say)

- **"Clear focus on the product" ≠ the agency myths.** It does not mean
  AI-models-only, and it does not mean full-body-only or no-crop. Models are
  fine. The actual rule: a viewer must be able to tell **which garment is for
  sale**. A model wearing sneakers + jeans + top + cardigan fails *when the
  listing is for the cardigan* — same photo could pass as the jeans listing if
  the framing makes the jeans the subject. Ambiguity is the violation, not the
  human.
- **AliExpress-grade images are a suspension matter, not a quality preference.**
  Google is protecting the quality of its own shopping surface; low-grade
  supplier photos read as exactly the store type it purges.
- **Why the SOP exists at all: every feed change is a trigger event.** Each
  product added or edited can fire an automatic or manual GMC check. The SOP is
  not per-product perfectionism — it is making sure that *whenever* the check
  fires, whatever it lands on is clean. This also re-justifies batch imports:
  fewer feed-change events, fewer dice rolls.
- **Provenance note:** this SOP is the course team's operating rule set, validated
  by keeping their own stores alive — not Google's published policy text.
  Where an agency claim conflicts with it, the SOP wins here; where Google's
  actual policy conflicts, Google wins.

- **Copyright is the terminal suspension** — fake Goyard/Gucci/Dr Martens class.
  <1% recovery; the GMC never comes back. The validator now refuses ~30
  frequently-counterfeited fashion marks in title, description or tags, and the
  "dupe / inspired by / replica / designer style" phrasing that carries the same
  trademark risk. The regex is a floor, not a licence: an unlisted brand name is
  still a violation.
- **Neutral backgrounds are preferred, not mandatory** — the narration is
  explicit ("we don't always do it"). They help branding and consistency; their
  absence is not a compliance failure. The pasted SOP's "must have" is read as
  strong-default.

## Suspension-trigger ranking (image review triage order)

1. **Copyright product** — terminal, <1% recovery. Check first, always.
2. **Watermark / text on image** — incl. Chinese text on supplier photos. A top
   trigger but recoverable; the tell of an unedited AliExpress import.
3. Everything else in the image rules (quality, ambiguity, backgrounds).

And the title principle stated as a mechanism, not a rule: **the title is where
the keyword research cashes out.** A researched keyword that is not in a product
title does nothing — Google matches shopping queries against titles, so the
scored-list keywords must literally appear in the titles of the products bought
against them. Research → scored sheet → supplier pick → **keyword into title** is
one unbroken chain; break the last link and the first three were wasted.

## Batch mode and the competitor-import hygiene chain

`--batch file.json` (array or JSONL) validates a whole import batch: every
per-product rule, plus **catalog-level title and handle uniqueness** — a rule a
single-product check cannot see. Run it on each weekly 50-batch before launch.

Competitor sourcing is allowed but the de-linking must be total, in this order:
1. **Title rewritten from scratch** (the formula, not a paraphrase)
2. **Description rewritten from scratch**
3. **Image metadata stripped** — EXIF ties a photo to its source site. At import:
   `exiftool -all= img.jpg` or a PIL re-save. Shopify's CDN re-encodes uploads,
   which strips most EXIF, but strip *before* upload rather than relying on it.
4. Handle regenerated from the new title (enforced by the validator)

And the description rule now stated with its reason: images inside descriptions
are refused **because they break** — each is a link out of Shopify's asset
pipeline that 404s when the source moves, and broken product pages are a named
suspension trigger. Size charts in descriptions are welcome — as text/tables,
never as images.

## Health-adjacent products: short-term money, long-term exclusion

Orthotic/orthopedic-class products (posture, compression-as-therapy, arch
support) can make short-term revenue but are named as incompatible with a
long-term store. **This supersedes the course's own Module 7.3 title examples**
("orthopedic high heels", "orthopedic wedge sandals") — an internal
contradiction resolved in favour of the stricter rule. The validator's medical
screen (orthopedic, therapeutic, clinically proven, medical-grade…) stays
strict; body-shaping terms without health claims (shapewear, tummy control)
remain allowed.

## Sale framing: seasonal names only, and the rules tightened over time

Closure/clearance sales worked on the team's first GMC "back then" — **that era
is over.** Only time-boxed seasonal framing survives: *Black Friday sale, winter
sale, seasonal sale.* Their Q4 numbers came from exactly these. Never
"closing down", "clearance", "everything must go" — and note the general lesson:
Google's tolerance ratchets down over time, so a tactic that worked on an old
GMC is not evidence it works on a new one.

## Discount mix — enforced at batch level

The pattern Google reads is longitudinal: *"running ads three months, always a
sale, every product the same discount, the sale never ends."* The validator now
refuses a batch (n≥10) where **everything** is discounted, or where every
discount is one uniform rate. The intended distribution: some at 0%, some 20%,
some 40%, **best sellers at 50%** — refreshed on the best-seller review.

Cadence note: this narration says the best-seller sweep is **biweekly**; the
earlier module notes said weekly. Recorded as biweekly per the more specific
statement — either way it aligns with the Pythago feed review rhythm.

## Empty collections — the SATA example, and HIVOLT's live exposure

"A dress collection with zero products in it" is the suspension example given.
**hivolt-usa.com currently has fourteen exactly-that collections live** —
`publishableUnpublish` is blocked at the connector, so unpublishing them remains
the standing owner action from `GMC-READINESS.md`. If a general store launches
on a fresh domain instead, its collections must be created *populated*, never
scaffolded empty.

## Launch mechanics — two modes, and the switch rule

**Batch mode (the safe default, and how the team runs earning stores):**
lister uploads **50–100 products per week as drafts**; once a week, all of them
launch **simultaneously**. One launch = one feed-change event = one dice roll,
instead of fifty.

**Daily mode (faster, riskier — one situation only):** a fresh GMC, just
approved on 5 products, *after* the post-approval freeze. Then 5→10→15→20→25
products per day for a few weeks.

**Switch from daily to batches when EITHER condition hits, whichever is first:**

| Trigger | Threshold |
|---|---|
| Count | **400–600 products** |
| Money | the store turns **profitable/consistent** — even below the count |

The second trigger is the operative one: *"as soon as you're profitable, you
don't want to risk anything anymore. It's not worth it."* A money-making GMC
never takes daily-import risk again.

**Shopify-mechanical translation for this pipeline:**
1. `productCreate` with `status: DRAFT` — validator (single-product mode) runs here, at listing time
2. Weekly: assemble the batch → validator `--batch` runs across all drafts (uniqueness + discount-mix)
3. One aliased mutation flips the whole batch `DRAFT → ACTIVE` — the single feed-change event
4. Never trickle drafts live individually; the simultaneity *is* the safety
