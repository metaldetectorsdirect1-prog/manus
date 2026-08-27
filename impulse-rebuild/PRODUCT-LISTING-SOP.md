# PRODUCT-LISTING-SOP.md

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
