"""Turn the HIVOLT catalogue into marketplace listings.

The store has product, margin and a working checkout, and almost no traffic.
Forty-two days in, ~5 real sessions a day. Shopify's own published figure is that
**over 80% of stores make zero revenue in their first 90 days** — that is the
normal case, not a fault in this store, and no amount of on-site work changes it.

The assets here are a 113-product catalogue at 65.7% gross margin with 1400x1400
photography and published fabric specs. What is missing is an audience. Building
one is the four-year route the comparables took. Renting one is same-week.

So this generates listing files for marketplaces that already have the buyers.

## eBay first, deliberately

Amazon has the traffic — 2.6 billion monthly visits — but its apparel categories
require a **GTIN** (UPC/EAN) per variant, and **541 of 541 variants here carry a
null barcode**. Listing on Amazon therefore needs either purchased GTINs or an
approved GTIN exemption, both of which take days to weeks. eBay accepts
"Does not apply" for GTIN on most apparel, has no monthly fee on the basic tier,
and needs no brand registry. It is the shortest path from this catalogue to a
listing a stranger can buy from.

Both files are generated. eBay is the one that can go up today.

## What a marketplace costs, against what it replaces

Per average unit — $48.89 price, $16.18 cost, $7.00 shipping, from live data:

    own store    48.89 - 16.18 - 7.00 - 1.72 processing  = $23.99   49.1%
    eBay ~13%    48.89 - 16.18 - 7.00 - 6.36 final value = $19.35   39.6%
    Amazon 17%   48.89 - 16.18 - 7.00 - 8.31 referral    = $17.39   35.6%

A third of the margin goes to the platform. That is the entire trade, stated
plainly: **36-40% of something beats 49% of nothing.** The own-store margin is
only better in the counterfactual where traffic exists, and after 42 days it
does not.

The average price is $48.89 rather than the $46.90 quoted before this ran,
because generating the file surfaced five products priced below what the store
charges for every comparable garment — four yoga tank tops at $34 against a
$17.98 unit cost, and a sports bra at $38 against $19.97. They cleared $3-5 a
unit on a marketplace and barely more on the store's own checkout. They are now
at $49 and $54, the rungs the rest of the catalogue already uses for those cost
tiers. That correction is worth more than the export it came out of.

Nothing here is a reason to close the Shopify store. It stays the brand surface
and the place repeat buyers land. The marketplace is where the first hundred
orders come from, and those orders are what produce the reviews, the demand
data and the payment history that every other channel needs and none of which
can be manufactured.
"""
import csv
import html
import json
import pathlib
import re
import sys
import time
from collections import defaultdict

# eBay final value fee for Clothing, Shoes & Accessories, and Amazon's apparel
# referral fee. Amazon's is frozen through 2026. Both are the headline rate; a
# per-order fixed fee is ignored because it does not change the decision.
EBAY_FEE = 0.13
AMAZON_FEE = 0.17
SHIP = 7.00

# A unit that clears less than this is not worth the pick, pack and the return
# risk. It is a flag to reprice, not a rule the script enforces.
THIN = 5.00


def load(econ, spec_path, desc_path):
    """Join the three bulk exports on product id.

    Only ACTIVE products are kept. The catalogue holds 21 archived products
    alongside the 113 live ones, and an archived product still comes back from
    a bulk export — listing one on a marketplace would advertise something the
    store has deliberately stopped selling.
    """
    products, variants = {}, defaultdict(list)
    for line in econ.read_text().splitlines():
        if not line.strip():
            continue
        d = json.loads(line)
        if "handle" in d:
            if d.get("status") != "ACTIVE":
                continue
            products[d["id"]] = d
        elif "price" in d:
            variants[d["__parentId"]].append(d)

    meta = defaultdict(dict)
    for line in spec_path.read_text().splitlines():
        if not line.strip():
            continue
        d = json.loads(line)
        if "key" in d:
            meta[d["__parentId"]][d["key"]] = d["value"]

    desc = {}
    for line in desc_path.read_text().splitlines():
        if not line.strip():
            continue
        d = json.loads(line)
        desc[d["id"]] = d.get("descriptionHtml") or ""

    return products, variants, meta, desc


def plain(raw):
    """Marketplace description fields take text, not markup.

    Two things the naive version got wrong, both visible in the exported CSV:
    the store's `<li>` tags are followed by a newline before the content, so
    stripping tags left a line holding nothing but a bullet; and `<br>` was
    dropped rather than converted, running "no cling." straight into the next
    sentence. Entities go through html.unescape rather than a hand-written
    pair of replacements, which missed &#39; and &quot;.
    """
    t = re.sub(r"<br\s*/?>", "\n", raw, flags=re.I)
    t = re.sub(r"<li>\s*", "\n• ", t, flags=re.I)
    t = re.sub(r"</p>|</h\d>|</ul>|</li>", "\n", t, flags=re.I)
    t = re.sub(r"<[^>]+>", "", t)
    t = html.unescape(t)
    return "\n".join(l.strip() for l in t.split("\n") if l.strip())


def main():
    root = pathlib.Path(sys.argv[1])
    # The economics export is named explicitly rather than defaulted, because
    # the first run of this script used an eight-hour-old export and reported
    # three products as loss-making at $34 when the live price was already $54.
    # Every input's age is printed below for the same reason.
    econ = root / (sys.argv[2] if len(sys.argv) > 2 else "econ.jsonl")
    spec, desc_path = root / "spec.jsonl", root / "desc2.jsonl"
    for f in (econ, spec, desc_path):
        age = (time.time() - f.stat().st_mtime) / 3600
        flag = "  <-- STALE, re-export before trusting" if age > 6 else ""
        print(f"  input {f.name:16s} {age:5.1f}h old{flag}")
    print()
    products, variants, meta, desc = load(econ, spec, desc_path)

    rows, skipped = [], []
    for pid, p in products.items():
        vs = variants.get(pid, [])
        if not vs:
            skipped.append((p["handle"], "no variants"))
            continue
        m = meta.get(pid, {})
        body = plain(desc.get(pid, ""))
        if not body:
            skipped.append((p["handle"], "no description"))
            continue

        for v in vs:
            price = float(v["price"])
            cost_o = (v.get("inventoryItem") or {}).get("unitCost")
            cost = float(cost_o["amount"]) if cost_o else None
            size = colour = ""
            for o in v.get("selectedOptions") or []:
                if o["name"].lower() == "size":
                    size = o["value"]
                elif o["name"].lower() in ("color", "colour"):
                    colour = o["value"]

            rows.append({
                "sku": v.get("sku") or "",
                "handle": p["handle"],
                "title": p["title"],
                "size": size,
                "colour": colour,
                "price": f"{price:.2f}",
                "cost": f"{cost:.2f}" if cost is not None else "",
                "gtin": "Does not apply",   # eBay accepts this; Amazon does not
                "brand": "HIVOLT",
                "condition": "New with tags",
                "gsm": m.get("gsm", ""),
                "composition": m.get("composition", ""),
                "care": m.get("care", ""),
                "description": body,
                "ebay_net": f"{price - (cost or 0) - SHIP - price * EBAY_FEE:.2f}",
                "amazon_net": f"{price - (cost or 0) - SHIP - price * AMAZON_FEE:.2f}",
            })

    if not rows:
        raise SystemExit("no listable variants — refusing to write an empty file")

    out = root / "marketplace-listings.csv"
    with out.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

    priced = [r for r in rows if r["cost"]]
    avg_e = sum(float(r["ebay_net"]) for r in priced) / len(priced)
    avg_a = sum(float(r["amazon_net"]) for r in priced) / len(priced)

    print(f"{len(rows)} listable variants across {len(products)} active products"
          f" -> {out.name}")
    if skipped:
        print(f"{len(skipped)} skipped: {skipped[:5]}")
    print(f"{len(rows) - len(priced)} variants carry no unit cost"
          " and cannot be checked for margin")

    print("\naverage contribution per unit, after platform fee and $7.00 shipping")
    print(f"  eBay   @{EBAY_FEE:.0%}   ${avg_e:6.2f}")
    print(f"  Amazon @{AMAZON_FEE:.0%}   ${avg_a:6.2f}")

    # Report by product, not by variant. Five sizes of one mispriced tee is one
    # decision to make, not five, and printing it five times hid that the whole
    # list was a single product.
    thin = {}
    for r in priced:
        worst = min(float(r["ebay_net"]), float(r["amazon_net"]))
        if worst < THIN and worst < thin.get(r["handle"], (999,))[0]:
            thin[r["handle"]] = (worst, r)
    if thin:
        print(f"\n{len(thin)} products contribute under ${THIN:.2f} on the worse"
              " of the two platforms:")
        for h, (worst, r) in sorted(thin.items(), key=lambda kv: kv[1][0]):
            print(f"  {h:46s} ${r['price']:>6s} cost ${r['cost']:>5s}"
                  f"  eBay ${float(r['ebay_net']):6.2f}  Amzn ${float(r['amazon_net']):6.2f}")
        print("  Reprice these or hold them back from the marketplace feeds.")
    else:
        print(f"\nNo product falls under ${THIN:.2f} on either platform.")

    print("\nGTIN is 'Does not apply' on every row. eBay accepts that on apparel;"
          "\nAmazon does not — it needs purchased GTINs or an approved exemption.")


if __name__ == "__main__":
    main()
