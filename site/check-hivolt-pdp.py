#!/usr/bin/env python3
"""HIVOLT PDP release gate.

Runs the real snippet files through a real Liquid engine against the QA
fixtures in site/hivolt_pdp_fixtures.py and asserts what they emit.

Three kinds of check live here and all three are release requirements:

  positive    the component renders the data it was given, correctly
  degradation missing data removes UI instead of producing a blank or a guess
  negative    the output never contains a claim nobody has verified - no
              rating, no review, no invented identifier, no unbacked shipping
              or returns property

The negative checks matter most. A structured-data document that gains an
aggregateRating is a Google manual-action risk and a lie to the shopper, so
those assertions are written to fail on the substring, not on a parsed
property, and cannot be satisfied by a value that merely looks empty.

Run:  python3 site/check-hivolt-pdp.py
Exit: 0 when every check passes, 1 otherwise.
"""
import json
import pathlib
import re
import sys
from html.parser import HTMLParser

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import hivolt_pdp_fixtures as fx          # noqa: E402
import hivolt_pdp_render as R             # noqa: E402
from hivolt_pdp_fixtures import OptionValue, mf, product, variant   # noqa: E402

CASES = []


def case(group, name):
    def deco(fn):
        CASES.append((group, name, fn))
        return fn
    return deco


# ---------------------------------------------------------------------------
# Small HTML utilities. These exist so structural defects fail as assertions
# rather than as something a human has to spot in a screenshot.
# ---------------------------------------------------------------------------
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link",
        "meta", "param", "source", "track", "wbr"}
INTERACTIVE = {"a", "button", "input", "select", "textarea", "details"}


class _Scan(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.errors = []
        self.ids = []
        self.nested_interactive = []
        self.tags = []

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        self.tags.append((tag, d))
        if "id" in d:
            self.ids.append(d["id"])
        if tag in INTERACTIVE and any(t in INTERACTIVE for t in self.stack):
            self.nested_interactive.append((self.stack[-1], tag))
        if tag not in VOID:
            self.stack.append(tag)

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if not self.stack:
            self.errors.append(f"</{tag}> with nothing open")
        elif self.stack[-1] != tag:
            self.errors.append(f"</{tag}> closes <{self.stack[-1]}>")
            if tag in self.stack:
                while self.stack and self.stack.pop() != tag:
                    pass
        else:
            self.stack.pop()


def scan(html):
    s = _Scan()
    s.feed(html)
    s.close()
    if s.stack:
        s.errors.append(f"never closed: {s.stack}")
    return s


def attrs_of(html, tag_name):
    return [d for t, d in scan(html).tags if t == tag_name]


# CSS colour keywords a naive implementation might reach for by handleizing an
# option name. None of these may ever appear in a style attribute.
COLOUR_KEYWORDS = ("sea", "slate", "bone", "black", "navy", "volt", "teal",
                   "ivory", "sand", "olive", "plum", "wheat")


# ===========================================================================
# T1 - specification table
# ===========================================================================
SPEC_LABELS = ["Composition", "Fabric weight", "Knit", "Fit", "Collar",
               "Placket", "Sleeve", "Hem", "Finish", "Seams", "Opacity",
               "Care", "Made in"]


@case("T1 specs", "every populated spec row renders, in schema order")
def _(env):
    html = R.spec_table(env, fx.golden_product())
    labels = [d for t, d in [(t, d) for t, d in scan(html).tags] if t == "dt"]
    dts = re.findall(r"<dt>(.*?)</dt>", html, re.S)
    assert [d.strip() for d in dts] == SPEC_LABELS, dts


@case("T1 specs", "spec values render verbatim from the metafield")
def _(env):
    html = R.spec_table(env, fx.golden_product())
    for expected in ("60% combed cotton / 40% recycled polyester", "Pique",
                     "Regular", "Flatlock, 4-thread", "Portugal"):
        assert expected in html, f"missing value: {expected}"


@case("T1 specs", "fabric weight is the only row that gains a unit")
def _(env):
    html = R.spec_table(env, fx.golden_product())
    assert "220 g/m&sup2;" in html
    assert html.count("g/m&sup2;") == 1, "unit leaked onto another row"


@case("T1 specs", "no spec row is ever rendered empty")
def _(env):
    for name, build in fx.SCENARIOS.items():
        html = R.spec_table(env, build())
        assert "<dd></dd>" not in html.replace("\n", "").replace(" ", ""), name
        assert "<dt></dt>" not in html, name


@case("T1 specs", "one missing field removes exactly one row")
def _(env):
    p = fx.golden_product()
    del p["metafields"]["spec"]["collar"]
    html = R.spec_table(env, p)
    dts = [d.strip() for d in re.findall(r"<dt>(.*?)</dt>", html, re.S)]
    assert "Collar" not in dts and len(dts) == len(SPEC_LABELS) - 1, dts


@case("T1 specs", "several missing fields leave the rest intact and in order")
def _(env):
    p = fx.golden_product()
    for k in ("collar", "placket", "hem", "opacity", "origin"):
        del p["metafields"]["spec"][k]
    dts = [d.strip() for d in re.findall(r"<dt>(.*?)</dt>", R.spec_table(env, p), re.S)]
    assert dts == ["Composition", "Fabric weight", "Knit", "Fit", "Sleeve",
                   "Finish", "Seams", "Care"], dts


@case("T1 specs", "scenario B: no spec data removes the whole block")
def _(env):
    html = R.spec_table(env, fx.scenario_b_no_specs())
    assert html.strip() == "", html[:200]


@case("T1 specs", "benefits render as a list, and vanish when absent")
def _(env):
    html = R.spec_table(env, fx.golden_product())
    lis = re.findall(r"<li>(.*?)</li>", html, re.S)
    assert len(lis) == 3 and "220 g/m2 pique" in lis[0], lis
    p = fx.golden_product()
    del p["metafields"]["spec"]["benefits"]
    assert "hv-spec__benefits" not in R.spec_table(env, p)


@case("T1 specs", "model line needs both height and size, or it does not render")
def _(env):
    assert "Model is 186 cm and wears size M." in R.spec_table(env, fx.golden_product())
    for drop in ("model_height_cm", "model_wears_size"):
        p = fx.golden_product()
        del p["metafields"]["spec"][drop]
        assert "hv-spec__model" not in R.spec_table(env, p), f"rendered without {drop}"


@case("T1 specs", "spec values are HTML-escaped")
def _(env):
    p = fx.golden_product()
    p["metafields"]["spec"]["fit"] = mf('Regular <script>alert(1)</script>')
    html = R.spec_table(env, p)
    assert "<script>" not in html and "&lt;script&gt;" in html


# ===========================================================================
# T2 - size guide
# ===========================================================================
@case("T2 size guide", "a real chart produces a trigger")
def _(env):
    html = R.size_guide(env, fx.golden_product(), "trigger")
    btn = attrs_of(html, "button")
    assert btn and btn[0]["data-hv-sg-open"].startswith("HvSizeGuide-"), html[:200]
    assert btn[0]["aria-haspopup"] == "dialog"


@case("T2 size guide", "scenario C: no chart means no trigger and no dialog")
def _(env):
    p = fx.scenario_c_specs_no_chart()
    for part in ("trigger", "dialog"):
        assert R.size_guide(env, p, part).strip() == "", part


@case("T2 size guide", "a chart with no measured cell renders nothing")
def _(env):
    p = fx.golden_product()
    chart = dict(fx.GOLDEN_CHART)
    chart["rows"] = mf([{"size": "S", "values": {}}, {"size": "M", "values": {}}])
    p["metafields"]["spec"]["size_chart"] = mf(chart)
    for part in ("trigger", "dialog"):
        assert R.size_guide(env, p, part).strip() == "", part


@case("T2 size guide", "trigger and dialog agree on the same id")
def _(env):
    p = fx.golden_product()
    target = attrs_of(R.size_guide(env, p, "trigger"), "button")[0]["data-hv-sg-open"]
    dlg = attrs_of(R.size_guide(env, p, "dialog"), "dialog")[0]
    assert dlg["id"] == target
    assert dlg["aria-labelledby"] == f"{target}-title"


@case("T2 size guide", "a uid keeps two instances on one page distinct")
def _(env):
    p = fx.golden_product()
    a = attrs_of(R.size_guide(env, p, "dialog", uid="a"), "dialog")[0]["id"]
    b = attrs_of(R.size_guide(env, p, "dialog", uid="b"), "dialog")[0]["id"]
    assert a != b, "uid did not disambiguate"


@case("T2 size guide", "table headers follow the chart's own column order")
def _(env):
    html = R.size_guide(env, fx.golden_product(), "dialog")
    ths = [t.strip() for t in re.findall(r'<th scope="col">(.*?)</th>', html, re.S)]
    assert ths == ["Size", "Chest", "Length", "Sleeve"], ths


@case("T2 size guide", "rows render in the stored unit")
def _(env):
    html = R.size_guide(env, fx.golden_product(), "dialog")
    assert "<span data-unit-cm>51</span>" in html
    assert 'data-active-unit="cm"' in html


@case("T2 size guide", "51 cm converts to 20.1 in")
def _(env):
    html = R.size_guide(env, fx.golden_product(), "dialog")
    assert "<span data-unit-cm>51</span><span data-unit-in>20.1</span>" in html


@case("T2 size guide", "a decimal centimetre survives and converts")
def _(env):
    html = R.size_guide(env, fx.golden_product(), "dialog")
    # 57.5 cm / 2.54 = 22.637... -> 22.6
    assert "<span data-unit-cm>57.5</span><span data-unit-in>22.6</span>" in html


@case("T2 size guide", "a chart stored in inches is not converted twice")
def _(env):
    p = fx.golden_product()
    chart = dict(fx.GOLDEN_CHART)
    chart["source_unit"] = mf("in")
    chart["rows"] = mf([{"size": "M", "values": {"chest": 20}}])
    chart["columns"] = mf([{"key": "chest", "label": "Chest"}])
    p["metafields"]["spec"]["size_chart"] = mf(chart)
    html = R.size_guide(env, p, "dialog")
    assert 'data-active-unit="in"' in html
    assert "<span data-unit-in>20</span>" in html
    assert "<span data-unit-cm>50.8</span>" in html


@case("T2 size guide", "an unmeasured cell is a dash plus real hidden text")
def _(env):
    html = R.size_guide(env, fx.golden_product(), "dialog")
    assert html.count("hv-sg__absent") == 1, "expected exactly one unmeasured cell"
    assert 'aria-hidden="true"' in html and "Not measured" in html


@case("T2 size guide", "a size with no measurements at all is dropped")
def _(env):
    html = R.size_guide(env, fx.golden_product(), "dialog")
    assert ">3XL<" not in html, "an entirely unmeasured size was rendered"
    rows = re.findall(r'<th scope="row">(.*?)</th>', html, re.S)
    assert [r.strip() for r in rows] == ["S", "M", "L", "XL", "2XL"], rows


@case("T2 size guide", "measurement basis changes the copy")
def _(env):
    p = fx.golden_product()
    flat = R.size_guide(env, p, "dialog")
    assert "Garment measured flat" in flat and "not body measurements" in flat
    chart = dict(fx.GOLDEN_CHART)
    chart["measurement_basis"] = mf("body")
    p["metafields"]["spec"]["size_chart"] = mf(chart)
    body = R.size_guide(env, p, "dialog")
    assert "Body measurements" in body and "Garment measured flat" not in body


@case("T2 size guide", "the retracted 'doubled where the column says so' copy stays gone")
def _(env):
    src = (R.SNIPPETS / "hivolt-size-guide.liquid").read_text()
    assert "doubled where" not in src, "an unbacked measurement claim came back"


@case("T2 size guide", "unit toggle offers both units and is a labelled radiogroup")
def _(env):
    html = R.size_guide(env, fx.golden_product(), "dialog")
    grp = [d for d in attrs_of(html, "div") if d.get("role") == "radiogroup"]
    assert grp and grp[0]["aria-label"] == "Measurement unit"
    vals = [i["value"] for i in attrs_of(html, "input")]
    assert vals == ["cm", "in"], vals
    assert sum(1 for i in attrs_of(html, "input") if "checked" in i) == 1


@case("T2 size guide", "the table is scrollable and reachable by keyboard")
def _(env):
    html = R.size_guide(env, fx.golden_product(), "dialog")
    reg = [d for d in attrs_of(html, "div") if d.get("role") == "region"]
    assert reg and reg[0]["tabindex"] == "0" and reg[0].get("aria-label")


@case("T2 size guide", "chart note and model line render inside the dialog")
def _(env):
    html = R.size_guide(env, fx.golden_product(), "dialog")
    assert "Measured flat across the chest" in html
    assert "and wears size M" in html


# ===========================================================================
# T3 - swatches
# ===========================================================================
def _colour_option(p):
    return p["options_with_values"][0]


@case("T3 swatches", "a real swatch colour becomes a chip with that exact colour")
def _(env):
    html = R.swatches(env, fx.golden_product(), _colour_option(fx.golden_product()))
    assert "background-color: #0f0f0f;" in html
    assert "background-color: #e8e4dc;" in html


@case("T3 swatches", "a swatch image becomes a background image")
def _(env):
    html = R.swatches(env, fx.golden_product(), _colour_option(fx.golden_product()))
    assert "background-image: url(/qa-fixture/volt-swatch.png)" in html


@case("T3 swatches", "a value with no swatch data becomes a text button")
def _(env):
    html = R.swatches(env, fx.golden_product(), _colour_option(fx.golden_product()))
    assert "hv-swatch__text" in html and "Deep Sea" in html


@case("T3 swatches", "no CSS colour is ever inferred from a value's name")
def _(env):
    p = fx.golden_product()
    html = R.swatches(env, p, _colour_option(p))
    styles = " ".join(d.get("style", "") for _, d in scan(html).tags).lower()
    for kw in COLOUR_KEYWORDS:
        assert f"background-color: {kw}" not in styles, f"guessed colour: {kw}"
    # Only the two declared hex values and one image may appear.
    assert styles.count("background-color:") == 2, styles


@case("T3 swatches", "scenario D: with no swatch data anywhere the group is text")
def _(env):
    p = fx.scenario_d_no_swatches()
    html = R.swatches(env, p, _colour_option(p))
    assert "hv-swatches--text" in html
    assert "background-color" not in html and "background-image" not in html
    assert html.count("hv-swatch__text") == 5


@case("T3 swatches", "chips and text buttons coexist in a mixed group")
def _(env):
    p = fx.golden_product()
    html = R.swatches(env, p, _colour_option(p))
    assert "hv-swatches--text" not in html, "mixed group wrongly marked all-text"
    assert html.count("hv-swatch__chip") == 3
    assert html.count("hv-swatch__text") == 2


@case("T3 swatches", "sold-out marks exactly the unavailable value")
def _(env):
    p = fx.golden_product()
    html = R.swatches(env, p, _colour_option(p))
    assert html.count("hv-swatch__label--out") == 1
    outs = [d for _, d in scan(html).tags if d.get("data-available") == "false"]
    assert len(outs) == 1 and outs[0]["data-value"] == "Slate", outs


@case("T3 swatches", "sold-out state is in the accessible name, not only the colour")
def _(env):
    p = fx.golden_product()
    html = R.swatches(env, p, _colour_option(p))
    labels = re.findall(r"<label[^>]*>(.*?)</label>", html, re.S)
    slate = [l for l in labels if "Slate" in l]
    assert slate and "Sold out" in slate[0], slate


@case("T3 swatches", "available values carry no sold-out wording")
def _(env):
    p = fx.golden_product()
    html = R.swatches(env, p, _colour_option(p))
    assert html.count("Sold out") == 1


@case("T3 swatches", "exactly one input is checked")
def _(env):
    p = fx.golden_product()
    html = R.swatches(env, p, _colour_option(p))
    assert sum(1 for d in attrs_of(html, "input") if "checked" in d) == 1


@case("T3 swatches", "the theme's variant JS hooks survive")
def _(env):
    p = fx.golden_product()
    html = R.swatches(env, p, _colour_option(p))
    fs = attrs_of(html, "fieldset")[0]
    assert fs["name"] == "Color" and fs["data-index"] == "option1"
    assert "variant-input-wrap" in fs["class"]
    for inp in attrs_of(html, "input"):
        assert inp["data-variant-input"] is None or inp["data-variant-input"] == ""
        assert inp["data-index"] == "option1"
        assert inp["name"] == "Color"
        assert inp["form"] == "f"
        assert inp["value"]


@case("T3 swatches", "every label points at an input that exists, and ids are unique")
def _(env):
    p = fx.golden_product()
    html = R.swatches(env, p, _colour_option(p))
    ids = [d["id"] for d in attrs_of(html, "input")]
    fors = [d["for"] for d in attrs_of(html, "label")]
    assert len(ids) == len(set(ids)), ids
    assert set(fors) == set(ids), (fors, ids)


@case("T3 swatches", "a value containing spaces produces a usable id")
def _(env):
    p = fx.golden_product()
    html = R.swatches(env, p, _colour_option(p))
    ids = [d["id"] for d in attrs_of(html, "input")]
    assert any("Deep%20Sea" in i or "Deep+Sea" in i or "Deep-Sea" in i for i in ids), ids
    assert all(" " not in i for i in ids), ids


@case("T3 swatches", "the size axis renders as text buttons with its own hooks")
def _(env):
    p = fx.golden_product()
    html = R.swatches(env, p, p["options_with_values"][1], option_index=2)
    fs = attrs_of(html, "fieldset")[0]
    assert fs["name"] == "Size" and fs["data-index"] == "option2"
    assert "hv-swatches--text" in fs["class"]
    assert html.count("hv-swatch__label--out") == 1        # 2XL


@case("T3 swatches", "option values are HTML-escaped in value and data attributes")
def _(env):
    p = fx.golden_product()
    opt = {"name": "Color",
           "values": [OptionValue('Bl"ack<script>', swatch={"color": "#000000"})],
           "selected_value": "x"}
    html = R.swatches(env, p, opt)
    assert "<script>" not in html


# ===========================================================================
# G6 - feed title
# ===========================================================================
@case("G6 feed title", "a populated feed title is used")
def _(env):
    p = fx.golden_product()
    assert R.feed_title(env, p) == f"{fx.QA_MARKER} Pique Polo Shirt - Men's Short Sleeve"
    assert R.feed_title(env, p, fmt="source") == "metafield"


@case("G6 feed title", "scenario H: a blank feed title falls back to the storefront title")
def _(env):
    p = fx.scenario_h_blank_feed_title()
    assert R.feed_title(env, p) == p["title"]
    assert R.feed_title(env, p, fmt="source") == "fallback"


@case("G6 feed title", "an absent metafield falls back too")
def _(env):
    p = fx.scenario_i_single_variant()
    assert R.feed_title(env, p) == p["title"]
    assert R.feed_title(env, p, fmt="source") == "fallback"


@case("G6 feed title", "variant options are appended for an item-level row")
def _(env):
    p = fx.golden_product()
    v = p["variants"][0]
    assert R.feed_title(env, p, variant=v).endswith(" - Black - S"), R.feed_title(env, p, variant=v)


@case("G6 feed title", "a single-variant product does not append 'Default Title'")
def _(env):
    p = fx.scenario_i_single_variant()
    assert R.feed_title(env, p, variant=p["variants"][0]) == p["title"]


@case("G6 feed title", "the feed title is truncated to Merchant Center's 150 characters")
def _(env):
    p = fx.golden_product()
    p["metafields"]["custom"]["feed_title"] = mf("W" * 200)
    assert len(R.feed_title(env, p)) == 150


@case("G6 feed title", "structured data uses the storefront title, never the feed title")
def _(env):
    p = fx.golden_product()
    _, data = R.structured_data(env, product=p)
    node = R.graph_node(data, "Product")
    assert node["name"] == p["title"]
    assert "Men's Short Sleeve" not in node["name"], "feed title leaked into markup"


# ===========================================================================
# G7 - identifiers
# ===========================================================================
def mode(env, p, v):
    return R.identifier(env, p, v, "mode").strip()


def feed(env, p, v):
    return R.identifier(env, p, v, "feed")


@case("G7 identifiers", "a 13-digit barcode resolves to gtin")
def _(env):
    assert mode(env, product(), variant(barcode=fx.FIXTURE_GTIN13)) == "gtin"


@case("G7 identifiers", "a 12-digit barcode resolves to gtin")
def _(env):
    assert mode(env, product(), variant(barcode=fx.FIXTURE_GTIN12)) == "gtin"


@case("G7 identifiers", "an 8-digit and a 14-digit barcode also resolve to gtin")
def _(env):
    assert mode(env, product(), variant(barcode="12345670")) == "gtin"
    assert mode(env, product(), variant(barcode="12345678901231")) == "gtin"


@case("G7 identifiers", "a non-numeric barcode is not a GTIN")
def _(env):
    assert mode(env, product(), variant(barcode="QA-PQ-BLK-M")) == "none"


@case("G7 identifiers", "a barcode of the wrong length is not a GTIN")
def _(env):
    for bad in ("1234567", "123456789", "123456789012345"):
        assert mode(env, product(), variant(barcode=bad)) == "none", bad


@case("G7 identifiers", "a barcode with embedded punctuation is not a GTIN")
def _(env):
    assert mode(env, product(), variant(barcode="4006381-33393")) == "none"


@case("G7 identifiers", "brand plus a product-level MPN resolves to brand_mpn")
def _(env):
    p = product(metafields={"spec": {}, "custom": {"mpn": mf("QA-MPN-001")}})
    assert mode(env, p, variant()) == "brand_mpn"


@case("G7 identifiers", "a variant MPN overrides the product default")
def _(env):
    p = product(metafields={"spec": {}, "custom": {"mpn": mf("PRODUCT-LEVEL")}})
    v = variant(metafields={"custom": {}, "mm-google-shopping": {"mpn": mf("VARIANT-LEVEL")}})
    out = feed(env, p, v)
    assert "mpn=VARIANT-LEVEL" in out and "PRODUCT-LEVEL" not in out, out


@case("G7 identifiers", "scenario F: declared gtin with no barcode falls through to none")
def _(env):
    p = fx.scenario_f_declared_gtin_no_barcode()
    for v in p["variants"]:
        assert mode(env, p, v) == "none", v["title"]


@case("G7 identifiers", "declared brand_mpn with no MPN falls through to none")
def _(env):
    p = product(metafields={"spec": {}, "custom": {"identifier_mode": mf("brand_mpn")}})
    assert mode(env, p, variant()) == "none"


@case("G7 identifiers", "declaring none suppresses a real barcode")
def _(env):
    p = product(metafields={"spec": {}, "custom": {"identifier_mode": mf("none")}})
    assert mode(env, p, variant(barcode=fx.FIXTURE_GTIN13)) == "none"


@case("G7 identifiers", "a variant override beats the product default in both directions")
def _(env):
    p = product(metafields={"spec": {}, "custom": {"identifier_mode": mf("auto"),
                                                   "mpn": mf("QA-MPN-001")}})
    inherit = variant()
    override = variant(metafields={"custom": {"identifier_mode": mf("none")},
                                   "mm-google-shopping": {}})
    assert mode(env, p, inherit) == "brand_mpn"
    assert mode(env, p, override) == "none"


@case("G7 identifiers", "scenario G: nothing verified means identifier_exists=no")
def _(env):
    p = fx.scenario_g_no_identifier()
    for v in p["variants"]:
        out = feed(env, p, v)
        assert "identifier_exists=no" in out, v["title"]
        assert "gtin=" not in out and "mpn=" not in out, out


@case("G7 identifiers", "a resolved gtin is reported to the feed with identifier_exists=yes")
def _(env):
    out = feed(env, product(), variant(barcode=fx.FIXTURE_GTIN13))
    assert f"gtin={fx.FIXTURE_GTIN13}" in out and "identifier_exists=yes" in out


@case("G7 identifiers", "brand and mpn are both sent in brand_mpn mode")
def _(env):
    p = product(metafields={"spec": {}, "custom": {"mpn": mf("QA-MPN-001")}})
    out = feed(env, p, variant())
    assert "brand=HIVOLT" in out and "mpn=QA-MPN-001" in out and "identifier_exists=yes" in out


@case("G7 identifiers", "a Shopify variant id is never emitted as an identifier")
def _(env):
    p = fx.golden_product()
    for v in p["variants"]:
        out = feed(env, p, v)
        for line in out.splitlines():
            line = line.strip()
            if line.startswith(("gtin=", "mpn=")):
                assert str(v["id"]) not in line, f"variant id leaked: {line}"


@case("G7 identifiers", "a HIVOLT SKU is never promoted to MPN automatically")
def _(env):
    v = variant(sku="QA-PQ-BLK-M")
    p = product()
    assert mode(env, p, v) == "none"
    assert "QA-PQ-BLK-M" not in feed(env, p, v)


@case("G7 identifiers", "an empty-string MPN is not an identifier")
def _(env):
    p = product(metafields={"spec": {}, "custom": {"mpn": mf("   ")}})
    assert mode(env, p, variant()) == "none"


@case("G7 identifiers", "a blank vendor blocks brand_mpn even with a real MPN")
def _(env):
    p = product(vendor="", metafields={"spec": {}, "custom": {"mpn": mf("QA-MPN-001")}})
    assert mode(env, p, variant()) == "none"


# ===========================================================================
# G8 - structured data
# ===========================================================================
FORBIDDEN = ("aggregateRating", "AggregateRating", "ratingValue", "reviewCount",
             '"review"', '"Review"', "priceValidUntil", "shippingDetails",
             "hasMerchantReturnPolicy", "OfferShippingDetails",
             "MerchantReturnPolicy")


@case("G8 structured data", "the golden product emits valid JSON")
def _(env):
    _, data = R.structured_data(env, product=fx.golden_product())
    assert data["@context"] == "https://schema.org"
    assert [n["@type"] for n in data["@graph"]] == \
        ["Organization", "WebSite", "BreadcrumbList", "Product"]


@case("G8 structured data", "Organization carries name and url")
def _(env):
    _, data = R.structured_data(env, product=fx.golden_product())
    org = R.graph_node(data, "Organization")
    assert org["name"] == "HIVOLT" and org["url"] == R.SHOP_URL
    assert org["@id"].endswith("#organization")


@case("G8 structured data", "Organization sameAs carries only non-blank socials")
def _(env):
    _, data = R.structured_data(env, product=fx.golden_product())
    assert R.graph_node(data, "Organization")["sameAs"] == ["https://facebook.com/hivolt"]


@case("G8 structured data", "Organization omits logo unless the favicon is big enough")
def _(env):
    _, no_logo = R.structured_data(env, product=fx.golden_product())
    assert "logo" not in R.graph_node(no_logo, "Organization")
    _, with_logo = R.structured_data(
        env, product=fx.golden_product(),
        settings={**R.ld_context()["settings"],
                  "favicon": {"width": 512, "src": "/qa-fixture/logo.png"}})
    assert R.graph_node(with_logo, "Organization")["logo"].startswith("https:")


@case("G8 structured data", "WebSite publishes through the Organization node")
def _(env):
    _, data = R.structured_data(env, product=fx.golden_product())
    site, org = R.graph_node(data, "WebSite"), R.graph_node(data, "Organization")
    assert site["publisher"]["@id"] == org["@id"]


@case("G8 structured data", "BreadcrumbList positions run 1..n without gaps")
def _(env):
    _, data = R.structured_data(env, product=fx.golden_product())
    items = R.graph_node(data, "BreadcrumbList")["itemListElement"]
    assert [i["position"] for i in items] == list(range(1, len(items) + 1))
    assert items[0]["name"] == "Home" and items[-1]["name"] == fx.golden_product()["title"]


@case("G8 structured data", "a collection in context adds a breadcrumb step")
def _(env):
    _, data = R.structured_data(
        env, product=fx.golden_product(),
        collection={"handle": "polos", "title": "Polos", "url": "/collections/polos"})
    items = R.graph_node(data, "BreadcrumbList")["itemListElement"]
    assert [i["name"] for i in items] == ["Home", "Polos", fx.golden_product()["title"]]
    assert items[1]["item"] == f"{R.SHOP_URL}/collections/polos"


@case("G8 structured data", "Product name matches the storefront title exactly")
def _(env):
    p = fx.golden_product()
    _, data = R.structured_data(env, product=p)
    assert R.graph_node(data, "Product")["name"] == p["title"]


@case("G8 structured data", "the offer count equals the variant count")
def _(env):
    p = fx.golden_product()
    _, data = R.structured_data(env, product=p)
    assert len(R.graph_node(data, "Product")["offers"]) == len(p["variants"]) == 25


@case("G8 structured data", "each offer's price comes from its own variant")
def _(env):
    p = fx.golden_product()
    _, data = R.structured_data(env, product=p)
    offers = R.graph_node(data, "Product")["offers"]
    by_id = {o["@id"].rsplit("=", 1)[1]: o for o in offers}
    for v in p["variants"]:
        assert by_id[str(v["id"])]["price"] == v["price"] / 100.0, v["title"]
    assert sorted({o["price"] for o in offers}) == [69.0, 74.0]


@case("G8 structured data", "every offer carries the presentment currency")
def _(env):
    _, data = R.structured_data(env, product=fx.golden_product())
    assert {o["priceCurrency"] for o in R.graph_node(data, "Product")["offers"]} == {"USD"}


@case("G8 structured data", "availability tracks each variant independently")
def _(env):
    p = fx.golden_product()
    _, data = R.structured_data(env, product=p)
    offers = R.graph_node(data, "Product")["offers"]
    by_id = {o["@id"].rsplit("=", 1)[1]: o for o in offers}
    for v in p["variants"]:
        want = "InStock" if v["available"] else "OutOfStock"
        assert by_id[str(v["id"])]["availability"].endswith(want), v["title"]
    kinds = [o["availability"] for o in offers]
    assert any("InStock" in k for k in kinds) and any("OutOfStock" in k for k in kinds)


@case("G8 structured data", "offer urls carry one variant param and no double query")
def _(env):
    p = fx.golden_product()
    _, data = R.structured_data(env, product=p)
    for o in R.graph_node(data, "Product")["offers"]:
        assert o["url"].count("?") == 1, o["url"]
        assert o["url"].startswith(f"{R.SHOP_URL}{p['url']}?variant="), o["url"]


@case("G8 structured data", "the product url is query-free even when reached with tracking")
def _(env):
    p = fx.golden_product()
    p["url"] = "/products/qa-fixture-pique-polo?_pos=3&_sid=abc&_ss=r"
    _, data = R.structured_data(env, product=p)
    assert R.graph_node(data, "Product")["url"] == \
        f"{R.SHOP_URL}/products/qa-fixture-pique-polo"


@case("G8 structured data", "gtin appears only on the offers that really have one")
def _(env):
    p = fx.golden_product()
    _, data = R.structured_data(env, product=p)
    offers = R.graph_node(data, "Product")["offers"]
    by_id = {o["@id"].rsplit("=", 1)[1]: o for o in offers}
    for v in p["variants"]:
        o = by_id[str(v["id"])]
        if v["barcode"]:
            assert o["gtin"] == v["barcode"], v["title"]
            assert o[f"gtin{len(v['barcode'])}"] == v["barcode"]
        else:
            assert "gtin" not in o, f"{v['title']} invented a gtin"
    assert sum(1 for o in offers if "gtin" in o) == 6      # 5 Black + Bone/L


@case("G8 structured data", "mpn appears only where a real MPN is stored")
def _(env):
    p = fx.golden_product()
    _, data = R.structured_data(env, product=p)
    offers = R.graph_node(data, "Product")["offers"]
    by_id = {o["@id"].rsplit("=", 1)[1]: o for o in offers}
    # Volt/M declares `none`, so it must carry no identifier at all.
    volt_m = next(v for v in p["variants"] if v["title"] == "Volt / M")
    assert "mpn" not in by_id[str(volt_m["id"])]
    assert "gtin" not in by_id[str(volt_m["id"])]
    # Bone (except L, which has a barcode) carries its own variant MPN.
    bone_s = next(v for v in p["variants"] if v["title"] == "Bone / S")
    assert by_id[str(bone_s["id"])]["mpn"] == "QA-MPN-BONE-001"


@case("G8 structured data", "scenario G: no identifier means no gtin and no mpn anywhere")
def _(env):
    raw, data = R.structured_data(env, product=fx.scenario_g_no_identifier())
    assert "gtin" not in raw and "mpn" not in raw
    for o in R.graph_node(data, "Product")["offers"]:
        assert "gtin" not in o and "mpn" not in o


@case("G8 structured data", "NEGATIVE: no rating or review property, in any scenario")
def _(env):
    for name, build in fx.SCENARIOS.items():
        raw, _ = R.structured_data(env, product=build())
        low = raw.lower()
        for banned in ("aggregaterating", "ratingvalue", "reviewcount", '"review"',
                       '"@type": "review"'):
            assert banned not in low, f"{name}: {banned} appeared"


@case("G8 structured data", "NEGATIVE: no unbacked commercial property, in any scenario")
def _(env):
    for name, build in fx.SCENARIOS.items():
        raw, _ = R.structured_data(env, product=build())
        for banned in FORBIDDEN:
            assert banned not in raw, f"{name}: {banned} appeared"


@case("G8 structured data", "NEGATIVE: no Shopify id is ever used as an identifier")
def _(env):
    p = fx.golden_product()
    _, data = R.structured_data(env, product=p)
    ids = {str(v["id"]) for v in p["variants"]} | {str(p["id"])}
    for o in R.graph_node(data, "Product")["offers"]:
        for key in ("gtin", "gtin8", "gtin12", "gtin13", "gtin14", "mpn", "sku"):
            if key in o and key != "sku":
                assert o[key] not in ids, f"{key} is a Shopify id"


@case("G8 structured data", "scenario I: a single-variant product emits one plain offer")
def _(env):
    p = fx.scenario_i_single_variant()
    _, data = R.structured_data(env, product=p)
    offers = R.graph_node(data, "Product")["offers"]
    assert len(offers) == 1
    assert "name" not in offers[0], "Default Title leaked into the offer name"
    assert offers[0]["price"] == 49.0


@case("G8 structured data", "scenario J: a bare product still emits valid, honest JSON")
def _(env):
    p = fx.scenario_j_bare_minimum()
    raw, data = R.structured_data(env, product=p)
    node = R.graph_node(data, "Product")
    assert node["name"] == p["title"]
    for absent in ("description", "image", "brand", "sku"):
        assert absent not in node, f"{absent} emitted with nothing behind it"
    assert node["offers"][0]["availability"].endswith("OutOfStock")


@case("G8 structured data", "a GemPages template yields no second Product node")
def _(env):
    _, data = R.structured_data(env, product=fx.golden_product(),
                                template={"suffix": "gp-template-1-2"})
    assert R.graph_node(data, "Product") is None
    assert [n["@type"] for n in data["@graph"]] == \
        ["Organization", "WebSite", "BreadcrumbList"]


@case("G8 structured data", "the home page carries Organization and WebSite only")
def _(env):
    _, data = R.structured_data(env, request={"page_type": "index"}, product={})
    assert [n["@type"] for n in data["@graph"]] == ["Organization", "WebSite"]


@case("G8 structured data", "a page template gets a breadcrumb but no Product")
def _(env):
    _, data = R.structured_data(env, request={"page_type": "page"}, product={},
                                page={"title": "Size guide"})
    types = [n["@type"] for n in data["@graph"]]
    assert types == ["Organization", "WebSite", "BreadcrumbList"]
    assert R.graph_node(data, "BreadcrumbList")["itemListElement"][-1]["name"] == "Size guide"


@case("G8 structured data", "the description is stripped of markup before it is emitted")
def _(env):
    p = fx.golden_product()
    p["description"] = "<p>A polo <b>with</b> markup.</p>"
    _, data = R.structured_data(env, product=p)
    assert R.graph_node(data, "Product")["description"] == "A polo with markup."


# ===========================================================================
# Degradation - every scenario must render without crashing or lying
# ===========================================================================
@case("Degradation", "every scenario renders every component without raising")
def _(env):
    for name, build in fx.SCENARIOS.items():
        p = build()
        R.spec_table(env, p)
        R.size_guide(env, p, "trigger")
        R.size_guide(env, p, "dialog")
        R.feed_title(env, p)
        for opt_i, opt in enumerate(p.get("options_with_values") or [], start=1):
            R.swatches(env, p, opt, option_index=opt_i)
        R.structured_data(env, product=p)


@case("Degradation", "every scenario produces well-formed HTML")
def _(env):
    for name, build in fx.SCENARIOS.items():
        html = R.preview_html(env, build())
        s = scan(html)
        assert not s.errors, f"{name}: {s.errors}"


@case("Degradation", "every scenario's preview page has no duplicate id")
def _(env):
    for name, build in fx.SCENARIOS.items():
        ids = scan(R.preview_html(env, build())).ids
        dupes = {i for i in ids if ids.count(i) > 1}
        assert not dupes, f"{name}: duplicate ids {dupes}"


@case("Degradation", "no interactive element is nested inside another")
def _(env):
    for name, build in fx.SCENARIOS.items():
        s = scan(R.preview_html(env, build()))
        assert not s.nested_interactive, f"{name}: {s.nested_interactive}"


@case("Degradation", "no scenario emits a placeholder or a TODO")
def _(env):
    for name, build in fx.SCENARIOS.items():
        html = R.preview_html(env, build()).lower()
        for junk in ("lorem", "todo", "fixme", "placeholder", "undefined",
                     "something something", "n/a", "tbd"):
            assert junk not in html, f"{name}: {junk!r} rendered"


@case("Degradation", "no scenario emits a visibly empty control or table cell")
def _(env):
    for name, build in fx.SCENARIOS.items():
        html = R.preview_html(env, build())
        compact = re.sub(r">\s+<", "><", html)
        for empty in ("<td></td>", "<dd></dd>", "<dt></dt>", "<li></li>",
                      "<th></th>", "<button></button>"):
            assert empty not in compact, f"{name}: {empty}"


@case("Degradation", "every scenario's structured data parses as JSON")
def _(env):
    for name, build in fx.SCENARIOS.items():
        raw, data = R.structured_data(env, product=build())
        json.dumps(data)
        assert raw.count("<script") == 1 and "</script>" in raw, name


# ===========================================================================
# Liquid source safety
# ===========================================================================
HIVOLT_SNIPPETS = sorted(R.SNIPPETS.glob("hivolt-*.liquid"))


@case("Liquid safety", "every HIVOLT snippet parses with the Shopify-shaped dialect")
def _(env):
    for path in HIVOLT_SNIPPETS + [R.SNIPPETS / "variant-button.liquid",
                                   R.SNIPPETS / "social-meta-tags.liquid"]:
        env.from_string(path.read_text())


@case("Liquid safety", "no condensed boolean guard reads a property it just null-checked")
def _(env):
    # Shopify Liquid evaluates `and`/`or` right to left, so
    # `x != blank and x.y > 0` runs the property read first. That bug shipped
    # once; this stops it coming back.
    pattern = re.compile(
        r"(?:if|unless|elsif)\s+([\w.\[\]'\"-]+)\s*(?:!=\s*blank|!=\s*''|)\s*"
        r"(?:and|or)\s+\1\.", re.I)
    offenders = []
    for path in HIVOLT_SNIPPETS:
        for i, line in enumerate(path.read_text().splitlines(), 1):
            if pattern.search(line):
                offenders.append(f"{path.name}:{i}: {line.strip()}")
    assert not offenders, "\n".join(offenders)


@case("Liquid safety", "size comparisons go through default, so nil never reaches >")
def _(env):
    src = (R.SNIPPETS / "hivolt-size-guide.liquid").read_text()
    assert "hv_col_count = hv_cols.size | default: 0" in src
    assert "hv_row_count = hv_rows.size | default: 0" in src
    spec = (R.SNIPPETS / "hivolt-spec-table.liquid").read_text()
    assert "hv_benefit_count = hv_benefits.size | default: 0" in spec


@case("Liquid safety", "the JSON-LD script tag is opened and closed exactly once")
def _(env):
    src = (R.SNIPPETS / "hivolt-structured-data.liquid").read_text()
    assert src.count("<script") == 1 and src.count("</script>") == 1


@case("Liquid safety", "no HIVOLT snippet writes a raw metafield into a style attribute")
def _(env):
    for path in HIVOLT_SNIPPETS:
        for line in path.read_text().splitlines():
            if "style=" in line and "metafields" in line:
                raise AssertionError(f"{path.name}: {line.strip()}")


@case("Liquid safety", "the structured-data snippet still guards against GemPages")
def _(env):
    src = (R.SNIPPETS / "hivolt-structured-data.liquid").read_text()
    assert "hv_gempages_template" in src and "gp-template-" in src


# ===========================================================================
# Nil-guard regressions
# ===========================================================================
# Shopify treats an unset metafield as blank; other Liquid engines do not.
# Every guard below was written against `== blank` and silently changed
# behaviour depending on the engine. Each is now resolved through `default`
# first, and each has a test that fails if the old form comes back.
@case("Nil guards", "the product-level identifier mode is actually reachable")
def _(env):
    p = product(metafields={"spec": {}, "custom": {"identifier_mode": mf("none")}})
    assert mode(env, p, variant(barcode=fx.FIXTURE_GTIN13)) == "none", \
        "product default was skipped, so a declared suppression was ignored"


@case("Nil guards", "an absent chart note produces no paragraph")
def _(env):
    p = fx.golden_product()
    chart = {k: v for k, v in fx.GOLDEN_CHART.items() if k != "note"}
    p["metafields"]["spec"]["size_chart"] = mf(chart)
    html = R.size_guide(env, p, "dialog")
    assert "hv-sg__note" not in html, "empty note paragraph rendered"


@case("Nil guards", "a chart note is escaped before its line breaks are added")
def _(env):
    p = fx.golden_product()
    chart = dict(fx.GOLDEN_CHART)
    chart["note"] = mf("Line one\nLine <b>two</b>")
    p["metafields"]["spec"]["size_chart"] = mf(chart)
    html = R.size_guide(env, p, "dialog")
    assert "<b>" not in html and "&lt;b&gt;" in html
    assert "<br" in html, "newline_to_br stopped working"


@case("Nil guards", "the size guide model line needs both height and size")
def _(env):
    assert "and wears size M." in R.size_guide(env, fx.golden_product(), "dialog")
    for drop in ("model_height_cm", "model_wears_size"):
        p = fx.golden_product()
        del p["metafields"]["spec"][drop]
        html = R.size_guide(env, p, "dialog")
        assert "hv-sg__model" not in html, f"half a sentence rendered without {drop}"


@case("Nil guards", "no HIVOLT snippet compares a metafield to blank")
def _(env):
    offenders = []
    for path in HIVOLT_SNIPPETS:
        for i, line in enumerate(path.read_text().splitlines(), 1):
            stripped = line.strip()
            if stripped.startswith(("comment", "{%- comment", "{% comment")):
                continue
            if "metafields" in line and re.search(r"[!=]=\s*blank", line):
                offenders.append(f"{path.name}:{i}: {stripped}")
    assert not offenders, (
        "metafield compared to blank; resolve through `| default: \'\'` instead:\n"
        + "\n".join(offenders))


@case("Nil guards", "swatch option values are escaped in both the chip and text paths")
def _(env):
    p = fx.golden_product()
    for swatch in ({"color": "#000000"}, {}):
        opt = {"name": "Color",
               "values": [OptionValue('<img src=x onerror=1>', swatch=swatch)],
               "selected_value": "x"}
        html = R.swatches(env, p, opt)
        assert "<img" not in html, f"unescaped value with swatch={swatch}"
        assert "&lt;img" in html


# ===========================================================================
# Runner
# ===========================================================================
def main():
    env = R.make_env()
    failed = []
    current = None
    for group, name, fn in CASES:
        if group != current:
            print(f"\n{group}")
            current = group
        try:
            fn(env)
            print(f"  ok    {name}")
        except AssertionError as e:
            failed.append((group, name))
            print(f"  FAIL  {name}\n        {e}")
        except Exception as e:                              # noqa: BLE001
            failed.append((group, name))
            print(f"  ERROR {name}\n        {type(e).__name__}: {e}")

    total = len(CASES)
    passed = total - len(failed)
    print(f"\nHIVOLT PDP RELEASE GATE: {passed}/{total} "
          f"{'PASS' if not failed else 'FAIL'}")
    if failed:
        print("\nFailed:")
        for group, name in failed:
            print(f"  [{group}] {name}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
