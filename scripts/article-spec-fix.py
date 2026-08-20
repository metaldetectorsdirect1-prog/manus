"""Reconcile the blog's fabric claims with the specs the product pages publish.

HIVOLT's whole argument is "published, not claimed". 501 blog articles were
generated in bulk, and a third of them state a fabric weight or a fibre
composition that disagrees with the product's own `spec.*` metafields. A brand
that publishes two different compositions for the same garment has not made the
argument — it has disproved it, and it has done so in the exact places an AI
search engine reads.

Three defects, and only the first three are mechanical. This script fixes those
and refuses to touch the fourth.

  1. **Wrong g/m².** Article says 220, the metafield says 250. The metafield is
     the supplier sheet, so the article is wrong.
  2. **Wrong composition.** Same, per fibre. `spandex` and `elastane` are the
     same fibre, as are `nylon` and `polyamide`, so only the percentages
     disagree — and they do, by up to 72 points.
  3. **Links to archived products.** 180 anchors point at products that no
     longer exist. Shopify will not let you redirect the path while the
     archived product still owns the handle, so the link itself has to move.
     The anchor text moves with it — a link reading "High-Waisted Yoga
     Leggings" that lands on ankle leggings is a second lie stacked on the fix.
  4. **Specs for products that publish none.** NOT FIXED HERE, on purpose. The
     articles state a weight for garments whose metafields are empty. Some are
     conversions of a figure the product does publish in another unit; the rest
     have no visible source at all. Deciding between "backfill the metafield"
     and "delete the claim" needs the supplier sheet, which is the owner's.
     They are listed in the report instead.

Rewriting a number near a link is only safe when the number is a claim *about
that product*. "look for 200 g/m² and up" sitting in the same paragraph is
advice, not a spec, and rewriting it to match the nearest product would corrupt
correct copy. GUARD_BEFORE/GUARD_AFTER hold the phrasings that mark a number as
general guidance; anything they match is left alone and counted as skipped.

Reads the JSONL from a bulkOperationRunQuery over articles and another over
active products with their spec metafields. Writes a JSONL of
`{"id", "article": {"body"}}` for changed articles only, ready for
bulkOperationRunMutation, plus a report of every edit it made.
"""
import csv
import json
import pathlib
import re
import sys
from collections import Counter, defaultdict

# Archived handle -> the closest active product. Chosen by name and category,
# not automatically: "High-Waisted Yoga Leggings" and "Women's High Waisted
# Ankle Leggings" are the same garment renamed, while "Contrast Trim Raglan
# Varsity Jacket" only has a two-tone sibling left. A wrong guess here sends a
# reader to the wrong garment, which is worse than the 404 it replaces.
REDIRECTS = {
    "high-waisted-yoga-leggings": "women-s-high-waisted-ankle-leggings",
    "women-s-high-waisted-yoga-leggings": "women-s-high-waisted-ankle-leggings",
    "womens-high-waist-tapered-leggings": "women-s-high-waisted-ankle-leggings",
    "mens-lightweight-training-t-shirt": "mens-lightweight-performance-t-shirt",
    "high-waisted-blend-biker-shorts": "women-s-high-waisted-pocket-biker-shorts",
    "women-s-high-rise-ankle-length-leggings": "womens-high-rise-ankle-length-leggings",
    "men-s-performance-regular-fit-t-shirt": "mens-regular-fit-performance-t-shirt",
    "men-s-regular-fit-training-t-shirt": "mens-regular-fit-performance-t-shirt",
    "women-s-high-waisted-ankle-length-yoga-leggings": "womens-high-rise-ankle-length-yoga-leggings",
    "womens-hollow-out-yoga-tank-top": "womens-yoga-tank-top",
    "contrast-trim-raglan-varsity-jacket": "two-tone-raglan-sleeve-varsity-jacket",
    "women-s-high-rise-flared-yoga-pants": "womens-high-rise-flared-yoga-pants",
    "women-s-halter-cropped-sports-bra": "womens-halter-yoga-sports-bra",
    "womens-high-waist-yoga-shorts": "womens-high-rise-yoga-shorts",
    "women-s-halter-color-block-yoga-sports-bra": "womens-color-block-yoga-sports-bra",
    "womens-high-rise-pocket-yoga-shorts-1": "womens-high-rise-pocket-yoga-shorts",
    "women-s-pleated-halter-sports-bra": "womens-ruched-halter-neck-sports-bra",
    "women-s-high-rise-color-block-yoga-shorts-1": "women-s-high-rise-color-block-yoga-shorts",
    "womens-high-rise-color-block-yoga-shorts": "women-s-high-rise-color-block-yoga-shorts",
    "womens-color-block-yoga-tank-top-1": "womens-color-block-yoga-tank-top",
    "womens-high-waist-color-block-yoga-shorts": "women-s-high-rise-color-block-yoga-shorts",
}

# Trade names for one fibre. Comparing "24% spandex" against "22% elastane" as
# different fibres would report every garment in the catalogue as mismatched.
FIBRE = {
    "spandex": "elastane", "elastane": "elastane", "lycra": "elastane",
    "nylon": "polyamide", "polyamide": "polyamide",
    "polyester": "polyester", "cotton": "cotton",
    "viscose": "viscose", "rayon": "viscose", "modal": "modal",
}

LINK = re.compile(r'<a href="/products/([a-z0-9\-]+)"([^>]*)>(.*?)</a>')
GSM = re.compile(r'(\d{2,3})(\s*)(g/m²|gsm|GSM|g/m2)')
# Percentages carry decimals ("61.9% cotton"). Matching only \d{1,3} pulls the
# fraction digits out as their own number and invents a "1% polyester" claim
# that is nowhere in the copy.
PCT = re.compile(r'(\d{1,3}(?:\.\d+)?)\s*%\s*([a-zA-Z]+)')
# A whole composition phrase, so it can be replaced as a unit. Patching one
# percentage inside a blend is what produces "100% polyester, 8% spandex".
RUN = re.compile(r'\d{1,3}(?:\.\d+)?\s*%\s*[a-zA-Z]+'
                 r'(?:\s*(?:,|/|and|with)\s*\d{1,3}(?:\.\d+)?\s*%\s*[a-zA-Z]+)*')
# Garments cut from two different fabrics publish both, panel by panel. There
# is no single blend to compare a sentence against, so these are never touched.
MULTI_FABRIC = re.compile(r'·|Fabric [AB]|Main\b|Contrast\b|Shell\b|Lining\b|Bra and|Bra \d',
                          re.I)

GUARD_BEFORE = re.compile(
    r"(look for|at least|above|below|under|over|around|roughly|minimum|maximum|"
    r"aim for|target|between|anything|start(ing)? at|upwards of|north of)"
    r"[^.]{0,40}$", re.I)
GUARD_AFTER = re.compile(r"^\s*(and up|or heavier|or more|or above|plus\b|\+)", re.I)

# How far after a link a number is still plausibly about that product. Long
# enough for "the X is 88% polyester at 240 g/m²", short enough that the next
# sentence about a different garment is out of range.
WINDOW = 300


def load_specs(path):
    """handle -> {gsm, comp, title} from the product bulk export."""
    products, metafields = {}, defaultdict(dict)
    for line in path.read_text().splitlines():
        if not line.strip():
            continue
        d = json.loads(line)
        if "handle" in d:
            products[d["id"]] = d
        elif "key" in d:
            metafields[d["__parentId"]][d["key"]] = d["value"]
    return {
        p["handle"]: {
            "gsm": metafields.get(pid, {}).get("gsm", ""),
            "comp": metafields.get(pid, {}).get("composition", ""),
            "title": p["title"],
        }
        for pid, p in products.items()
    }


def short_name(title):
    """"HIVOLT Women's High Waisted Ankle Leggings, Black, 220 GSM" -> the name.

    Anchor text carries the colour and weight only by accident of the Google
    Shopping title rewrite; in a sentence it reads as noise.
    """
    name = re.sub(r"^HIVOLT\s+", "", title)
    name = re.sub(r",\s*\d+\s*GSM\s*$", "", name, flags=re.I)
    name = re.sub(r",\s*[A-Z][\w/ ’'-]*$", "", name)
    return name.strip()


def fibre_map(text):
    """"80% nylon, 20% spandex" -> {"polyamide": "80", "elastane": "20"}.

    Returns None when any token is not a fibre. "stretches by 30% more" parses
    as a percentage of something called "more"; treating that as a composition
    would rewrite a sentence about stretch into a fabric blend.
    """
    out = {}
    for pct, fib in PCT.findall(text):
        key = FIBRE.get(fib.lower())
        if key is None:
            return None
        out[key] = pct
    return out or None


def guarded(window, match):
    """True when this number reads as general advice rather than a spec."""
    return bool(GUARD_BEFORE.search(window[:match.start()])
                or GUARD_AFTER.match(window[match.end():]))


def fix_body(body, spec, log):
    """Return the corrected body. `log` collects one tuple per edit."""

    # 1. Archived links first, so the window logic that follows sees the real
    #    target and validates the numbers against the product now being linked.
    def relink(m):
        handle, attrs, text = m.group(1), m.group(2), m.group(3)
        target = REDIRECTS.get(handle)
        if not target:
            return m.group(0)
        name = short_name(spec[target]["title"]) if target in spec else text
        log.append(("link", handle, re.sub("<[^>]+>", "", text), f"{name} ({target})"))
        return f'<a href="/products/{target}"{attrs}>{name}</a>'

    body = LINK.sub(relink, body)

    # 2. Numbers, per link window. Rebuilt left to right because every edit
    #    shifts the offsets of everything after it.
    hits = list(LINK.finditer(body))
    out, cursor = [], 0
    for i, m in enumerate(hits):
        stop = hits[i + 1].start() if i + 1 < len(hits) else len(body)
        w_start = m.end()
        w_end = min(stop, w_start + WINDOW)
        heading = body.find("<h2", w_start, w_end)
        if heading != -1:
            w_end = heading
        if w_end <= cursor:
            continue

        out.append(body[cursor:w_start])
        window = body[w_start:w_end]
        s = spec.get(m.group(1))

        if s:
            if s["gsm"]:
                def fix_gsm(g):
                    if g.group(1) == s["gsm"] or guarded(window, g):
                        return g.group(0)
                    log.append(("gsm", m.group(1), f"{g.group(1)} g/m²",
                                f'{s["gsm"]} g/m²'))
                    return f'{s["gsm"]}{g.group(2)}{g.group(3)}'
                window = GSM.sub(fix_gsm, window)

            if s["comp"] and not MULTI_FABRIC.search(s["comp"]):
                real = fibre_map(s["comp"])

                def fix_comp(r):
                    claimed = fibre_map(r.group(0))
                    # Not a composition, or already right, or it names a fibre
                    # this garment does not contain — in which case the sentence
                    # is about something else and is not ours to rewrite.
                    if (not real or not claimed or claimed == real
                            or not set(claimed) & set(real)):
                        return r.group(0)
                    # "Below about 15% spandex, leggings restrict a squat" is
                    # advice about knits in general that happens to sit near a
                    # product link. Swapping the garment's blend into it yields
                    # "Below about 78% polyamide, 22% elastane".
                    if guarded(window, r):
                        return r.group(0)
                    log.append(("comp", m.group(1), r.group(0), s["comp"]))
                    return s["comp"]
                window = RUN.sub(fix_comp, window)

        out.append(window)
        cursor = w_end

    out.append(body[cursor:])
    return "".join(out)


def main():
    articles_path, specs_path = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
    blog_handle = sys.argv[3] if len(sys.argv) > 3 else "news"
    spec = load_specs(specs_path)

    missing = [h for h in REDIRECTS.values() if h not in spec]
    if missing:
        raise SystemExit(f"redirect targets are not active products: {missing}")

    articles = [json.loads(l) for l in articles_path.read_text().splitlines() if l.strip()]
    out_path = articles_path.parent / "articles-fixed.jsonl"
    report_path = articles_path.parent / "articles-fix-report.txt"

    # A substitution that lands next to a stray fibre word leaves text like
    # "78% polyamide, 22% elastane/elastane". Guards are meant to prevent it;
    # this is the check that the guards actually did.
    MANGLED = re.compile(r'%\s*([a-zA-Z]+)\s*/\s*\1|%\s*[a-zA-Z]+\s*,\s*'
                         r'\d{1,3}(?:\.\d+)?\s*%\s*[a-zA-Z]+\s*/\s*[a-zA-Z]+', re.I)

    changed, edits, report, artifacts = 0, Counter(), [], []
    with out_path.open("w") as fh:
        for a in articles:
            body = a.get("body") or ""
            log = []
            fixed = fix_body(body, spec, log)
            if fixed == body:
                continue
            for m in MANGLED.finditer(fixed):
                if not MANGLED.search(body[max(0, m.start() - 80):m.end() + 80]):
                    artifacts.append(f"{a['handle']}: ...{fixed[m.start()-60:m.end()+40]}...")
            changed += 1
            for kind, handle, was, now in log:
                edits[kind] += 1
                report.append(f"{a['handle']}\t{kind}\t{handle}\t{was!r} -> {now!r}")
            fh.write(json.dumps({"id": a["id"], "article": {"body": fixed}}) + "\n")

    if artifacts:
        for a in artifacts[:20]:
            print("ARTIFACT", a, file=sys.stderr)
        raise SystemExit(f"{len(artifacts)} rewrites left mangled text — refusing to write")

    # Two carriers for the same corrections. The JSONL is what
    # bulkOperationRunMutation consumes and is the route to prefer — one call,
    # every article, no spreadsheet in the middle. Where that mutation is
    # unavailable, the CSV is a Matrixify "Blog Posts" import: it matches on ID
    # and rewrites Body HTML, leaving every other field alone.
    csv_path = articles_path.parent / "articles-fixed-matrixify.csv"
    by_id = {a["id"]: a for a in articles}
    with csv_path.open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["ID", "Handle", "Blog: Handle", "Command", "Body HTML"])
        for line in out_path.read_text().splitlines():
            d = json.loads(line)
            w.writerow([d["id"].rsplit("/", 1)[-1], by_id[d["id"]]["handle"],
                        blog_handle, "UPDATE", d["article"]["body"]])

    report_path.write_text("\n".join(report) + "\n")
    print(f"{changed} of {len(articles)} articles changed -> {out_path.name}")
    print(f"                              -> {csv_path.name}")
    for kind, n in sorted(edits.items()):
        print(f"  {kind:5s} {n}")
    print(f"{len(report)} edits logged -> {report_path.name}")


if __name__ == "__main__":
    main()
