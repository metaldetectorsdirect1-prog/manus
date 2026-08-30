# HIVOLT — full theme and landing page audit — 2026-08-30

Live theme `158911561960`, role `MAIN` (read from Shopify's `role` field).
Storefront rendered with headless Chromium via the Higgsfield sandbox; local
egress to hivolt-usa.com is blocked.

## 1. The landing page as a customer sees it

6,648px tall. **18 images. 7 product links on the entire page.**

| Section | Height | Images | Product links | Heading |
|---|---:|---:|---:|---|
| announcement | 38px | 0 | 0 | — |
| hero | 750px | 1 | 0 | The Winter Edit |
| category-edit | 785px | 3 | 0 | — |
| new-in | 724px | 8 | **7** | New This Week |
| dress-editorial | 700px | 1 | 0 | The Dress Edit |
| **knit-edit** | **573px** | **0** | **0** | **Knitwear We Love** |
| brand-story | 598px | 1 | 0 | Made to be kept |
| explore-grid | 746px | 4 | 0 | Explore |
| service | 330px | 0 | 0 | Complimentary US shipping |
| newsletter | 331px | 0 | 0 | — |
| footer | 548px | 0 | 0 | SHOP |

`new-in` is the only product rail that renders anything. A catalogue of 1,603
active products is represented on the homepage by seven.

**`knit-edit` renders 573 pixels of empty space beneath its heading.** Its
collection setting points at handle `knitwear`, which does not exist. An empty
section that still occupies half a screen is worse than one that collapses.

For scale, the Fashion Nova homepage measured the same way: 13,700px, 169
images, 57 distinct products.

## 2. Head and meta

| Field | Value | Verdict |
|---|---|---|
| `<title>` | Women's Dresses, Knitwear and Coats \| HIVOLT | good — specific |
| `description` | names the categories, free shipping, 60-day returns | good |
| `canonical` | `https://hivolt-usa.com/` | correct |
| `og:url` | `https://hivolt-usa.com/` | correct |
| **`og:image`** | **`http://hivolt-usa.com/cdn/...`** | **insecure protocol** |
| `twitter:card` | summary_large_image | correct |
| `robots` | absent | indexable, correct |
| **favicon** | **no `<link rel=icon>` emitted at all** | **missing** |

No console errors. No 4xx or 5xx responses. No broken image files. The theme is
technically clean; the defects are content and configuration.

The `og:image` served over `http` on an `https` page is commonly refused or
downgraded by social and messaging previews. `config/settings_data.json` has
`"favicon": ""`, so the browser tab shows a default globe.

## 3. Structured data — live output

The rendered JSON-LD Organization node carries exactly:

```
@type | @id | name | url | email
```

No `legalName`, no `telephone`, no `PostalAddress`, no `contactPoint`. The
enriched 3,371-byte version exists only on the unpublished draft. Because
`settings.logo` is empty, the Organization has no logo either.

## 4. Announcement bar — live text

```
COMPLIMENTARY TRACKED SHIPPING ON ALL US ORDERS
60 DAYS TO RETURN OR EXCHANGE
```

The published refund policy states: **"We do not process direct exchanges."**
The storefront promises a service the policy refuses, on every page.

## 5. Navigation

**Header (`nova-main`) is clean.** 27 collection links, every handle resolves.
Women, Men, Accessories, The Edit, Journal and Help all populate.

**Footer Shop column (`nova-footer-shop`) has four dead links**, and the footer
renders on every page:

| Link | Target | Correct target |
|---|---|---|
| Dresses | `/collections/dresses` | `/collections/dresses-1` |
| Knitwear | `/collections/knitwear` | `/collections/knitwear-sweaters` |
| Coats & Jackets | `/collections/coats-jackets` | `/collections/womens-coats-jackets` |
| Denim | `/collections/denim` | `/collections/jeans-bottoms` |

Footer About and Help columns are entirely valid.

### A contact menu exists but is not wired in

Menu `footer-legal`, titled "Contact", already contains:

- Contact us → `/pages/contact-us`
- `support@hivolt-usa.com` → `mailto:`
- `+1 914-650-2041` → `tel:`

`sections/footer-group.json` renders `nova-footer-shop`, `footer-about` and
`footer-help` — not `footer-legal`. The phone number and email address are one
menu selection away from being visible sitewide.

## 6. Correction to the Fashion Nova comparison

`docs/FASHION-NOVA-SITEWIDE.md` records HIVOLT as having "none" for Track
Order, Help Centre, Size Guide and a shipping page. **That is wrong.** All four
exist, are published, and three already appear in the footer Help column.

17 published pages: Our Mission, Help Center, Shipping & Delivery, 60-Day
Love-It Guarantee, Contact Us, Returns & Refunds, Size Guide, Size Guide —
Women, Size Guide — Men, Terms of Service, Accessibility Statement, Track Your
Order, Materials & Specifications, Care Guide, Payment Policy, Your Privacy
Choices, Google Site Verification.

Four unpublished: Voltcore 2-Piece Set, Fabric Weight Index, Size Guide
(duplicate handle `size-chart`), Privacy at HIVOLT.

The support architecture is largely built. It is under-surfaced, not absent.

## 7. The store carries two identities

| Signal | Says |
|---|---|
| Terms of Service | "technical activewear and gym apparel: tops, bottoms, sports bras, leggings, shorts" |
| Blog title | "Training Journal — Activewear Styling & Workout Guides" (21 articles) |
| Unpublished pages | Voltcore 2-Piece Set, Fabric Weight Index |
| Catalogue | 1,603 products: dresses, coats, men's shirts, boots |
| Navigation | Women / Men / Accessories / The Edit |
| Homepage | The Winter Edit, The Dress Edit, Knitwear |

The Terms also promise fibre composition and g/m² fabric weight published per
style; the general-fashion catalogue does not carry those specs.

This is an activewear brand with a general fashion catalogue layered over it.
Legal terms, blog and product range describe different businesses. Owner
decision: which one is HIVOLT.

## 8. Ranked repair list

| # | Fix | Where | Blocked on |
|---:|---|---|---|
| 1 | Nine broken links on the homepage | theme editor | — |
| 2 | Four broken links in footer Shop menu | Navigation | — |
| 3 | Announcement: remove the exchange promise | theme editor | — |
| 4 | Add `footer-legal` as a fourth footer column | theme editor | — |
| 5 | Favicon | theme settings | 512×512 image |
| 6 | `og:image` to https | theme settings | re-upload asset |
| 7 | Header logo | theme settings | logo file |
| 8 | Enriched Organization schema | staged on draft | publish draft |
| 9 | Social profile links | theme settings | real URLs |
| 10 | Reconcile Terms vs catalogue | policy or catalogue | owner decision |

Items 1, 3 and 8 are already fixed and verified on unpublished draft
`158911987944`. Items 2 and 4 are Navigation and footer settings, outside the
theme file, and must be done in admin either way.

Production theme writes are refused by the connector, which permits
`themeFilesUpsert` on unpublished themes only. No theme was published or
unpublished as a workaround.
