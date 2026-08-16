# Google Ads dropshipping — the method, mapped onto HIVOLT

2026-08-14. Source: four transcripts the owner supplied from the AB Inner
Circle channel (Google Ads dropshipping, ~20 stores, fashion). Their revenue
screenshots are their claims and nothing here depends on believing them; the
*mechanics* are internally consistent and mostly verifiable against Google's
own documentation, so what follows is the method distilled, then HIVOLT's
position against each piece, then the divergences adopted deliberately.

The owner has decided the store runs Google Ads. That supersedes the earlier
no-ads constraint.

## The method, in one paragraph

Google Shopping is demand capture, not demand creation. The Merchant Center
feed IS the business: wide catalogue of items people already search for,
listed 2 months + ~16 days before their seasonal peak (products take ~2 weeks
to start receiving spend after listing), titles built from 2–3 real search
keywords, clean text-only descriptions, one PMax campaign restricted to the
shopping feed only (all other surfaces disabled), start $50/day, scale by
doubling only while ROAS holds 2.5–3, and every two weeks draft any product
whose ad spend passed the account's average CPA (~$30 in fashion) without a
sale — so budget concentrates on winners. Feed quality drives CPC (target
<$0.50 US); suspension avoidance is mostly policy consistency: identical
shipping/return numbers everywhere, real contact details, social profiles
linked, sales under 50%, no price mismatch between store and feed.

## Where HIVOLT already stands

Further along than a fresh store on every axis except catalogue size:

| method requirement | HIVOLT state |
|---|---|
| GMC exists, products synced | Google & YouTube channel installed, 113 active products on it |
| feed attributes complete | gender/age_group/custom_product/category/image/size/color: 113/113, verified per-product |
| policy consistency | full read 08-14: refund, shipping, terms §5/§6, contact all agree. Free shipping, no minimum, 60-day free-label returns |
| no aggressive sales | max discount 20%; automatic 15%; nothing near the 50% line |
| price mismatch | impossible by construction — the channel syncs from Shopify; no manual feed edits, and the standing rule is **never upload a feed TSV** |
| titles | 107/113 carry a gender word, median 55 chars, only 5 exceed the ~70-char Shopping truncation |
| descriptions | text-only, spec-led, zero contradictions with policy (scanned all 134) |
| PDP quality | conversion fixes staged in source (v36): mobile snap gallery, sticky add-to-cart, strongest-facts price line |

## The gaps, ranked by what they block

1. **The domain claim in Merchant Center.** Everything in the method runs
   through an approved GMC serving impressions. An unclaimed account cannot
   appear in Shopping at all, and two accounts claiming one domain
   (5838274874 vs 5705286743) suppress offers in a way that looks exactly
   like a feed fault. Nothing else on this list matters until this is done.
   Owner-only; `merchants.google.com` is blocked from this container.
2. **Ads data.** The CPA drafting rule — the single highest-leverage habit in
   the method — needs per-product spend and ROAS. Windsor.ai's `google_ads`
   connector is the pipe; the auto-login authorization link was issued 08-14
   and is unused. Until it's authorized, nobody can run the every-two-weeks
   draft pass, and losers accumulate spend silently.
3. **The v36 deploy** (PDP fixes) — built, validated, waiting only on the
   Shopify connector re-auth.
4. **Catalogue cadence.** The method lists 50–100 products/week; HIVOLT has
   113, static. This is the real strategic divergence — see below.
5. **Seasonal window, and it is open NOW.** Mid-August plus the 2-months+16-days
   rule means importing for late October–November demand **today**: hoodies,
   sweatshirts, joggers, track pants, jackets, long-sleeve training tops.
   HIVOLT already carries all of these categories, so "double down on what
   works" and the seasonal play point the same direction: deepen hoodies /
   joggers / jackets before deepening anything summer.
6. **Social links.** GMC trust wants Instagram/Pinterest linked and in the
   footer; theme settings carry only `social_facebook`. Owner-gated.
7. **GMC delivery settings must mirror the policy**: cutoff + 2–4 day
   handling + 8–14 day transit. Longer than their 7–12 example; consistency
   matters more than the number, and the policy is already published.

## Title work prepared, not yet applied

All 113 titles lead with "HIVOLT" — the highest-value characters spent on a
brand nobody searches, while the brand already reaches Google through the
feed's brand attribute. The method's pattern is keyword-first
("Women's High-Rise Flared Yoga Leggings …"). Moving the brand off the front
is a bulk `productUpdate` sweep, prepared once Shopify is back. If it
happens, now is the time — title edits trigger item re-review, which costs
days of serving, and the account currently serves nothing.

## Divergences, chosen deliberately

- **No deliberate suspension.** The transcripts suggest doing "things
  purposely wrong" to trigger the first suspension early. With an unclaimed
  GMC and a 42-day-old domain, inviting a misrepresentation strike gambles
  the one asset the whole plan depends on. Rejected.
- **Free return label stays.** Their setup makes the label the customer's
  responsibility. HIVOLT's policy provides it free — a published
  differentiator, already mirrored in GMC-relevant schema
  (`returnFees: FreeReturn`). Changing it to match a video would be a
  coupled edit across refund policy, terms, product copy and JSON-LD, in the
  wrong direction.
- **Spec honesty survives scale.** Mass-import at 50–100/week only works
  here if each product keeps the published fibre composition and fabric
  weight, quoted not invented — blank when the supplier publishes nothing.
  Import velocity is capped by spec availability, and that is the brand.
- **Supplier reality check before any import wave:** the Tapstitch
  app-managed shipping profile had 89 paid US rates deactivated by hand. A
  catalogue resync can reactivate them, and paid rates appearing at checkout
  while every policy says free shipping is precisely the
  price/shipping-mismatch class of suspension. Any import batch must be
  followed by re-reading the shipping profile.

## The operating loop, once the claim lands

Weekly: import batch (seasonal + double-down categories), spec metafields
populated, titles keyword-first, run `site/check-liquid.py` if theme copy
changed, verify shipping profile untouched. Every two weeks: pull
per-product spend/ROAS via Windsor, draft everything past ~$30 spend with no
sale, read winners from right to left (30d → 7d) before killing anything
whose recent curve is improving. Scale budget by doubling only at ROAS ≥ 2.5.
Watch CPC drift above $0.50 as the feed-quality alarm.
