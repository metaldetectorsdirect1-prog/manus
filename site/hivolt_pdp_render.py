#!/usr/bin/env python3
"""Render the HIVOLT PDP snippets outside Shopify.

The storefront is not reachable from this environment, so every check runs the
real snippet files through a real Liquid engine against fixture drops. This
module owns the engine and the render helpers; the assertions live in
site/check-hivolt-pdp.py and the browser page in site/render-pdp-preview.py, so
both look at exactly the same output.

The Shopify filters below are deliberately thin. Each does the least that lets
the template under test run, so a passing assertion is about our Liquid rather
than about a clever stub.
"""
import json
import pathlib

from liquid import DictLoader, Environment

ROOT = pathlib.Path(__file__).resolve().parent.parent
THEME = ROOT / "site" / "theme-v7"
SNIPPETS = THEME / "snippets"
ASSETS = THEME / "assets"

SHOP_URL = "https://hivolt-usa.com"


# ---------------------------------------------------------------------------
# Shopify filters python-liquid does not ship
# ---------------------------------------------------------------------------
_STRINGS = {
    "products.product.sold_out": "Sold out",
    "products.general.size_chart": "Size chart",
    "products.general.size_trigger": "size",
    "products.general.color_swatch_trigger": "color",
}


def f_t(value, *a, **k):
    return _STRINGS.get(str(value), str(value))


def f_image_url(value, *a, **k):
    return str(value)


def f_handleize(value, *a, **k):
    out = "".join(c if c.isalnum() else "-" for c in str(value).lower())
    while "--" in out:
        out = out.replace("--", "-")
    return out.strip("-")


def f_json(value, *a, **k):
    return json.dumps(value)


def f_money(value, *a, **k):
    return f"${int(value) / 100:.2f}"


def make_env():
    env = Environment(loader=DictLoader(
        {p.stem: p.read_text() for p in SNIPPETS.glob("*.liquid")}))
    for name, fn in (("t", f_t), ("image_url", f_image_url),
                     ("handleize", f_handleize), ("json", f_json),
                     ("money", f_money), ("img_url", f_image_url)):
        env.filters[name] = fn
    return env


# ---------------------------------------------------------------------------
# Render helpers
# ---------------------------------------------------------------------------
def swatches(env, product, option, option_index=1, section_id="main", form_id="f"):
    return env.get_template("hivolt-swatches").render(
        product=product, option=option, option_index=option_index,
        section_id=section_id, form_id=form_id, block={"settings": {}})


def size_guide(env, product, part, **kw):
    return env.get_template("hivolt-size-guide").render(
        product=product, part=part, **kw)


def spec_table(env, product, **kw):
    return env.get_template("hivolt-spec-table").render(product=product, **kw)


def feed_title(env, product, variant=None, fmt="plain"):
    return env.get_template("hivolt-feed-title").render(
        product=product, variant=variant, format=fmt).strip()


def identifier(env, product, variant, fmt="mode"):
    return env.get_template("hivolt-identifier").render(
        product=product, variant=variant, format=fmt)


def ld_context(**over):
    """The page-level globals the structured-data snippet reads."""
    ctx = {
        "request": {"page_type": "product"},
        "shop": {"url": SHOP_URL, "name": "HIVOLT", "currency": "USD"},
        "cart": {"currency": {"iso_code": "USD"}},
        "settings": {
            "favicon": None,
            "social_facebook_link": "https://facebook.com/hivolt",
            "social_instagram_link": "",
            "social_youtube_link": "",
            "social_tiktok_link": "",
            "social_pinterest_link": "",
        },
        "template": {"suffix": ""},
        "canonical_url": f"{SHOP_URL}/products/qa-fixture-pique-polo",
        "collection": {}, "page": {}, "blog": {}, "article": {},
    }
    ctx.update(over)
    return ctx


def structured_data(env, **over):
    """Render the JSON-LD and return (raw_html, parsed_object).

    Parsing here rather than in each test means a malformed document fails
    every structured-data assertion at once instead of producing a confusing
    substring mismatch.
    """
    raw = env.get_template("hivolt-structured-data").render(**ld_context(**over))
    body = raw.split(">", 1)[1].rsplit("</script>", 1)[0]
    return raw, json.loads(body)


def graph_node(data, node_type):
    for node in data["@graph"]:
        if node["@type"] == node_type:
            return node
    return None


# ---------------------------------------------------------------------------
# Standalone preview page, used by the browser QA pass
# ---------------------------------------------------------------------------
PREVIEW_CHROME = """
body { margin:0; font-family:-apple-system,"Helvetica Neue",Arial,sans-serif;
       color:#111; background:#fff; }
.wrap { max-width:640px; margin:0 auto; padding:20px 20px 60px; }
.qa-banner { background:#111; color:#fff; padding:10px 20px; font-size:12px;
             letter-spacing:.08em; text-transform:uppercase; }
.lbl { font-size:11px; letter-spacing:.12em; text-transform:uppercase;
       color:#767676; margin:26px 0 10px; }
.nul { font-size:13px; color:#767676; font-style:italic; }
.visually-hidden { position:absolute!important; width:1px; height:1px; margin:-1px;
  padding:0; overflow:hidden; clip:rect(0 0 0 0); white-space:nowrap; border:0; }
.hide { display:none; }
.variant-wrapper { margin:0 0 4px; }
.variant__label { display:block; font-size:12px; letter-spacing:.08em;
  text-transform:uppercase; color:#767676; margin:0 0 8px; }
"""


def preview_html(env, product, title="HIVOLT PDP fixture"):
    """One page carrying every component this work introduced.

    It is not a replica of the Shopify PDP — it is the components in isolation
    against the real CSS, which is what the viewport and dialog checks need.
    """
    blocks = []
    for i, option in enumerate(product.get("options_with_values") or [], start=1):
        blocks.append(
            f'<div class="lbl">Option: {option["name"]}</div>'
            f'<div class="variant-wrapper">'
            f'<span class="variant__label">{option["name"]}</span>'
            f'{swatches(env, product, option, option_index=i)}</div>')

    trigger = size_guide(env, product, "trigger").strip()
    dialog = size_guide(env, product, "dialog").strip()
    specs = spec_table(env, product).strip()

    blocks.append('<div class="lbl">Size guide</div>' +
                  (trigger or '<div class="nul">no chart data - renders nothing</div>'))
    blocks.append('<div class="lbl">Specification</div>' +
                  (specs or '<div class="nul">no spec data - renders nothing</div>'))

    css = (ASSETS / "hivolt-pdp.css").read_text()
    js = (ASSETS / "hivolt-size-guide.js").read_text()

    return f"""<!doctype html>
<html class="js" lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<style>
{css}
{PREVIEW_CHROME}
</style>
</head>
<body>
<div class="qa-banner">QA fixture &mdash; not real product data</div>
<main class="wrap">
<h1 class="lbl" style="font-size:18px;letter-spacing:0;text-transform:none;color:#111">{product['title']}</h1>
{"".join(blocks)}
</main>
{dialog}
<script>{js}</script>
</body>
</html>
"""
