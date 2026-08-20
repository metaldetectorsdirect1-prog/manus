#!/usr/bin/env python3
"""Render the HIVOLT PDP snippets against mock data and assert what they emit.

parse-liquid.py proves the templates parse. This proves they behave: that the
size guide disappears when there are no measurements, that a swatch with no
colour data falls back to text instead of guessing a CSS colour, that the
structured data is valid JSON and never carries a rating or an invented
identifier, and that the unit conversion is right.

The storefront is not reachable from this environment, so this is where the
behaviour gets checked before a human previews the theme.

Run:  python3 site/check-hivolt-pdp.py
"""
import json
import pathlib
import sys
from collections.abc import Mapping

from liquid import Environment
from liquid import DictLoader

SNIPPETS = pathlib.Path("site/theme-v7/snippets")


# --------------------------------------------------------------------------
# Shopify filters python-liquid does not ship. Deliberately thin: each one does
# the least that lets the template under test run, so a passing assertion is
# about our Liquid, not about a clever stub.
# --------------------------------------------------------------------------
def f_t(value, *a, **k):
    return {"products.product.sold_out": "Sold out",
            "products.general.size_chart": "Size chart",
            "products.general.size_trigger": "size"}.get(str(value), str(value))


def f_image_url(value, *a, **k):
    return str(value)


def f_handleize(value, *a, **k):
    return str(value).lower().replace(" ", "-")


def f_json(value, *a, **k):
    return json.dumps(value)


def f_money(value, *a, **k):
    return f"${int(value) / 100:.2f}"


class OptionValue(Mapping):
    """Behaves like Shopify's product_option_value: a string with attributes."""

    def __init__(self, name, available=True, selected=False, swatch=None):
        self._d = {"name": name, "available": available, "selected": selected,
                   "swatch": swatch or {}}

    def __getitem__(self, k):
        return self._d[k]

    def __iter__(self):
        return iter(self._d)

    def __len__(self):
        return len(self._d)

    def __str__(self):
        return self._d["name"]


def make_env():
    env = Environment(loader=DictLoader(
        {p.stem: p.read_text() for p in SNIPPETS.glob("*.liquid")}))
    for name, fn in (("t", f_t), ("image_url", f_image_url),
                     ("handleize", f_handleize), ("json", f_json),
                     ("money", f_money), ("img_url", f_image_url)):
        env.filters[name] = fn
    return env


def mf(value):
    """A metafield drop: the template always reads `.value`."""
    return {"value": value}


CHART_CM = {
    "title": mf("Pique polo - unisex adult"),
    "measurement_basis": mf("garment_flat"),
    "source_unit": mf("cm"),
    "columns": mf([{"key": "chest", "label": "Chest"},
                   {"key": "length", "label": "Length"}]),
    "rows": mf([{"size": "S", "values": {"chest": 51, "length": 70}},
                {"size": "M", "values": {"chest": 54}},
                {"size": "L", "values": {}}]),
    "note": mf("Measured flat across the chest, one inch below the armhole."),
    "source_reference": mf("supplier tech pack 2026-08"),
}


def product(**over):
    base = {
        "id": 999, "title": "HIVOLT Pique Polo", "handle": "hivolt-pique-polo",
        "url": "/products/hivolt-pique-polo", "vendor": "HIVOLT",
        "description": "A polo.", "images": [], "variants": [],
        "has_only_default_variant": False, "empty?": False,
        "selected_or_first_available_variant": None,
        "metafields": {"spec": {}, "custom": {}},
    }
    base.update(over)
    return base


def variant(**over):
    base = {"id": 111, "title": "Black / M", "sku": "", "barcode": None,
            "price": 6900, "available": True, "options": ["Black", "M"],
            "metafields": {"custom": {}, "mm-google-shopping": {}}}
    base.update(over)
    return base


CASES = []


def case(name):
    def deco(fn):
        CASES.append((name, fn))
        return fn
    return deco


# --------------------------------------------------------------------------
# T2 — size guide
# --------------------------------------------------------------------------
@case("size guide renders the table when real measurements exist")
def _(env):
    out = env.get_template("hivolt-size-guide").render(
        product=product(metafields={"spec": {"size_chart": mf(CHART_CM)}}),
        part="dialog")
    assert "<dialog" in out and 'id="HvSizeGuide-999"' in out, out[:400]
    assert "<th scope=\"row\">S</th>" in out
    return out


@case("size guide converts cm to inches without changing what is stored")
def _(env):
    out = env.get_template("hivolt-size-guide").render(
        product=product(metafields={"spec": {"size_chart": mf(CHART_CM)}}),
        part="dialog")
    # 51 cm / 2.54 = 20.07... -> 20.1
    assert "<span data-unit-cm>51</span><span data-unit-in>20.1</span>" in out, \
        "chest row did not convert as expected"
    assert 'data-active-unit="cm"' in out


@case("size guide omits a cell that was never measured")
def _(env):
    out = env.get_template("hivolt-size-guide").render(
        product=product(metafields={"spec": {"size_chart": mf(CHART_CM)}}),
        part="dialog")
    assert out.count("hv-sg__absent") == 1, "size M is missing Length; expected one dash"
    assert ">L<" not in out, "size L has no measurements at all and must be dropped"


@case("size guide renders NOTHING when no chart is attached")
def _(env):
    p = product()
    for part in ("trigger", "dialog"):
        out = env.get_template("hivolt-size-guide").render(product=p, part=part)
        assert out.strip() == "", f"{part} emitted {out!r} with no chart"


@case("size guide renders NOTHING when the chart has no real values")
def _(env):
    empty = dict(CHART_CM)
    empty["rows"] = mf([{"size": "S", "values": {}}])
    p = product(metafields={"spec": {"size_chart": mf(empty)}})
    for part in ("trigger", "dialog"):
        out = env.get_template("hivolt-size-guide").render(product=p, part=part)
        assert out.strip() == "", f"{part} emitted {out!r} for an empty chart"


# --------------------------------------------------------------------------
# T3 — swatches
# --------------------------------------------------------------------------
def render_swatches(env, values):
    return env.get_template("hivolt-swatches").render(
        product=product(), option={"name": "Color", "values": values},
        option_index=1, section_id="main", form_id="f", block={"settings": {}})


@case("swatch with real colour data renders a chip")
def _(env):
    out = render_swatches(env, [
        OptionValue("Black", swatch={"color": "#111111"}, selected=True),
        OptionValue("Bone", swatch={"color": "#e8e4dc"})])
    assert "background-color: #111111;" in out
    assert "hv-swatches--text" not in out
    assert out.count("hv-swatch__chip") == 2


@case("swatch with NO colour data falls back to text, never a guessed colour")
def _(env):
    out = render_swatches(env, [OptionValue("Deep Sea"), OptionValue("Bone")])
    assert "hv-swatches--text" in out
    assert "background-color" not in out, "a colour was invented from the name"
    assert "hv-swatch__text" in out and "Deep Sea" in out


@case("sold-out swatch is marked in class and in the accessible name")
def _(env):
    out = render_swatches(env, [
        OptionValue("Black", swatch={"color": "#111111"}),
        OptionValue("Bone", available=False, swatch={"color": "#e8e4dc"})])
    assert out.count("hv-swatch__label--out") == 1
    assert "Sold out" in out, "sold-out state is not in the accessible name"


@case("swatch keeps the theme's variant JS hooks intact")
def _(env):
    out = render_swatches(env, [OptionValue("Black", swatch={"color": "#111"})])
    for hook in ('data-variant-input', 'data-index="option1"', 'name="Color"',
                 'class="variant-input-wrap', 'value="Black"'):
        assert hook in out, f"missing theme hook: {hook}"


# --------------------------------------------------------------------------
# G7 — identifier resolution
# --------------------------------------------------------------------------
def mode(env, p, v):
    return env.get_template("hivolt-identifier").render(
        product=p, variant=v, format="mode").strip()


@case("identifier: a real 13-digit barcode resolves to gtin")
def _(env):
    assert mode(env, product(), variant(barcode="4006381333931")) == "gtin"


@case("identifier: a non-numeric barcode is not a GTIN")
def _(env):
    assert mode(env, product(), variant(barcode="HV-POLO-BLK-M")) == "none"


@case("identifier: a 7-digit barcode is not a valid GTIN length")
def _(env):
    assert mode(env, product(), variant(barcode="1234567")) == "none"


@case("identifier: brand + MPN resolves to brand_mpn when there is no barcode")
def _(env):
    p = product(metafields={"spec": {}, "custom": {"mpn": mf("PQ-220-BLK")}})
    assert mode(env, p, variant()) == "brand_mpn"


@case("identifier: nothing real means none, so the feed sends identifier_exists=no")
def _(env):
    p = product()
    assert mode(env, p, variant()) == "none"
    feed = env.get_template("hivolt-identifier").render(
        product=p, variant=variant(), format="feed")
    assert "identifier_exists=no" in feed
    assert "gtin=" not in feed and "mpn=" not in feed


@case("identifier: declaring gtin without a barcode falls through, it does not fake one")
def _(env):
    p = product(metafields={"spec": {}, "custom": {"identifier_mode": mf("gtin")}})
    v = variant()
    assert mode(env, p, v) == "none"
    assert "111" not in env.get_template("hivolt-identifier").render(
        product=p, variant=v, format="feed"), "variant id leaked as an identifier"


@case("identifier: a variant override beats the product default")
def _(env):
    p = product(metafields={"spec": {}, "custom": {"identifier_mode": mf("auto"),
                                                   "mpn": mf("PQ-220")}})
    v = variant(metafields={"custom": {"identifier_mode": mf("none")},
                            "mm-google-shopping": {}})
    assert mode(env, p, v) == "none"


# --------------------------------------------------------------------------
# G6 — feed title
# --------------------------------------------------------------------------
@case("feed title falls back to the storefront title when unset")
def _(env):
    tpl = env.get_template("hivolt-feed-title")
    p = product()
    assert tpl.render(product=p, format="plain").strip() == "HIVOLT Pique Polo"
    assert tpl.render(product=p, format="source").strip() == "fallback"


@case("feed title uses the metafield and appends variant options")
def _(env):
    p = product(metafields={"spec": {},
                            "custom": {"feed_title": mf("HIVOLT Pique Polo Shirt - Men's")}})
    out = env.get_template("hivolt-feed-title").render(
        product=p, variant=variant(), format="plain").strip()
    assert out == "HIVOLT Pique Polo Shirt - Men's - Black - M", out


# --------------------------------------------------------------------------
# T1 — spec table
# --------------------------------------------------------------------------
@case("spec table renders NOTHING when no spec is filled in")
def _(env):
    out = env.get_template("hivolt-spec-table").render(product=product())
    assert out.strip() == "", out[:200]


@case("spec table renders only the rows that have values")
def _(env):
    p = product(metafields={"spec": {"composition": mf("100% cotton"),
                                     "gsm": mf(220)}})
    out = env.get_template("hivolt-spec-table").render(product=p)
    assert "Composition" in out and "100% cotton" in out
    assert "220 g/m" in out
    for absent in ("Collar", "Placket", "Hem", "Made in"):
        assert absent not in out, f"{absent} rendered with no value"


# --------------------------------------------------------------------------
# G8 — structured data
# --------------------------------------------------------------------------
def render_ld(env, **ctx):
    base = {"request": {"page_type": "product"}, "shop": {"url": "https://hivolt-usa.com",
            "name": "HIVOLT", "currency": "USD"},
            "cart": {"currency": {"iso_code": "USD"}},
            "settings": {"favicon": None, "social_facebook_link": "https://facebook.com/hivolt",
                         "social_instagram_link": "", "social_youtube_link": "",
                         "social_tiktok_link": "", "social_pinterest_link": ""},
            "template": {"suffix": ""}, "canonical_url": "https://hivolt-usa.com/products/x",
            "collection": {}, "page": {}, "blog": {}, "article": {}}
    base.update(ctx)
    out = env.get_template("hivolt-structured-data").render(**base)
    body = out.split(">", 1)[1].rsplit("</script>", 1)[0]
    return out, json.loads(body)


@case("structured data is valid JSON on a product page")
def _(env):
    v = variant(sku="HV-PQ-BLK-M")
    p = product(variants=[v], selected_or_first_available_variant=v)
    _, data = render_ld(env, product=p)
    types = [n["@type"] for n in data["@graph"]]
    assert types == ["Organization", "WebSite", "BreadcrumbList", "Product"], types


@case("structured data never emits a rating or a review")
def _(env):
    v = variant()
    p = product(variants=[v], selected_or_first_available_variant=v)
    raw, _ = render_ld(env, product=p)
    for banned in ("aggregateRating", "AggregateRating", "\"review\"", "Review"):
        assert banned not in raw, f"{banned} appeared in structured data"


@case("structured data omits gtin and mpn when there is no real identifier")
def _(env):
    v = variant()
    p = product(variants=[v], selected_or_first_available_variant=v)
    raw, data = render_ld(env, product=p)
    assert "gtin" not in raw and "mpn" not in raw
    offer = data["@graph"][3]["offers"][0]
    assert offer["price"] == 69.0 and offer["priceCurrency"] == "USD"


@case("structured data emits gtin only for a real barcode")
def _(env):
    v = variant(barcode="4006381333931")
    p = product(variants=[v], selected_or_first_available_variant=v)
    _, data = render_ld(env, product=p)
    offer = data["@graph"][3]["offers"][0]
    assert offer["gtin"] == "4006381333931" and offer["gtin13"] == "4006381333931"


@case("offer availability follows the variant, not a default")
def _(env):
    v1 = variant(id=1, available=True)
    v2 = variant(id=2, available=False, title="Black / L")
    p = product(variants=[v1, v2], selected_or_first_available_variant=v1)
    _, data = render_ld(env, product=p)
    got = [o["availability"] for o in data["@graph"][3]["offers"]]
    assert got == ["https://schema.org/InStock", "https://schema.org/OutOfStock"], got


@case("no Product node on a GemPages template, to avoid two answers on one page")
def _(env):
    v = variant()
    p = product(variants=[v], selected_or_first_available_variant=v)
    _, data = render_ld(env, product=p, template={"suffix": "gp-template-1-2"})
    assert [n["@type"] for n in data["@graph"]][-1] != "Product"


@case("home page still carries Organization and WebSite, and no breadcrumb")
def _(env):
    _, data = render_ld(env, request={"page_type": "index"}, product={})
    assert [n["@type"] for n in data["@graph"]] == ["Organization", "WebSite"]


def main():
    env = make_env()
    failed = 0
    for name, fn in CASES:
        try:
            fn(env)
            print(f"  ok  {name}")
        except AssertionError as e:
            failed += 1
            print(f"FAIL  {name}\n      {e}")
        except Exception as e:                              # noqa: BLE001
            failed += 1
            print(f"ERR   {name}\n      {type(e).__name__}: {e}")
    print(f"\n{len(CASES) - failed}/{len(CASES)} checks pass")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
