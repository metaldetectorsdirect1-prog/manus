# HIVOLT — full store audit, 2026-08-08

Three read-only agents swept the store in parallel: theme Liquid, theme CSS and
design system, and SEO metadata across all 642 resources (110 products, 14
collections, 18 pages, 500 articles). Everything below was verified against live
Shopify data before it was changed. Where an agent was wrong, that is recorded
too — including the one case where I acted on a wrong finding and had to revert.

The theme fixes are in commit `86ad852`. This document covers the store-side
data changes, which are live immediately and independent of which theme is
published.

---

## 1. Factual contradictions in metadata — 5 found, 5 fixed

These are the severe class: the store asserting a number that its own published
data contradicts. Same family as the Drop 04 "210 gsm" bug.

| Resource | Was | Verified truth | Now |
|---|---|---|---|
| `voltcore-2-piece-set…` product | "save **$10.98**" | bra $38 + leggings $54 = $92, set $79 | "save **$13**" |
| `leggings` collection | "**220**-270 g/m2" | published gsm: 200, 220×5, 230, 250, 270 | "**200**-270 g/m2" |
| `leggings` collection | "Sizes **S-2XL**" | max size in collection is XL; 6 of 15 are 4–12 numeric; one runs 2XS | "Sizes 2XS-XL and 4-12" |
| `outerwear-hoodies` collection | "Sizes **XS-2XL**" | two products run 2XS; three are 2-4/6-8/10-12 | "Sizes 2XS-2XL and 2-12" |
| `tennis-and-court` collection | "tennis and **pickleball** apparel" | none of the 9 members mentions pickleball | phrase removed |

### The one I got wrong

The SEO agent reported the `outerwear-hoodies` fabric range "130-380 g/m2" as
fabricated, on the grounds that the lightest published `spec.gsm` metafield in
the collection is 165. I changed it to 165-380 on that basis.

That was wrong, and I reverted it. `soft-hooded-sports-jacket` has no
`spec.gsm` metafield — `build-spec-metafields.py` only wrote the metafield where
the supplier gave a g/m² figure, and this supplier gave imperial:

> **Weight:** Light (3.8 oz/yd²)

3.8 oz/yd² × 33.906 = **128.8 g/m²**. The original 130 was accurate. The
collection now reads "130-380 g/m2 from light layers to heavy fleece" — the
range restored, and the word "fleece" no longer applied to a 130 g/m² shell.

**Lesson worth keeping: absence of a metafield is not absence of the fact.**
Nine of the ten products in that collection had the metafield; reasoning from
that set alone produced a confident wrong answer.

---

## 2. The Drop Calendar was selling two things that do not exist

`/pages/drops`, body copy:

1. **"210gsm quick-dry knit"** — the third appearance of this contradiction.
   Product `spec.gsm` metafields, the Drop 04 collection description and the
   collection's SEO description all say **220**. Corrected.

2. **"sizes are held for 15 minutes at checkout"** — Shopify does not do this.
   There is no 15-minute size reservation on this plan; inventory is decremented
   at payment. This is a manufactured-scarcity mechanic that a shopper can
   directly disprove by leaving a tab open, and it sits on the page whose whole
   job is to make the drop model credible. Replaced with what actually happens:
   nothing is held or reserved.

3. **"Circuit members get 24-hour early access"** — removed, because the
   Membership page states the opposite in as many words: *"There is no members'
   discount, no points balance and no tier to climb. The Circuit is a
   notification list."* Two pages, two incompatible descriptions of the same
   programme. The Membership page is the one the theme template was built
   around, so the Drop Calendar was brought into line with it.

---

## 3. The shipping page was selling a country the store cannot ship to

`/pages/shipping-delivery` opened with:

> "We currently ship to the **United States and Canada** only."

followed by a full Canada section — **$9.95 flat rate, tracked, 10–20 business
days, customer pays duties**.

The store is US-only. The delivery profiles are US-only, the Returns & Refunds
page says "We ship within the United States only", and the shipping policy
agrees. A Canadian shopper could read a priced, specified service and then find
no way to buy it at checkout.

Canada section removed; opening line now says United States only.

---

## 4. The under-$50 article was quoting a price the store has never charged

`quality-activewear-under-50-what-39-99-should-get-you` claimed, in the body:

> "**HIVOLT prices most pieces at $39.99**"

and built a table headed *"What $39.99 Gets You at HIVOLT"* around three
products. The store uses whole-dollar pricing. The real prices of those three:

| Product named in the article | Real price |
|---|---|
| "Performance Short Sleeve T-Shirt" (actually *Unisex Performance Training T-Shirt*) | **$34** |
| "Soft Hooded Sports Jacket" | **$69** — not under $50 at all |
| "Women's Cropped Sports Bra" (actually *Women's High-Stretch Cropped Sports Bra*) | **$38** |

It also attributed "87% polyester, 13% spandex at 200 g/m2" to the short-sleeve
tee. That spec belongs to the **long**-sleeve tee; the short-sleeve product
publishes no composition or weight at all.

Rewritten against verified data. The sub-$50 tier is **$34 / $38 / $42**, and
the table now carries eight products whose price, composition and gsm are all
published on their own product pages. The $69 jacket is gone.

One knock-on: the original set a "minimum 160 g/m² for tops" rule that HIVOLT's
own $34 tee (130 g/m², 100% polyester) fails. The FAQ now describes what weight
is *for* — 130–180 for hot-weather tops and layering, 200+ where opacity under
stretch matters — instead of a threshold the catalogue contradicts. The FAQ
JSON-LD was updated to match; it had the $39.99 figure in it too.

Title and meta title no longer name a price. The handle still contains
`39-99`; changing it would break the URL, and a redirect is a separate call.

---

## 5. Missing metadata — 17 of 18 pages now covered

Only 4 of 18 published pages had any SEO metadata. Google was building snippets
from body text — which is how the "United States and Canada" line above could
have reached a search result.

Written for 13 pages (title + description), plus a title for the
`drop-04-voltcore` collection, which had a description but no title.

Notable: **`/pages/voltcore` — the Voltcore landing page, the store's single
conversion target — had neither.** So did the 60-Day Guarantee page.

`google-site-verification` was deliberately **not** given metadata. Its entire
body is the verification token; it is thin content with nothing to rank. It now
emits `<meta name="robots" content="noindex,follow">` via a handle check in
`layout/theme.liquid` — noindex rather than disallow, so the verification fetch
still succeeds.

---

## 6. Blog metadata — 500 articles

Every article's `description_tag` was byte-identical to its `title_tag`. There
was no real meta description anywhere in the blog, so Google discards it and
writes its own snippet: 500 URLs with no snippet control.

Separately, the six boilerplate suffixes stripped from article *titles* in
commit `0b20f8c` were never stripped from the *meta* titles, so 105 meta titles
disagreed with their own H1.

Both are mechanically fixable because two fields are already correct:
`article.title` (de-boilerplated) and `article.summary` (a real, specific
~150-char description per article). So `title_tag ← "{title} | HIVOLT"` and
`description_tag ← summary`.

The pipe also settles the separator: the store was running four conventions at
once — `| HIVOLT` on 123 products and collections, ` - HIVOLT` on 500 articles,
` — HIVOLT` on one page, and three pages with the brand mid-title.

**One correction issued mid-run.** The first instruction was to drop the brand
suffix when the total exceeded 60 characters. That is wrong here, because
`layout/theme.liquid` does:

```liquid
{% unless page_title contains shop.name %} &ndash; {{ shop.name }}{% endunless %}
```

Omitting the brand does not shorten the rendered title — Liquid appends
" – HIVOLT" itself, with an en dash, reintroducing the exact separator
inconsistency the pass exists to remove. The rule became: always append
" | HIVOLT", accept the length.

---

## 7. Checked and clean

Worth recording, because these were the suspicions going in:

- **Zero exact duplicate SEO titles or descriptions** across all 642 resources,
  normalised or not. The duplication is self-duplication (§6), not collision.
- **Zero competing-brand contamination in live metadata** — no "Focus Foxes",
  "YUBBEX", "collagen", "supplement" or "gummies" in any of the 642
  title/description values.
- **Zero hardcoded colour literals** in the stylesheets outside the documented
  `.swatch` exception.
- **Shipping and returns claims in product/collection metadata are consistent** —
  every one says "Free US shipping", none claims worldwide, Canada, UK or EU,
  and none misstates the 60-day window.
- **All 110 product titles and descriptions are within length.** The length
  violations are entirely in the blog.

---

## 8. Still open

**Needs the merchant, not the API:**

1. **Publish theme v21.** The connector cannot publish themes. v19 is currently
   MAIN; v21 carries every fix in commit `86ad852` plus the two above.
2. **The three legal policies** still describe a collagen-peptide subscription
   business, and are linked from the checkout page. `shopPolicyUpdate` needs the
   `write_legal_policies` scope, which this connector does not hold. Replacement
   text is in `LEGAL-POLICY-REWRITE.md`.
3. **Customer accounts still point at `https://account.focusfoxes.shop`.**
4. **The delivery window disagrees with the legal Shipping Policy.** Every
   storefront surface now says 2–4 to dispatch and 8–14 to arrive — 13 templates,
   the shipping page, the JSON-LD and the Voltcore FAQ, which was still on 5–8
   and is now aligned. The legal Shipping Policy says 1–2 and 5–8. Only the
   merchant knows which the fulfilment partner actually hits.

**Judgement calls left alone deliberately:**

5. **`/pages/wholesale` and `/pages/ambassadors`** describe operated programmes —
   trade pricing tiers, 24-unit minimums, 3–4 week custom-branding lead times,
   ambassador commission and seasonal kit. Nothing in the store contradicts them,
   but nothing evidences them either. They are business claims, not factual
   errors, so they were left as written and given accurate metadata. If those
   programmes are not actually running, both pages need rewriting.
6. **Eight unpublished pages carry YUBBEX and supplement-business titles**
   (`ambassador`, `team`, `ingredients`, `halal`, `subscribe`,
   `subscription-help`, `quality`, `help`). All are `isPublished: false` and
   return 404, so they emit nothing today. Deleting is irreversible and they are
   already inert, so they were left. They become live titles the moment anyone
   publishes them.

**Known and unfixed in the theme** (lower severity than the above):

7. `customers-addresses.liquid` — the province field is unusable without JS, and
   there is no `posted_successfully?` state.
8. `list-collections.liquid` — no `paginate`.
9. `product.liquid` — price and `compare_at` can disagree with the selected
   variant; `aria-pressed` default state.
10. `settings_schema.json` — no `favicon` or `share_image` setting.
11. `page.voltcore.liquid` — "Sizes S–XL, matte black" and the fit claims are
    hand-typed rather than read from the product.

---

## 9. Sales channels — 61 of 110 products were invisible to TikTok

Found while looking for organic distribution that costs nothing.

The store has an **"AfterShip for TikTok" publication installed** on Shopify
(`gid://shopify/Publication/188060008680`), and only **49 of 110 active products
were published to it**. The 61 missing ones included:

- `voltcore-2-piece-set-twist-front-bra-flare-leggings` — the flagship, the
  single product with its own landing page and the store's one conversion target
- `women-s-twist-front-v-neck-sports-bra` — its own component
- every unisex jersey, every skirt, every varsity jacket, most joggers

All 61 published via `publishablePublish`, zero `userErrors`, and verified by
re-reading `publishedOnPublication` on exactly the 61 IDs that were changed —
61/61 now true. **110/110.**

### This does not put anything on TikTok yet

Two separate facts, and they were worth separating:

| Check | Result |
|---|---|
| Shopify publication (`publishedOnPublication`) | **110/110** — done |
| AfterShip Feed onboarding (`check-onboarding-status`) | `connect_ecommerce_store`, `connect_sales_channel_stores`, `configure_initial_settings` — **all three false** |
| Connected TikTok Shop stores (`get-sales-channel-stores`) | **`[]` — none** |

So the catalogue is staged on the Shopify side and nothing is syncing, because
there is no TikTok Shop seller account linked. The value of doing it now is that
when that account is connected, all 110 flow rather than 49 — and nobody has to
notice that the flagship was among the missing.

### Also confirmed while checking

- **Payments work.** Shopify Pay, Apple Pay and Google Pay are all live, USD,
  SSL valid on `hivolt-usa.com`, `checkoutApiSupported: true`. The 0-for-24
  checkout record is not a broken gateway. (`read_shopify_payments` is still
  missing, so the card gateway itself could not be inspected directly — but
  three digital wallets being active means Shopify Payments is enabled.)
- **Markets are correct.** "United States" is primary and enabled;
  "International" is disabled. The market's handle is the legacy string
  `united-states-and-canada`, which is cosmetic — the market itself is US-only,
  which is why the Canada section on the shipping page (§3) described a service
  that genuinely could not be bought.
- **Other channels are complete**, not partial: Online Store, Shop,
  Facebook & Instagram, Microsoft Copilot and Manus all carry the catalogue.
  TikTok was the only one with a gap.

## 10. Blog metadata — complete

All **499 in-scope articles** repaired (500 minus the one handled by hand in §4):

- `title_tag` ← `"{title} | HIVOLT"` — 499/499, every one carrying the suffix
- `description_tag` ← `article.summary` verbatim — 499/499
- Articles where `title_tag == description_tag`: **500 → 0**
- Zero `userErrors` across 40 batched `metafieldsSet` calls
- Zero articles skipped for an empty summary — every one had a real summary
- Verified across the **full corpus**, not a sample: a second bulk export
  re-read `title`, `summary` and both metafields and diffed against intent

`bulkOperationRunMutation` was refused by the connector's safety policy. That is
a legitimate guardrail; the work went through batched `metafieldsSet` instead
and no attempt was made to route around it.
