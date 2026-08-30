"""Generate the fabric-weight index page from published spec metafields.

HIVOLT's one defensible asset is that it publishes the fabric weight of every
garment, taken from the mill specification. That data currently exists only
scattered across 113 product pages, where nothing can quote it as a whole and
Google sees 113 unrelated documents.

This turns it into one page that is:

  * **Citable.** An AI answering "how heavy are HIVOLT leggings" or "what is a
    good gsm for activewear" needs a passage that states the range and the
    comparison in one place. 109 products, 91-380 g/m², in a single sorted
    table, is that passage. No competitor publishes the equivalent, so there is
    nothing for a model to prefer over it.
  * **An internal-link hub.** 109 links to product pages from one document.
    Products currently sit several clicks from the homepage and take roughly
    one session a day between them.
  * **Crawlable.** A plain table of 109 linked rows, which is what a model
    extracts anyway — no duplicate structured data restating the markup.

Price is deliberately not a column. Building this surfaced two 380 g/m²
varsity jackets priced $42 and $74 — a real inconsistency that was invisible
while the numbers sat on 113 separate pages, and one the owner has to resolve.
Until they do, a weight-versus-price table would publicly disprove the exact
"the number justifies the price" argument the page exists to make. The product
links carry price anyway.

Every number is read from the `spec.*` metafields, which were themselves taken
from the supplier sheet. Nothing here is computed, rounded or inferred — a
product with no published weight is listed as such rather than estimated, which
is the whole point of the page.

Input is the JSONL from a bulkOperationRunQuery over active products with their
spec metafields. Writes page-body HTML to stdout or a file.
"""
import html
import json
import pathlib
import sys
from collections import defaultdict

# The bands the store already prices against, so the page explains the ladder
# a shopper actually meets rather than inventing a new scale.
BANDS = [
    (300, "Heavyweight", "Outerwear and fleece-backed layers. Structure you can feel."),
    (240, "Substantial", "Opaque under load without stiffness. Where most of the leggings sit."),
    (180, "Mid", "Everyday training weight. Moves more than it holds."),
    (0, "Light", "Hot-weather and summer-session fabrics. Built to breathe."),
]


def band(gsm):
    for floor, name, _ in BANDS:
        if gsm >= floor:
            return name
    return "Light"


def load(path):
    products, metafields = {}, defaultdict(dict)
    for line in path.read_text().splitlines():
        if not line.strip():
            continue
        d = json.loads(line)
        if "handle" in d:
            products[d["id"]] = d
        elif "key" in d:
            metafields[d["__parentId"]][d["key"]] = d["value"]

    rows, unpublished = [], []
    for pid, p in products.items():
        mf = metafields.get(pid, {})
        gsm = mf.get("gsm", "")
        entry = {
            "handle": p["handle"],
            "title": p["title"],
            "composition": mf.get("composition", ""),
            "price": float(p["priceRangeV2"]["minVariantPrice"]["amount"]),
            "category": (p.get("category") or {}).get("fullName", "").split(" > ")[-1],
        }
        if gsm.isdigit():
            rows.append({**entry, "gsm": int(gsm)})
        else:
            unpublished.append(entry)

    rows.sort(key=lambda r: (-r["gsm"], r["title"]))
    unpublished.sort(key=lambda r: r["title"])
    return rows, unpublished


def build(rows, unpublished):
    e = html.escape
    heaviest, lightest = rows[0], rows[-1]
    out = []
    add = out.append

    add("<p><strong>Every fabric weight HIVOLT sells, in one table.</strong> "
        f"{len(rows)} garments, from {lightest['gsm']} to {heaviest['gsm']} g/m², "
        "each figure taken from the supplier's specification sheet rather than "
        "estimated or rounded.</p>")

    add("<h2>What g/m² means</h2>"
        "<p>Grams per square metre is how much fabric is actually there. It is "
        "the number that governs whether a legging stays opaque through a deep "
        "squat, whether a tee clings when it is wet, and whether a hoodie holds "
        "its shape. Almost no activewear brand publishes it. We publish all of "
        "it, including the numbers that are not flattering.</p>")

    add("<h2>The weight bands</h2><table><thead><tr><th>Band</th><th>Range</th>"
        "<th>What it means</th><th>Products</th></tr></thead><tbody>")
    for floor, name, meaning in BANDS:
        n = sum(1 for r in rows if band(r["gsm"]) == name)
        # BANDS is ordered descending, so `next(... if f > floor)` returns 300
        # every time and prints "180-299" for a band that ends at 239. The
        # ceiling is the *smallest* floor above this one.
        higher = [f for f, _, _ in BANDS if f > floor]
        ceiling = min(higher) - 1 if higher else None
        rng = f"{floor}+ g/m²" if ceiling is None else f"{floor}–{ceiling} g/m²"
        add(f"<tr><td><strong>{e(name)}</strong></td><td>{e(rng)}</td>"
            f"<td>{e(meaning)}</td><td>{n}</td></tr>")
    add("</tbody></table>")

    add(f"<h2>All {len(rows)} published weights, heaviest first</h2>"
        "<table><thead><tr><th>Weight</th><th>Product</th><th>Type</th>"
        "<th>Composition</th></tr></thead><tbody>")
    for r in rows:
        add(f"<tr><td><strong>{r['gsm']} g/m²</strong></td>"
            f"<td><a href=\"/products/{e(r['handle'])}\">{e(r['title'])}</a></td>"
            f"<td>{e(r['category'])}</td><td>{e(r['composition'])}</td></tr>")
    add("</tbody></table>")

    if unpublished:
        add("<h2>Published without a fabric weight</h2>"
            "<p>These carry a supplier composition but no g/m² figure. We do not "
            "convert from another unit and we do not estimate — a converted "
            "number is not a quotation. They are listed here rather than left "
            "out, because a gap you can see is worth more than a table that "
            "looks complete.</p><ul>")
        for r in unpublished:
            add(f"<li><a href=\"/products/{e(r['handle'])}\">{e(r['title'])}</a>"
                f" — {e(r['composition']) or 'composition not published'}</li>")
        add("</ul>")

    # No ItemList JSON-LD here. It was drafted carrying position + url, and once
    # the names came out as duplicates of the table it held nothing a crawler
    # could not read straight off the anchors. Structured data that restates the
    # visible markup is weight, not signal — the weights and compositions that
    # matter are already Product schema on each target page.
    return "\n".join(out)


def main():
    src = pathlib.Path(sys.argv[1])
    rows, unpublished = load(src)
    if not rows:
        raise SystemExit("no published weights found — refusing to write an empty index")
    body = build(rows, unpublished)
    out = src.parent / "fabric-index.html"
    out.write_text(body)
    print(f"{len(rows)} weighted rows, {len(unpublished)} without a weight "
          f"-> {out.name} ({len(body)} bytes)")


if __name__ == "__main__":
    main()
