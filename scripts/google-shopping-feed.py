"""Build a Google Shopping primary feed (TSV) from a Shopify bulk export.

Why this exists: HIVOLT has a Merchant Center account (5705286743) and no feed
source, because the Shopify Google & YouTube channel is not installed. That
install is owner-only. A **file-based primary feed** is not — Merchant Center
accepts an uploaded TSV directly, so this bypasses the channel entirely and
gets the catalogue in front of Google without waiting.

It is a stopgap, not the destination. A file feed is a snapshot: the moment a
price or a stock level moves in Shopify, the uploaded feed is stale and Google
starts disapproving offers for mismatching the landing page. Re-run this and
re-upload after any catalogue change, or install the channel and let it sync.

Input is the JSONL from:

    bulkOperationRunQuery { products(query: "status:active") { ... } }

which returns products, variants and metafields as separate lines joined by
`__parentId`. Run with the JSONL path as the only argument.

Two deliberate omissions, both about not asserting things this container cannot
check:

  * **No `google_product_category`.** Google validates it against its own
    taxonomy, and www.google.com is blocked at the proxy here, so the strings
    cannot be verified. The store *does* carry `mc-facebook.google_product_category
    = 5322` — but the same value on all 113 products, covering dresses, skirts
    and varsity jackets alike, is one blanket assignment from the Meta channel
    rather than a per-product judgement. Omitting the field makes Google assign
    it per product from the title and description, which beats a broad ID
    applied to everything. Shopify's own category path goes in `product_type`,
    which is free-text and validated against nothing.
  * **No `gtin` or `mpn`, and `identifier_exists: no`.** These are unbranded
    manufacturer blanks with no manufacturer-assigned identifier. That is
    already what `mm-google-shopping.custom_product: TRUE` says in Shopify, and
    the feed should not contradict the store. It also keeps the offers
    unclustered, so they are never lined up beside the identical blank from a
    cheaper seller.
"""
import csv
import json
import pathlib
import sys
from collections import defaultdict

CURRENCY = "USD"
DOMAIN = "https://hivolt-usa.com"

COLUMNS = [
    "id", "item_group_id", "title", "description", "link", "image_link",
    "additional_image_link", "availability", "price", "sale_price", "brand",
    "condition", "identifier_exists", "product_type", "color", "size",
    "age_group", "gender", "material", "product_highlights",
    "custom_label_0", "custom_label_1",
]


def load(path):
    products, variants, metafields, images = {}, defaultdict(list), defaultdict(dict), defaultdict(list)
    for line in path.read_text().splitlines():
        if not line.strip():
            continue
        d = json.loads(line)
        parent = d.get("__parentId")
        gid = d.get("id", "")
        if "namespace" in d:
            metafields[parent][f"{d['namespace']}.{d['key']}"] = d["value"]
        elif "/ProductVariant/" in gid:
            variants[parent].append(d)
        elif "/Product/" in gid:
            products[gid] = d
        elif parent and "image" in d:
            # A MediaImage line from the product's media connection. Video and
            # model media come through with no `image` key and are skipped.
            url = (d.get("image") or {}).get("url")
            if url:
                images[parent].append(url)
    return products, variants, metafields, images


def gsm_band(gsm):
    """Segment for later campaign bidding. Bands, not raw numbers, because a
    bid strategy wants a handful of buckets rather than twenty values."""
    if not gsm:
        return ""
    n = int(gsm)
    if n < 150:
        return "light"
    if n < 220:
        return "mid"
    if n < 280:
        return "heavy"
    return "heaviest"


def price_band(amount):
    p = float(amount)
    if p < 40:
        return "under-40"
    if p < 60:
        return "40-59"
    if p < 80:
        return "60-79"
    return "80-plus"


def highlights(mf, product_type):
    """2-4 short feature bullets. Google renders these on the listing, and it
    is the only place in the Shopping UI where the published-spec argument
    fits at all. Shipping and returns are deliberately absent — Google asks for
    product features here, not policy.

    In a text feed Google separates repeated values with a **comma**, so a
    comma inside a bullet silently splits it in two. "Composition: 89%
    polyester, 11% spandex" would arrive as two mangled highlights. Every
    internal comma becomes a middot before the join.
    """
    out = []
    gsm = mf.get("spec.gsm")
    if gsm:
        out.append(f"Fabric weight {gsm} g/m2 — published from the mill specification")
    comp = mf.get("spec.composition")
    if comp:
        out.append(f"Composition: {comp}")
    seams = mf.get("spec.seams")
    if seams:
        out.append(f"{seams} seams")
    if product_type:
        out.append(f"{product_type} — unbranded with no printed logo")
    clean = [h.replace(", ", " · ").replace(",", " ·")[:150] for h in out[:10]]
    # Google asks for at least two highlights. A lone bullet is worse than
    # none — it reads as a half-filled field and can trip a feed warning — so
    # products with only one usable fact send the attribute empty.
    return ",".join(clean) if len(clean) >= 2 else ""


def main():
    src = pathlib.Path(sys.argv[1])
    products, variants, metafields, images = load(src)

    # Prefer the SKU as the feed id: it is human-readable in Merchant Center's
    # error reports, which matters when 541 rows come back with one problem.
    # Only if SKUs are not unique does it fall back to the variant id, and it
    # checks rather than assuming.
    skus = [v.get("sku") for vs in variants.values() for v in vs]
    use_sku = all(skus) and len(set(skus)) == len(skus)
    if not use_sku:
        print(f"  SKUs not usable as ids ({len(set(skus))} unique of {len(skus)}) — using variant ids")

    rows, skipped = [], []
    for pid, p in products.items():
        mf = metafields.get(pid, {})
        featured = ((p.get("featuredMedia") or {}).get("image") or {}).get("url", "")
        gallery = [u for u in images.get(pid, []) if u != featured]
        if not featured:
            featured = gallery.pop(0) if gallery else ""
        gsm = mf.get("spec.gsm", "")
        ptype = (p.get("category") or {}).get("fullName", "") or p.get("productType", "")

        for v in variants.get(pid, []):
            if not featured:
                skipped.append((p["handle"], "no image"))
                continue
            opts = {o["name"].lower(): o["value"] for o in v.get("selectedOptions", [])}
            price, compare = v["price"], v.get("compareAtPrice")
            # Google's convention: `price` is the reference, `sale_price` the
            # amount actually charged. Shopify stores it the other way round.
            if compare and float(compare) > float(price):
                listed, sale = compare, price
            else:
                listed, sale = price, ""

            rows.append({
                "id": v["sku"] if use_sku else v["id"].split("/")[-1],
                "item_group_id": p["handle"],
                "title": p["title"][:150],
                "description": " ".join((p.get("description") or "").split())[:5000],
                "link": f"{DOMAIN}/products/{p['handle']}?variant={v['id'].split('/')[-1]}",
                "image_link": featured,
                "additional_image_link": ",".join(gallery[:10]),
                "availability": "in_stock" if v.get("availableForSale") else "out_of_stock",
                "price": f"{float(listed):.2f} {CURRENCY}",
                "sale_price": f"{float(sale):.2f} {CURRENCY}" if sale else "",
                "brand": p.get("vendor", ""),
                "condition": "new",
                "identifier_exists": "no",
                "product_type": ptype,
                "color": opts.get("color", ""),
                "size": opts.get("size", ""),
                "age_group": mf.get("mm-google-shopping.age_group", ""),
                "gender": mf.get("mm-google-shopping.gender", ""),
                "material": mf.get("spec.composition", ""),
                "product_highlights": highlights(mf, p.get("productType", "")),
                "custom_label_0": gsm_band(gsm),
                "custom_label_1": price_band(price),
            })

    # Fail loudly rather than shipping a feed with holes in the fields Google
    # rejects an Apparel offer for.
    required = ["id", "title", "description", "link", "image_link",
                "availability", "price", "brand", "color", "size",
                "age_group", "gender"]
    bad = [(r["id"], c) for r in rows for c in required if not r[c]]
    if bad:
        for i, c in bad[:20]:
            print(f"  MISSING {c:16} on {i}")
        raise SystemExit(f"{len(bad)} missing required values — not writing the feed")

    out = src.parent / "hivolt-google-shopping-feed.tsv"
    with out.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=COLUMNS, delimiter="\t",
                           quoting=csv.QUOTE_MINIMAL, extrasaction="raise")
        w.writeheader()
        w.writerows(rows)

    on_sale = sum(1 for r in rows if r["sale_price"])
    with_hl = sum(1 for r in rows if r["product_highlights"])
    print(f"{len(rows)} offers across {len(products)} products -> {out.name}")
    print(f"  {on_sale} carry a sale_price, {with_hl} carry product_highlights")
    if skipped:
        print(f"  skipped {len(skipped)}: {skipped[:5]}")


if __name__ == "__main__":
    main()
