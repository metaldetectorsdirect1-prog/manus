"""Does the eBay upload file still match live Shopify prices?

    python3 scripts/ebay-price-drift.py <products.jsonl> <ebay-seller-hub-upload.csv>

`ebay-listings.py` writes a file that is correct the moment it is generated and
degrades silently from then on. A price change in Shopify admin does not touch
the CSV, and an eBay listing is a binding offer -- uploading a stale file sells
garments at a number nobody chose. So the file is re-checked against live
prices before every upload rather than trusted because it was right once.

The products.jsonl input is a bulkOperationRunQuery export of:

    products(query: "status:active") { edges { node { id handle
      variants { edges { node { price selectedOptions { name value } } } } } } }

## The join, and the trap in it

Rows are matched on (handle, Size, Color).

**CustomLabel on a variation row is the variant SKU, not the product handle.**
Only the parent row carries the handle. Joining every row on CustomLabel looks
reasonable, runs clean, and compares exactly zero prices while reporting 541
handles as "not live" -- a wrong answer that looks like a catalogue problem.
The handle therefore comes from the parent that opens each group, walking the
file in order.

Mismatches print both numbers. A count on its own is not evidence.
"""
import collections
import csv
import json
import sys


def load_live(path):
    """handle -> {(size, color): price} from a bulk products export."""
    handles, live = {}, collections.defaultdict(dict)
    with open(path) as fh:
        for line in fh:
            if not line.strip():
                continue
            o = json.loads(line)
            gid = o.get("id", "")
            # Metafield rows carry no id when the query did not ask for one.
            if "namespace" in o and "key" in o:
                continue
            if "/ProductVariant/" in gid:
                opts = {x["name"].strip().lower(): x["value"].strip()
                        for x in o.get("selectedOptions", [])}
                live[o["__parentId"]][(opts.get("size", ""),
                                       opts.get("color", ""))] = o["price"]
            elif "/Product/" in gid:
                handles[gid] = o["handle"]
    return {handles[g]: v for g, v in live.items() if g in handles}


def main():
    by_handle = load_live(sys.argv[1])
    rows = list(csv.DictReader(open(sys.argv[2])))

    n_live = sum(len(v) for v in by_handle.values())
    parents = [r for r in rows if not r["Relationship"]]
    varrows = [r for r in rows if r["Relationship"] == "Variation"]
    print(f"live: {len(by_handle)} products, {n_live} variants")
    print(f"file: {len(parents)} parents, {len(varrows)} variation rows\n")

    mismatch, unmatched, unknown = [], [], set()
    checked = 0

    def compare(handle, size, color, filed):
        nonlocal checked
        variants = by_handle.get(handle)
        if variants is None:
            unknown.add(handle)
            return
        got = variants.get((size, color))
        if got is None:
            unmatched.append((handle, size, color))
            return
        checked += 1
        if abs(float(got) - float(filed)) > 0.001:
            mismatch.append((handle, size, color, filed, got))

    current = None
    for r in rows:
        if not r["Relationship"]:
            current = r["CustomLabel"]
            # A single-variant garment is emitted flat, with its price on the
            # parent row; a multi-variant parent carries no price by design.
            if r["*StartPrice"].strip():
                variants = by_handle.get(current)
                if variants and len(variants) == 1:
                    (size, color), _ = next(iter(variants.items()))
                    compare(current, size, color, r["*StartPrice"])
                else:
                    unknown.add(current)
        elif r["Relationship"] == "Variation":
            d = dict(p.split("=", 1)
                     for p in r["RelationshipDetails"].split("|") if "=" in p)
            compare(current, d.get("Size", ""), d.get("Color", ""),
                    r["*StartPrice"])

    print(f"{checked} of {n_live} live variants priced in the file")
    print(f"price mismatches:            {len(mismatch)}")
    for h, s, c, filed, got in mismatch[:25]:
        print(f"   {h:46s} {s:4s} {c:14s} file ${filed:>7s}  live ${got:>7s}")
    if len(mismatch) > 25:
        print(f"   … +{len(mismatch) - 25} more")

    print(f"file rows with no live variant: {len(unmatched)}")
    for h, s, c in unmatched[:10]:
        print(f"   {h} Size={s} Color={c}")
    print(f"handles not live or not active: {len(unknown)}")
    for h in sorted(unknown)[:10]:
        print(f"   {h}")

    stale = mismatch or unmatched or unknown or checked != n_live
    print("\n" + ("REGENERATE before uploading." if stale else
                  "File matches live prices. Safe to upload."))
    return 1 if stale else 0


if __name__ == "__main__":
    sys.exit(main())
