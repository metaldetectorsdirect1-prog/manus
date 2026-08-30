# HIVOLT-EMPTY-COLLECTION-AUDIT.md — fresh read 2026-08-28

15 collections exist. 2 populated (all, knitwear — 4 products each). 13
empty: 11 still published to Online Store, 2 already unpublished. Several
are also published to **Google & YouTube** and **AfterShip for TikTok**
channels — empty collections syndicated to external surfaces.

**Live-store defect found (report only — live nav is a global,
customer-facing resource):** the LIVE theme's footer menu links
"The Polo Collection" (/collections/mens-golf-polos) and "The Championship
Capsule" (/collections/long-sleeve-golf-polos) — both collections are now
UNPUBLISHED, so the live footer serves 404s today. Fixing it means editing
the live "footer" menu → owner approval (included in the package below).

| ID | Title | Handle | Published? | Products | Live nav link? | Dev nav link? | Indexable? | Keep for future? | Recommendation |
|---|---|---|---|---|---|---|---|---|---|
| 448200114408 | Women's & Men's Apparel | all | Online Store + Shop | 4 | live footer "Shop all" | no | yes | yes (canonical /all) | KEEP |
| 450083651816 | Knitwear | knitwear | Online Store + Shop | 4 | no | staged (post-publication) | yes | yes | KEEP |
| 449024033000 | Women's Activewear | womens-activewear | OS + Shop + AfterShip | 0 | no | no | yes (empty page) | no (category retired) | UNPUBLISH → DELETE LATER |
| 449024065768 | Tops | tops | OS + Shop + AfterShip | 0 | no | no | yes | yes (Phase-5 fashion) | UNPUBLISH → NEEDS PRODUCTS |
| 449024131304 | Hoodies & Sweats | outerwear-hoodies | OS + Shop + AfterShip | 0 | no | no | yes | maybe (rename "Outerwear"?) | UNPUBLISH → RENAME later |
| 449283326184 | Sports Bras | sports-bras | OS + AfterShip + **Google & YouTube** | 0 | no | no | yes | no | UNPUBLISH (incl. G&Y) → DELETE LATER |
| 449283358952 | Leggings | leggings | OS + AfterShip + **Google & YouTube** | 0 | no | no | yes | no | UNPUBLISH (incl. G&Y) → DELETE LATER |
| 449283391720 | Shorts | shorts | OS + AfterShip + **Google & YouTube** | 0 | no | no | yes | no | UNPUBLISH (incl. G&Y) → DELETE LATER |
| 449718714600 | Sets | sets | OS + POS + Manus | 0 | no | no | yes | yes ("Matching sets" Phase-5) | UNPUBLISH → NEEDS PRODUCTS |
| 450068513000 | Dresses | dresses | OS + Shop | 0 | no | no | yes | yes (Phase-5) | UNPUBLISH → NEEDS PRODUCTS |
| 450068545768 | Loungewear | loungewear | OS + Shop | 0 | no | no | yes | maybe | UNPUBLISH → HOLD |
| 450083619048 | Coats & Jackets | coats-jackets | OS + Shop | 0 | no | no | yes | yes (Phase-5) | UNPUBLISH → NEEDS PRODUCTS |
| 450083684584 | Denim | denim | OS + Shop | 0 | no | no | yes | yes (Phase-5) | UNPUBLISH → NEEDS PRODUCTS |
| 450293465320 | The Polo Collection | mens-golf-polos | **unpublished** | 0 | **YES — live footer → 404** | no | no | no | DELETE LATER + fix live footer link |
| 450293498088 | The Championship Capsule | long-sleeve-golf-polos | **unpublished** | 0 | **YES — live footer → 404** | no | no | no | DELETE LATER + fix live footer link |

## SINGLE AUTHORIZATION PACKAGE (owner: approve as one block)

> "Approved: unpublish the 11 empty published collections listed above from
> Online Store (and from Google & YouTube / AfterShip where published);
> remove the two golf links from the live footer menu; deletion of retired
> activewear/golf collections may follow after 30 days."

## Execution record — 2026-08-28 authorized pass

Owner approved Decision B. Outcome:

- **Collection unpublishing: BLOCKED BY CONNECTOR.** `publishableUnpublish`
  is refused by the MCP server's safety policy ("Unpublishing is blocked to
  prevent accidental storefront catalog removal") — independent of owner
  authorization. Zero collection writes occurred (spot-check read-backs
  confirm all publication states unchanged). No workaround was attempted.
  **Smallest owner action (~2 min):** Admin → Products → Collections →
  select the 11 rows above → make unavailable on Online Store, Shop, and
  where listed, Google & YouTube / AfterShip / POS / Facebook & Instagram.
- **Live footer 404s: FIXED + read-back verified.** Before: "Shop" column
  parent and two children pointed at the unpublished golf collections
  (mens-golf-polos, long-sleeve-golf-polos) — three 404 targets. After:
  parent "Shop" → /collections/all, single child "Shop all" →
  /collections/all; golf items removed; every other footer destination
  re-verified published (shipping-delivery ✓, terms-of-service ✓). Menu
  item IDs preserved; nothing replaced with unrelated filler.
- `/pages/size-guide` links were NOT touched: the page is published (stale
  golf content — a Decision-F rewrite item, not a 404).

| Menu item | Before | After |
|---|---|---|
| Shop (parent) | /collections/mens-golf-polos (404) | /collections/all |
| The Polo Collection | /collections/mens-golf-polos (404) | **removed** |
| The Championship Capsule | /collections/long-sleeve-golf-polos (404) | **removed** |
| Shop all | /collections/all | unchanged |
| all other items | verified published destinations | unchanged |
