"""Build Google Shopping titles for HIVOLT's active products.

Google matches a shopping query against the `title` attribute harder than
against anything else in the feed, and for Apparel it documents the order
Brand + Gender + Product type + Attributes. Shopify sends `product.title`
straight through with no separate feed field, so the product title *is* the
shopping title — there is nowhere else to put this.

Every title is generated from data already on the product rather than written
by hand, because 113 hand-written strings is exactly where a wrong colour or a
stale weight hides. Input is a TSV of `id, title, colour, gsm` read off the
live store; output is the productUpdate variables.

Two decisions worth keeping:

  * `GSM`, not `g/m²`. The rest of the store says g/m² and should keep saying
    it — but a shopper types "220 gsm leggings", and the title is the one
    surface being matched against what people type. Same number, same claim.
  * A blank gsm column stays blank. The men's training set pairs a 130 g/m²
    tee with 165 g/m² shorts; picking either one for the title would state a
    weight the set does not have.
"""
import json
import pathlib
import sys

SRC = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "products.tsv")
BRAND = "HIVOLT"
LIMIT = 150  # Google's hard cap; the tile shows roughly the first 70


def build(title, colour, gsm):
    """Brand + the product's own name + colour + weight, in that order."""
    base = title.replace("’", "'").strip()

    # Several titles already end in "- Black" or "- White & Green", which would
    # otherwise repeat the moment the colour is appended. Strip only when the
    # tail really is the colour, so a product legitimately named "... - Long"
    # keeps its suffix.
    if " - " in base:
        head, _, tail = base.rpartition(" - ")
        if tail.replace(" & ", "/").strip().lower() == colour.strip().lower():
            base = head.strip()

    parts = [f"{BRAND} {base}", colour]
    if gsm:
        parts.append(f"{gsm} GSM")
    return ", ".join(parts)


def main():
    rows, out = [], []
    for line in SRC.read_text().splitlines():
        if not line.strip():
            continue
        pid, title, colour, *rest = line.split("\t")
        rows.append((pid, title, colour, (rest[0] if rest else "").strip()))

    seen = {}
    for pid, title, colour, gsm in rows:
        new = build(title, colour, gsm)
        if len(new) > LIMIT:
            raise SystemExit(f"over {LIMIT} chars: {new}")
        # A duplicate title makes two offers compete with each other for the
        # same query instead of covering two.
        if new in seen:
            raise SystemExit(f"duplicate title: {new}\n  {seen[new]} and {pid}")
        seen[new] = pid
        out.append({"id": f"gid://shopify/Product/{pid}", "title": new})

    longest = max(out, key=lambda o: len(o["title"]))
    print(f"{len(out)} titles, all unique, longest {len(longest['title'])} chars")
    print(f"  {longest['title']}")
    (SRC.parent / "titles.json").write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
