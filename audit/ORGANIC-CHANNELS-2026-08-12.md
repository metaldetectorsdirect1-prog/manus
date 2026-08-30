# Where organic traffic can actually come from

2026-08-12. Asked to find organic traffic, find solutions, and add repos or
skills. The skills answer is at the bottom and it is short.

## First, what the content channel is actually doing

47 search sessions landed on blog articles in **60 days**, spread across 40+
different articles at 1–3 each. That is roughly **one click per article per two
months**. The content is indexed and ranking; it is ranking at position 30–80,
which is what a 42-day-old domain with no backlinks earns.

Seven of those 47 are perfume queries hitting **deleted** articles from the
business that previously ran on this domain. The domain still has more search
authority for perfume than for activewear.

Content is not a lever anyone can pull this quarter. It compounds over 6–12
months or it does nothing. Writing more of it now changes nothing.

## The channel that fits this business

HIVOLT sells supplier-sourced garments, US-only, with no reviews, no on-camera
talent and no audience. That rules out every channel that needs a brand and
points at the ones where **the product finds the buyer** rather than the buyer
finding the brand.

### 1. Google Shopping free listings — the whole thing is one owner action

Verified today on the Shopify side, and it is clean:

* **113 of 113** active products are published to the Google & YouTube channel
* **0** active products are missing from it
* feed attributes complete — brand, leaf category, colour, size, gender,
  age_group, `custom_product`

Nothing in Shopify is blocking this. The gate is entirely inside Merchant
Center, and it is absolute: **an unverified, unclaimed account cannot appear in
organic shopping results at all.** Once the domain is claimed and shipping is
configured, product review runs **24–72 hours**, and matching is driven by feed
quality rather than keywords — which is the part that is already done.

This is the highest-intent traffic available to the store, it costs nothing per
click, and it is one screen of work.

**Do it in the Google & YouTube channel's own Merchant Center account
(5838274874), not the older manual one (5705286743).** Two accounts claiming one
domain suppress offers on a claim conflict, which looks identical to a feed
problem and is not one.

### 2. Microsoft / Bing Shopping — nearly free once #1 is done

Microsoft Merchant Center imports the feed directly from Google Merchant
Center, so the setup cost after #1 is close to zero. Competition for the same
queries is far lower. Bing already sends this store traffic. The live theme
already carries a `bing_site_verification` field, so verification is a paste.

Nobody has set this up, and it is the cheapest incremental channel on the list.

### 3. TikTok Shop — installed, never connected

AfterShip for TikTok is an installed publication and
`get-sales-channel-stores` still returns `[]`, so no seller account is
attached. TikTok Shop is product discovery inside the app: the algorithm puts
products in front of buyers without the brand needing its own audience. That
matters here, because the brand's own TikTok presence has produced **zero**
referrals from twelve films.

### 4. Pinterest — the only brand channel that needs no talent

Not set up at all. It fits the constraints better than anything else on the
list: it uses assets the store already has, needs nobody on camera, and its
traffic is durable — a pin can keep driving visits for **12–24 months**, against
a TikTok video's few days. Pinterest also sends **33% more referral traffic to
e-commerce than Facebook**, and its users arrive planning a purchase rather than
scrolling. Realistic first traction is about **90 days**.

One caveat worth taking seriously: the format that works is **lifestyle imagery
at 2:3 (1000×1500)**, not product-on-white. This catalogue is product shots. The
gap is the same one TikTok exposed — no photography of a person wearing the
garment.

There is no Pinterest API in this container, so this is owner setup.

## Ranked

| | Channel | Owner work | First traffic | Blocked on |
|---|---|---|---|---|
| 1 | Google Shopping free listings | one screen | 24–72h after claim | domain claim + shipping in MC |
| 2 | Microsoft/Bing Shopping | ~15 min | days | #1 first |
| 3 | TikTok Shop | account signup | weeks | seller account |
| 4 | Pinterest | ongoing | ~90 days | account + lifestyle imagery |
| 5 | The 501 articles | none | 6–12 months | already running |

The first three are all product-discovery channels, all already installed as
Shopify apps, and all blocked on the same kind of owner action. That is the real
finding: **the store is not short of channels or capability. Three channels are
installed and switched off.**

## On adding repos and skills

~202 skills are installed (`scripts/seo-skills-setup.sh` reproduces them), plus
18 seo-* subagents. None of them will produce a sale, and installing more will
not either. The store's problem has not been capability for some time — every
technical surface that can be fixed from here has been fixed. What is left is
three account setups that require a signed-in browser.

Nothing new was installed today, deliberately. It would have been activity, not
progress.

## Sources

* Google Merchant Center product review timing and the unverified-account rule —
  <https://webappick.com/how-long-does-it-take-for-products-to-show-on-google-shopping/>,
  <https://support.google.com/merchants/answer/13889434>,
  <https://digitalcommerce.com/google-merchant-center-for-organic-traffic/>
* Pinterest pin longevity, referral share and new-account timelines —
  <https://limelightmarketing.com/blogs/pinterest-marketing-tips/>,
  <https://www.outfy.com/blog/pinterest-seo/>,
  <https://marylumley.com/pinterest-for-e-commerce/>
