#!/usr/bin/env python3
"""Render-validate the JSON-LD emitted by the theme's structured-data sources.

Executes the actual shipped Liquid (sections/hivolt-structured-data.liquid via
its repo mirror, plus the Product block in fashion-pdp-info.liquid) with a
minimal Liquid interpreter that supports exactly the constructs those files
use, then json.loads() every <script type="application/ld+json"> produced.
Every page type and conditional branch is exercised. Exit 1 on any invalid
JSON or missing required key.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SD = (ROOT / "impulse-rebuild/theme/fashion/hivolt-structured-data.liquid").read_text()
PDP = (ROOT / "impulse-rebuild/theme/fashion/fashion-pdp-info.liquid").read_text()

FILTERS = {
    "json": lambda v, a=None: json.dumps(v),
    "append": lambda v, a: str(v) + str(a),
    "prepend": lambda v, a: str(a) + str(v),
    "strip_html": lambda v, a=None: re.sub(r"<[^>]+>", "", str(v)),
    "truncate": lambda v, a: (str(v)[: int(a) - 3] + "...") if len(str(v)) > int(a) else str(v),
    "date": lambda v, a: "2026-08-01T09:00:00+0000",  # fixture timestamp
    "image_url": lambda v, a: f"//cdn.example/{v}?width={a}",
    "divided_by": lambda v, a: (float(v) / float(a)) if "." in str(a) else int(v) // int(a),
}


def liquid_value(expr, ctx):
    expr = expr.strip()
    if expr.startswith("'") and expr.endswith("'"):
        return expr[1:-1]
    if re.fullmatch(r"-?\d+(\.\d+)?", expr):
        return float(expr) if "." in expr else int(expr)
    cur = ctx
    for part in expr.split("."):
        if isinstance(cur, dict) and part in cur:
            cur = cur[part]
        elif part == "first" and isinstance(cur, list):
            cur = cur[0] if cur else None
        elif part == "size":
            cur = len(cur) if cur is not None else 0
        else:
            return None
    return cur


def run_filter(name, val, arg, ctx):
    a = liquid_value(arg, ctx) if arg is not None else None
    return FILTERS[name](val, a)


def eval_output(expr, ctx):
    parts = [p.strip() for p in expr.split("|")]
    val = liquid_value(parts[0], ctx)
    for f in parts[1:]:
        m = re.match(r"(\w+)(?::\s*(.+))?$", f)
        name, arg = m.group(1), m.group(2)
        if name == "image_url":  # image_url: width: N
            arg = re.sub(r"^width:\s*", "", arg)
        val = run_filter(name, val, arg, ctx)
    return str(val)


def eval_cond(cond, ctx):
    cond = cond.strip()
    if " and " in cond:
        return all(eval_cond(c, ctx) for c in cond.split(" and "))
    m = re.match(r"(.+?)\s*(==|!=)\s*(.+)", cond)
    if m:
        left = liquid_value(m.group(1), ctx)
        rexpr = m.group(3).strip()
        right = None if rexpr == "blank" else liquid_value(rexpr, ctx)
        if rexpr == "blank":
            ok = left is None or left == "" or left == []
            return ok if m.group(2) == "==" else not ok
        return (left == right) if m.group(2) == "==" else (left != right)
    if " and " in cond:
        return all(eval_cond(c, ctx) for c in cond.split(" and "))
    v = liquid_value(cond, ctx)
    return bool(v)


def render(src, ctx):
    src = re.sub(r"\{%-?\s*comment\s*-?%\}.*?\{%-?\s*endcomment\s*-?%\}", "", src, flags=re.S)
    src = re.sub(r"\{%\s*schema\s*%\}.*?\{%\s*endschema\s*%\}", "", src, flags=re.S)
    src = re.sub(r"\{%\s*style\s*%\}.*?\{%\s*endstyle\s*%\}", "", src, flags=re.S)

    # assigns
    for m in re.finditer(r"\{%-?\s*assign\s+(\w+)\s*=\s*([\w.\']+)\s*-?%\}", src):
        ctx[m.group(1)] = liquid_value(m.group(2), ctx)
    src = re.sub(r"\{%-?\s*assign[^%]*-?%\}", "", src)

    # resolve if/elsif/else blocks (innermost first)
    tag = re.compile(
        r"\{%-?\s*if\s+(?P<c>[^%]+?)\s*-?%\}(?P<body>(?:(?!\{%-?\s*(?:if|endif))[\s\S])*?)\{%-?\s*endif\s*-?%\}"
    )

    def resolve_if(m):
        chunks = re.split(r"\{%-?\s*elsif\s+([^%]+?)\s*-?%\}|\{%-?\s*else\s*-?%\}", m.group("c") and ("" ) or "")
        return ""  # placeholder, replaced below

    def resolve_block(cond, body):
        # split body on elsif/else at this level
        parts = re.split(r"\{%-?\s*elsif\s+([^%]+?)\s*-?%\}", body)
        # parts: [seg0, cond1, seg1, cond2, seg2 ...]
        conds = [cond] + [parts[i] for i in range(1, len(parts), 2)]
        segs = [parts[0]] + [parts[i] for i in range(2, len(parts), 2)]
        # trailing else inside last seg
        for i, c in enumerate(conds):
            seg = segs[i]
            else_split = re.split(r"\{%-?\s*else\s*-?%\}", seg)
            if eval_cond(c, ctx):
                return else_split[0]
            if i == len(conds) - 1 and len(else_split) > 1:
                return else_split[1]
        return ""

    pattern = re.compile(
        r"\{%-?\s*if\s+([^%]+?)\s*-?%\}((?:(?!\{%-?\s*if\s)[\s\S])*?)\{%-?\s*endif\s*-?%\}"
    )
    prev = None
    while prev != src:
        prev = src
        src = pattern.sub(lambda m: resolve_block(m.group(1), m.group(2)), src, count=1)

    # for loops over product.media (pdp-info image array) — fixture: render one item
    src = re.sub(
        r"\{%\s*for\s+media\s+in\s+product\.media[^%]*%\}(.*?)\{%\s*endfor\s*%\}",
        lambda m: m.group(1).replace("{% unless forloop.last %},{% endunless %}", ""),
        src,
        flags=re.S,
    )
    src = re.sub(r"\{%-?\s*unless[^%]*%\}.*?\{%-?\s*endunless\s*-?%\}", "", src, flags=re.S)

    # outputs
    src = re.sub(r"\{\{-?\s*(.+?)\s*-?\}\}", lambda m: eval_output(m.group(1), ctx), src)
    return src


def scripts_of(html):
    return re.findall(r'<script type="application/ld\+json">\s*(.*?)\s*</script>', html, flags=re.S)


BASE = {
    "shop": {"url": "https://hivolt-usa.com"},
    "request": {"origin": "https://hivolt-usa.com"},
    "settings": {"favicon": "shop_images/hivolt-favicon.png"},
    "cart": {"currency": {"iso_code": "USD"}},
}

CASES = []
# index, favicon set and unset
CASES.append(("index favicon-set", SD, {**BASE, "request": {"page_type": "index", "origin": "x"}}, ["Organization", "WebSite"]))
CASES.append(("index favicon-unset", SD, {**BASE, "settings": {"favicon": None}, "request": {"page_type": "index"}}, ["Organization", "WebSite"]))
# product with and without collection
prod = {"title": 'Elena "Relaxed" Sweater', "url": "/products/elena", "collections": [{"title": "Knitwear", "url": "/collections/knitwear"}]}
CASES.append(("product with collection", SD, {**BASE, "request": {"page_type": "product"}, "product": prod}, ["BreadcrumbList"]))
CASES.append(("product no collection", SD, {**BASE, "request": {"page_type": "product"}, "product": {**prod, "collections": []}}, ["BreadcrumbList"]))
# collection with/without description
col = {"title": "Knitwear", "url": "/collections/knitwear", "description": "<p>Soft & warm — the \"good\" stuff.</p>"}
CASES.append(("collection with description", SD, {**BASE, "request": {"page_type": "collection"}, "collection": col}, ["BreadcrumbList", "CollectionPage"]))
CASES.append(("collection no description", SD, {**BASE, "request": {"page_type": "collection"}, "collection": {**col, "description": ""}}, ["BreadcrumbList", "CollectionPage"]))
# page
CASES.append(("page", SD, {**BASE, "request": {"page_type": "page"}, "page": {"title": 'Help "Center"'}}, ["BreadcrumbList"]))
# blog
CASES.append(("blog", SD, {**BASE, "request": {"page_type": "blog"}, "blog": {"title": "Training Journal", "url": "/blogs/news"}}, ["BreadcrumbList"]))
# article with/without image+author
art = {"title": "Layering 101 — a \"how to\"", "url": "/blogs/news/layering", "image": "art.jpg", "published_at": "x", "author": "HIVOLT Team"}
CASES.append(("article full", SD, {**BASE, "request": {"page_type": "article"}, "blog": {"title": "Training Journal", "url": "/blogs/news"}, "article": art}, ["BreadcrumbList", "Article"]))
CASES.append(("article minimal", SD, {**BASE, "request": {"page_type": "article"}, "article": {**art, "image": None, "author": None}}, ["BreadcrumbList", "Article"]))
# cart/search/404 must emit nothing
for pt in ["cart", "search", "404", "password", "list-collections"]:
    CASES.append((f"{pt} emits nothing", SD, {**BASE, "request": {"page_type": pt}}, []))

# fashion-pdp-info Product JSON-LD
pdp_ctx = {
    **BASE,
    "product": {
        "title": 'Elena "Relaxed" Sweater',
        "url": "/products/elena",
        "description": "<p>Soft merino & cotton.</p>",
        "featured_media": {"preview_image": "img1"},
        "media": [{"preview_image": "img1.jpg"}],
        "selected_or_first_available_variant": {"sku": "HV-ELENA-S"},
        "price_min": 6800,
        "price_max": 7400,
        "variants": [1, 2, 3],
        "available": True,
        "metafields": {"spec": {}, "hivolt": {}, "judgeme": {"review_widget_data": {"value": {"number_of_reviews": 0}}}},
    },
    "request": {"page_type": "product", "origin": "https://hivolt-usa.com"},
}
CASES.append(("pdp-info Product", PDP, pdp_ctx, ["Product"]))
pdp_soldout = json.loads(json.dumps(pdp_ctx))
pdp_soldout["product"]["available"] = False
pdp_soldout["product"]["selected_or_first_available_variant"]["sku"] = None
CASES.append(("pdp-info Product sold-out no-sku", PDP, pdp_soldout, ["Product"]))

failures = 0
for name, src, ctx, expected in CASES:
    try:
        out = render(src, dict(ctx))
        blocks = scripts_of(out)
        types = []
        for b in blocks:
            data = json.loads(b)  # raises on invalid JSON
            types.append(data.get("@type"))
            if data.get("@type") == "Product":
                offers = data["offers"]
                assert offers["@type"] == "AggregateOffer" and "lowPrice" in offers and "priceCurrency" in offers
                assert "aggregateRating" not in data and "review" not in data
            if data.get("@type") == "BreadcrumbList":
                items = data["itemListElement"]
                assert items[0]["name"] == "Home" and items[0]["position"] == 1
                assert all(items[i]["position"] == i + 1 for i in range(len(items)))
        missing = [t for t in expected if t not in types]
        extra_when_none = types if not expected else []
        if missing or extra_when_none:
            print(f"FAIL {name}: types={types} missing={missing}")
            failures += 1
        else:
            print(f"ok   {name}: {types}")
    except Exception as e:  # noqa: BLE001
        print(f"FAIL {name}: {type(e).__name__}: {e}")
        failures += 1

print(f"\n{'FAIL' if failures else 'PASS'} — {len(CASES) - failures}/{len(CASES)} JSON-LD render cases valid")
sys.exit(1 if failures else 0)
