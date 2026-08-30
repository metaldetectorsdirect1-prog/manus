# HIVOLT-ANALYTICS-IMPLEMENTATION.md — design before install, 2026-08-28

Current state: no pixels installed (layout verified clean; app installs not
present/visible). **Nothing is installed by this plan.** GA4 installation is
Decision C in the owner package.

## Architecture

One collection layer: **Shopify Customer Events (Web Pixels)**. GA4 via the
official Google & YouTube channel pixel; Meta/TikTok later via their
official channel pixels only. No hardcoded tags in theme.liquid — the theme
emits DOM CustomEvents; a single custom web pixel relays them. This
prevents the classic duplicate-purchase problem (checkout events come only
from the protected pixel context).

## Event map

| Event | Trigger | Parameters | Shopify source | GA4 | Meta | TikTok | Consent | Duplicate risk |
|---|---|---|---|---|---|---|---|---|
| page_view | route render | page_type | standard pixel | page_view | PageView | Pageview | analytics | low — one pixel only |
| view_item_list | collection/search grid render | list_id, items[] | standard `collection_viewed` | view_item_list | ViewCategory | ViewContent(list) | analytics | low |
| select_item | product card click | item_id, list_id | custom (theme emit) | select_item | — | ClickButton | analytics | low |
| view_item | PDP render | item_id, price, currency | standard `product_viewed` | view_item | ViewContent | ViewContent | analytics | low |
| search | search submit | query | standard `search_submitted` | search | Search | Search | analytics | low |
| search_no_results | results page, count 0 | query | custom | search (results=0) | — | — | analytics | low |
| filter_apply | S&D filter change | filter_name, value | custom | custom event | — | — | analytics | low |
| size_guide_open | size-guide open | item_id | custom (when guide exists) | custom | — | — | analytics | low |
| variant_select | variant change | variant_id | custom | custom | — | — | analytics | low |
| variant_unavailable | sold-out selected | variant_id | custom | custom | — | — | analytics | low |
| add_to_cart | ATC / Quick Add | item, qty, value | standard `product_added_to_cart` | add_to_cart | AddToCart | AddToCart | marketing? no — analytics; ad platforms need marketing consent | MEDIUM — never also fire from theme JS |
| remove_from_cart | cart line remove | item | standard | remove_from_cart | — | — | analytics | low |
| view_cart | cart/drawer open | value, items | standard `cart_viewed` | view_cart | — | — | analytics | low |
| begin_checkout | checkout entry | value, items | standard `checkout_started` | begin_checkout | InitiateCheckout | InitiateCheckout | marketing for ads | MEDIUM — pixel-only |
| purchase | order complete | transaction_id, value, tax, shipping, items | standard `checkout_completed` | purchase | Purchase | CompletePayment | marketing for ads | **HIGH if any tag duplicates — forbid non-pixel purchase tags** |
| add_to_wishlist | wishlist provider event | item | provider | add_to_wishlist | AddToWishlist | AddToWishlist | analytics | provider-dependent |
| back_in_stock_request | BIS form submit | variant_id | provider | custom | Lead | SubmitForm | marketing (contact capture) | provider-dependent |
| complete_the_look_add | ATC from CTL module | item, source_item | custom | add_to_cart(source=ctl) | AddToCart | AddToCart | as ATC | pass source param, not a second event |

Consent categories per Shopify Customer Privacy API: analytics vs
marketing; ad-platform pixels must respect marketing consent; GA4 in
analytics. No consent claim is made until the consent surface is configured
(legal review item).

## Installation recommendation (on approval)

1. Owner creates GA4 property; installs Google & YouTube channel; links Ads.
2. Verify standard events flow (DebugView) before any custom events.
3. Add one custom web pixel for the custom events above; theme emits
   `document.dispatchEvent(new CustomEvent('hivolt:<event>', {detail}))`
   from the relevant components (small, additive theme change — prepared on
   the workbench only after the pixel exists to receive them).
4. Meta/TikTok pixels only when those channels are actually planned.
