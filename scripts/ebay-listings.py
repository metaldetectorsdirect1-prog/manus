"""Turn the HIVOLT catalogue into an eBay Seller Hub Reports upload file.

`marketplace-export.py` proved the economics work. This produces the file a
person can actually upload, which is a different and stricter problem.

## What changed since File Exchange

eBay File Exchange is being retired in favour of **Seller Hub -> Reports**,
which takes the same CSV dialect. The rules that shape this script:

* the `*Action` column must come first, and carries the site/currency header
* `C:`-prefixed columns are the category's Item Specifics
* every listing needs a **leaf category id**, which cannot be derived from a
  Shopify product type — see config/ebay-categories.json

## Variations, and why they matter commercially

541 variants as 541 separate listings would blow through the free insertion
allowance and bury the store in duplicates. eBay's multi-variation format
collapses them to **one listing per garment** with a size/colour matrix:

    parent row     Relationship empty, RelationshipDetails "Size=S;M;L|Color=Black",
                   StartPrice and Quantity empty
    variation row  Relationship "Variation", RelationshipDetails "Size=M|Color=Black",
                   with its own StartPrice and Quantity

A garment with a single variant is emitted as a plain listing instead, because
a one-value variation matrix is rejected.

## Three things eBay will remove a listing for

Handled here rather than discovered after a takedown:

1. **Links to an off-eBay store.** The product copy links to the fabric index
   and the returns page on hivolt-usa.com. Anchors are unwrapped to their text
   and bare URLs stripped.
2. **Contact details in the listing body.** support@hivolt-usa.com appears in
   some copy; email addresses are removed.
3. **Titles over 80 characters**, which are truncated on eBay's side at a word
   boundary nobody chose. Over-length titles are reported, not silently cut.

## What it does not do

It does not invent a category id, and it does not upload. Uploading needs the
owner's seller account.
"""
import csv
import html
import json
import pathlib
import re
import sys
from collections import defaultdict

SITE = "*Action(SiteID=US|Country=US|Currency=USD|Version=1193|CC=UTF-8)"

# Terms that must match what the store already publishes. The shipping policy
# says free on every US order; the refund policy says 60 days, unworn with
# tags, and that HIVOLT provides the return label. ShippingCostPaidByOption
# therefore has to be Seller, not Buyer.
LOCATION = "Willowbrook, IL 60527"
DISPATCH_DAYS = 4          # policy says dispatched in 2-4 business days
RETURN_DAYS = "Days_60"
CONDITION_NEW_WITH_TAGS = 1000
TITLE_MAX = 80

COLUMNS = [
    SITE, "CustomLabel", "*Category", "*Title", "Relationship",
    "RelationshipDetails", "*Description", "*ConditionID", "PicURL",
    "*Quantity", "*Format", "*StartPrice", "*Duration", "Location",
    "DispatchTimeMax", "ReturnsAcceptedOption", "ReturnsWithinOption",
    "RefundOption", "ShippingCostPaidByOption", "ShippingType",
    "ShippingService-1:Option", "ShippingService-1:Cost",
    "C:Brand", "C:Size", "C:Color", "C:Department", "C:Type",
    "C:Material", "C:Size Type",
]

EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+")
BARE_URL = re.compile(r"https?://\S+|(?<![\w@.])(?:www\.)?hivolt-usa\.com\S*")


def gender_of(tags):
    for g in ("unisex", "womens", "mens"):
        if g in tags:
            return g
    return "unknown"


def clean_description(raw):
    """eBay-safe HTML: no off-site links, no contact details."""
    t = re.sub(r"</?a\b[^>]*>", "", raw, flags=re.I)   # unwrap, keep the text
    t = EMAIL.sub("", t)
    t = BARE_URL.sub("", t)
    # The copy sometimes says "see the Fabric Weight Index" next to the link it
    # just lost. Left as prose: it reads as a reference, not a dead pointer.
    return html.unescape(t).strip()


def load(root, econ_name):
    econ = root / econ_name
    products, variants = {}, defaultdict(list)
    for line in econ.read_text().splitlines():
        if not line.strip():
            continue
        d = json.loads(line)
        if "handle" in d:
            if d.get("status") == "ACTIVE":
                products[d["id"]] = d
        elif "price" in d:
            variants[d["__parentId"]].append(d)

    desc = {}
    for line in (root / "desc2.jsonl").read_text().splitlines():
        if line.strip():
            d = json.loads(line)
            desc[d["id"]] = d.get("descriptionHtml") or ""

    spec = defaultdict(dict)
    for line in (root / "spec.jsonl").read_text().splitlines():
        if line.strip():
            d = json.loads(line)
            if "key" in d:
                spec[d["__parentId"]][d["key"]] = d["value"]

    media, mtags = defaultdict(list), {}
    for line in (root / "media2.jsonl").read_text().splitlines():
        if not line.strip():
            continue
        d = json.loads(line)
        if "handle" in d:
            mtags[d["id"]] = (d.get("productType") or "", d.get("tags") or [])
        elif "image" in d:
            media[d["__parentId"]].append(d["image"]["url"])

    return products, variants, desc, spec, media, mtags


def options_of(variant):
    size = colour = ""
    for o in variant.get("selectedOptions") or []:
        n = o["name"].lower()
        if n == "size":
            size = o["value"]
        elif n in ("color", "colour"):
            colour = o["value"]
    return size, colour


def base_row(cat, title, desc, pics):
    return {
        SITE: "Add",
        "*Category": cat,
        "*Title": title,
        "*Description": desc,
        "*ConditionID": CONDITION_NEW_WITH_TAGS,
        "PicURL": "|".join(pics[:12]),
        "*Format": "FixedPrice",
        "*Duration": "GTC",
        "Location": LOCATION,
        "DispatchTimeMax": DISPATCH_DAYS,
        "ReturnsAcceptedOption": "ReturnsAccepted",
        "ReturnsWithinOption": RETURN_DAYS,
        "RefundOption": "MoneyBack",
        "ShippingCostPaidByOption": "Seller",
        "ShippingType": "Flat",
        "ShippingService-1:Option": "USPSGround",
        "ShippingService-1:Cost": "0.00",
        "C:Brand": "HIVOLT",
        "C:Size Type": "Regular",
    }


def main():
    root = pathlib.Path(sys.argv[1])
    econ_name = sys.argv[2] if len(sys.argv) > 2 else "econ.jsonl"
    cfg = json.loads(pathlib.Path("config/ebay-categories.json").read_text())
    cats, departments = cfg["categories"], cfg["department"]
    # Per-handle, and they win. 'unisex:Jersey' covers four soccer jerseys and
    # three generic training jerseys; one id for both would mis-file three.
    overrides = cfg.get("overrides", {})

    products, variants, desc, spec, media, mtags = load(root, econ_name)

    rows, unresolved, long_titles, skipped = [], defaultdict(list), [], []

    for pid, p in sorted(products.items(), key=lambda kv: kv[1]["handle"]):
        vs = variants.get(pid, [])
        ptype, tags = mtags.get(pid, ("", []))
        g = gender_of(tags)
        key = f"{g}:{ptype}"
        pics = media.get(pid, [])

        if not vs or not pics:
            skipped.append((p["handle"], "no variants" if not vs else "no image"))
            continue

        category = overrides.get(p["handle"]) or cats.get(key)
        if category is None:
            unresolved[key].append(p["handle"])
            continue

        title = p["title"]
        if len(title) > TITLE_MAX:
            long_titles.append((p["handle"], len(title), title))

        m = spec.get(pid, {})
        body = clean_description(desc.get(pid, ""))
        if not body:
            skipped.append((p["handle"], "no description"))
            continue

        common = base_row(category, title, body, pics)
        common.update({
            "C:Department": departments.get(g, ""),
            "C:Type": ptype,
            "C:Material": m.get("composition", ""),
        })

        sizes, colours = [], []
        for v in vs:
            s, c = options_of(v)
            if s and s not in sizes:
                sizes.append(s)
            if c and c not in colours:
                colours.append(c)

        # A variation matrix needs at least one axis with two or more values.
        multi = len(vs) > 1 and (len(sizes) > 1 or len(colours) > 1)

        if multi:
            axes = []
            if sizes:
                axes.append("Size=" + ";".join(sizes))
            if colours:
                axes.append("Color=" + ";".join(colours))
            parent = dict(common)
            parent.update({
                "CustomLabel": p["handle"],
                "Relationship": "",
                "RelationshipDetails": "|".join(axes),
                "*Quantity": "",
                "*StartPrice": "",
            })
            rows.append(parent)

            for v in vs:
                s, c = options_of(v)
                detail = []
                if s:
                    detail.append(f"Size={s}")
                if c:
                    detail.append(f"Color={c}")
                child = dict(common)
                # Variation rows carry only what differs. Title, description
                # and pictures live on the parent; repeating them here is what
                # makes eBay treat each row as its own listing.
                for strip in ("*Title", "*Description", "PicURL", "*Category"):
                    child[strip] = ""
                child.update({
                    "CustomLabel": v.get("sku") or f"{p['handle']}-{s}{c}",
                    "Relationship": "Variation",
                    "RelationshipDetails": "|".join(detail),
                    "*Quantity": 25,
                    "*StartPrice": f"{float(v['price']):.2f}",
                    "C:Size": s,
                    "C:Color": c,
                })
                rows.append(child)
        else:
            v = vs[0]
            s, c = options_of(v)
            single = dict(common)
            single.update({
                "CustomLabel": v.get("sku") or p["handle"],
                "Relationship": "",
                "RelationshipDetails": "",
                "*Quantity": 25,
                "*StartPrice": f"{float(v['price']):.2f}",
                "C:Size": s,
                "C:Color": c,
            })
            rows.append(single)

    listings = sum(1 for r in rows if r["Relationship"] != "Variation")

    if unresolved:
        need = sum(len(v) for v in unresolved.values())
        print(f"{len(unresolved)} category ids are still null, covering "
              f"{need} of {len(products)} products:\n")
        for k in sorted(unresolved):
            print(f'  "{k}": {len(unresolved[k])} products '
                  f"(e.g. {unresolved[k][0]})")
        print("\nFill them in config/ebay-categories.json and re-run.")

    if not rows:
        raise SystemExit(
            "\nNo listable rows — every product's category is still null, and "
            "this script will not invent one. Nothing written.")

    out = root / "ebay-seller-hub-upload.csv"
    with out.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=COLUMNS, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow({c: r.get(c, "") for c in COLUMNS})

    print(f"\n{listings} listings / {len(rows)} rows -> {out.name}")
    if skipped:
        print(f"{len(skipped)} products skipped: {skipped[:5]}")
    if long_titles:
        print(f"\n{len(long_titles)} titles exceed eBay's {TITLE_MAX} characters "
              "and would be cut mid-phrase. Shorten these rather than let eBay "
              "choose where:")
        for h, n, t in sorted(long_titles, key=lambda x: -x[1])[:10]:
            print(f"  {n:3d}  {h}\n       {t}")

    print("\nBefore uploading: Seller Hub -> Reports -> Uploads takes this file "
          "directly.\nQuantity is set to 25 per variation, not the 1,000 the "
          "store carries — a\nnew seller account has a selling limit and 1,000 "
          "would breach it on day one.")


if __name__ == "__main__":
    main()
