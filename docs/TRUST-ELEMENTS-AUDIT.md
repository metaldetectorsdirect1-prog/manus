# Trust elements audit — 2026-08-30

Brief: *"our Goal is to have the most trusted store like apple.com, nike.com …
we need to have all trust elements of the website like favicon and everything
else and fix any false or contradicting details."*

Measured against the live site (rendered in headless Chromium) and the live
Shopify policy records. Everything below is a reading taken on 2026-08-30.

---

## 1. What a visitor can currently verify about you: almost nothing

| Trust element | Apple / Nike | HIVOLT live |
|---|---|---|
| Favicon | yes | **none — `iconCount: 0`** |
| Apple touch icon | yes | none |
| Phone visible on site | yes | **no** |
| Email visible on site | yes | **no** |
| Postal address on site | yes | policies only |
| Organization schema with address + phone | yes | **name, url, email only** |
| `og:image` over HTTPS | yes | **served over `http://`** |
| Social profile links | yes | all five settings empty |
| Customer reviews | yes | none yet — stated honestly |

**The favicon is the visible one.** With `favicon: ""` the browser tab, the
bookmark, and the history entry all show a blank page glyph. Every large retailer
has one. It is the cheapest trust signal on this list and the store has none.

## 2. Contradictions found — a store that disagrees with itself

These were live simultaneously.

| Claim | Contradicted by |
|---|---|
| Announcement bar, **every page**: *"60 DAYS TO RETURN OR EXCHANGE"* | Refund Policy: *"We do not process direct exchanges."* |
| Terms §1: *"We sell technical activewear and gym apparel"* | The store sells dresses, coats, knitwear, denim, footwear, menswear — 925 products across 17 categories |
| Terms §1: *"We publish the fibre composition and fabric weight in grams per square metre for each style"* | No product page carries a GSM figure. Checked across all 206 rewritten descriptions. |
| Contact policy: *"Orders are dispatched from Illinois."* | Shipping policy: *"fulfilled and dispatched by our overseas manufacturing partner … rather than from a warehouse we hold in the United States"* |
| Terms §1: *"HIVOLT is a single member limited liability company"* | Shipping policy: *"HIVOLT is a trading name of Dn Global Trading LLC"* |
| Refund policy: *"cancelled … before they enter production"* | Nothing is produced to order; it is dispatched by a supplier |

The Shipping Policy is the honest one and the others should be brought into line
with it. Its disclosure — that orders ship from an overseas partner, not a US
warehouse — is a genuine trust asset and is why the 10-18 day window makes sense.

## 3. Done in this session

| Fix | State |
|---|---|
| Organization schema enriched: `legalName`, `telephone`, `PostalAddress`, `ContactPoint`, `areaServed` | **applied** to draft theme `158911987944`, verified (2,668 → 3,371 bytes, `updatedAt 04:38:34Z`) |
| Fabricated colour claims removed from SEO title + description, 206 products | applied, verified 0 residue |
| Fabricated colour claims removed from description bodies, 206 products | applied |
| `"In stock now."` / `"In stock and ready to ship."` removed from products with no stock | applied |
| `"Fit: true to size — see size guide"` removed from jewellery, bags, scarves and hats where it is meaningless | applied |
| `sale` collection "Up to 80% off" with 0 products | fixed earlier |
| `best-sellers` "chosen by customers again and again" on 0 orders | fixed earlier |

## 4. Blocked — needs the owner

### 4.1 The three policy rewrites

`shopPolicyUpdate` returned:

```
Access denied for shopPolicyUpdate field.
Required access: `write_legal_policies` access scope.
```

The connector does not hold that scope, and that is not something to work
around. Corrected text is written and ready; it needs pasting into
**Settings → Policies**. The three edits are:

**Contact information** — replace *"Orders are dispatched from Illinois"* with
*"Orders are fulfilled and dispatched by our overseas manufacturing partner and
sent directly to you, rather than from a warehouse we hold in the United
States."* Change *"Business Name: HIVOLT"* to *"HIVOLT is a trading name of Dn
Global Trading LLC"*. Add *"We do not process direct exchanges."* to the returns
line.

**Terms of Service §1** — replace the activewear-only description with the real
category list, change *"HIVOLT is a single member limited liability company"* to
*"HIVOLT is a trading name of Dn Global Trading LLC, a limited liability company
registered in the State of Illinois"*, and replace the GSM claim with: *"Where a
supplier publishes a fibre composition, a fabric weight in grams per square
metre, or a garment measurement, we publish it on that product's page. Where a
supplier publishes nothing, we say so rather than estimating a figure."*
Add the no-exchanges sentence to §6 and the overseas-fulfilment sentence to §5.

**Refund policy** — *"before they enter production"* → *"before they are
dispatched"*. Add *"We do not issue store credit in place of a refund."*

### 4.2 Favicon

`config/settings_data.json` has `"favicon": ""`. It needs a square image,
512×512 PNG on a transparent or `#1A1A1A` ground, legible as a single mark at
16px — a HIVOLT monogram rather than a wordmark, because a wordmark is unreadable
at that size. Upload under **Settings → Brand**, then set it in the theme editor.

This was deliberately not auto-filled with the existing `ChatGPT_Image_Jul_25…png`
that currently serves as the `og:image`: it has not been inspected at favicon
size, and the brand mark is a decision worth making rather than inheriting.

### 4.3 Announcement bar

*"60 DAYS TO RETURN OR EXCHANGE"* → *"60 DAYS TO RETURN, FREE"*. It lives in the
header section group, edited through the theme editor.

### 4.4 Still outstanding from the earlier audit

- **918 of 925 products carry phantom inventory.** The single largest trust
  defect on the store. Nothing else on this page matters as much.
- `og:image` served over `http://` — should be `https://`.
- Social profile links all empty; `sameAs` cannot be added to the schema until
  they exist.
