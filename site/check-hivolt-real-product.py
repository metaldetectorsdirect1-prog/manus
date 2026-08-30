#!/usr/bin/env python3
"""HIVOLT real-product render gate.

check-hivolt-pdp.py proves the snippets behave against a golden fixture. This
file proves something different and narrower: that the data actually written to
the live catalogue renders the way the provenance record says it should, and
that every field left deliberately blank stays invisible on the page.

The drop below is transcribed from an authoritative read-back of
gid://shopify/Product/9603121774824 taken after the write, not from the
mutation payload and not from memory. Two fields carry a value; fifteen do not.
The point of this gate is that the fifteen produce no row, no placeholder and
no invented text - because the moment one of them renders "Knit" or "-" the
page is making a claim nobody verified.

Run:  python3 site/check-hivolt-real-product.py
Exit: 0 when every check passes, 1 otherwise.
"""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import hivolt_pdp_render as R                      # noqa: E402
from hivolt_pdp_fixtures import OptionValue, mf    # noqa: E402

# ---------------------------------------------------------------------------
# Read-back of 2026-08-22, product 9603121774824, status DRAFT
# ---------------------------------------------------------------------------
PRODUCT_GID = "gid://shopify/Product/9603121774824"

# Present, with the class of evidence behind each. Both are Class B: stated by
# the supplier for this exact item, not yet verified against a garment label.
WRITTEN = {
    "composition": "100% Cotton",
    "fit": "Regular",
}

# Every spec.* field the read-back returned null for. Kept explicit rather than
# derived so that a future field silently appearing in the catalogue fails this
# gate instead of slipping onto the page unnoticed.
BLANK = [
    "gsm", "knit", "collar", "placket", "cuff", "hem", "finish", "seams",
    "opacity", "care", "origin", "benefits", "model_height_cm",
    "model_wears_size", "size_chart",
]

# The label text the spec table would print for each blank key, from
# hivolt-spec-table.liquid. If a blank key ever renders, its label is what
# would appear, so the negative assertion looks for the label.
BLANK_LABELS = {
    "gsm": "Fabric weight", "knit": "Knit", "collar": "Collar",
    "placket": "Placket", "cuff": "Sleeve", "hem": "Hem", "finish": "Finish",
    "seams": "Seams", "opacity": "Opacity", "care": "Care", "origin": "Made in",
}

SIZES = ["EUR S 60-70kg", "EUR M 70-80kg", "EUR XL 90-100kg",
         "EUR XXL 100-105kg", "EUR L 80-90kg"]
COLOURS = ["Navy", "White", "Light Blue", "Dark Grey", "Black", "Army Green"]

# Text that must never reach the page in place of a missing value.
PLACEHOLDERS = ["N/A", "n/a", "TBD", "Unknown", "unknown", "Coming soon",
                "See size chart", "Standard fit", "Pique", "Interlock",
                "Anti-Pilling", "Machine wash"]

CASES = []


def case(group, name):
    def deco(fn):
        CASES.append((group, name, fn))
        return fn
    return deco


def real_product():
    """The drop, built from the read-back. Blank fields are simply absent,
    which is exactly how Liquid sees an unset metafield."""
    return {
        "id": 9603121774824,
        "title": "HIVOLT Classic Cotton Polo — Men's Short Sleeve",
        "handle": "hivolt-classic-cotton-polo-mens-short-sleeve",
        "url": "/products/hivolt-classic-cotton-polo-mens-short-sleeve",
        "vendor": "HIVOLT",
        "description": "",
        "images": [],
        "featured_media": None,
        "variants": [],
        "has_only_default_variant": False,
        "empty?": False,
        "selected_or_first_available_variant": None,
        "options_with_values": [
            {"name": "Color", "values": [OptionValue(c) for c in COLOURS]},
            {"name": "Size", "values": [OptionValue(s) for s in SIZES]},
        ],
        "metafields": {
            "spec": {k: mf(v) for k, v in WRITTEN.items()},
            "custom": {},
        },
    }


def text_of(html):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html)).strip()


# ---------------------------------------------------------------------------
# What the two written values must produce
# ---------------------------------------------------------------------------
@case("Written values", "spec table renders and is not empty")
def t_table_renders(env):
    out = R.spec_table(env, real_product())
    assert "hv-spec__list" in out, "spec table did not render at all"


@case("Written values", "composition row prints 100% Cotton")
def t_composition(env):
    out = R.spec_table(env, real_product())
    assert re.search(r"<dt>Composition</dt>\s*<dd>\s*100% Cotton\s*</dd>", out), \
        f"composition row missing or wrong:\n{out}"


@case("Written values", "fit row prints Regular")
def t_fit(env):
    out = R.spec_table(env, real_product())
    assert re.search(r"<dt>Fit</dt>\s*<dd>\s*Regular\s*</dd>", out), \
        f"fit row missing or wrong:\n{out}"


@case("Written values", "exactly two rows render")
def t_row_count(env):
    out = R.spec_table(env, real_product())
    rows = out.count('class="hv-spec__row"')
    assert rows == 2, f"expected 2 spec rows, got {rows}"


@case("Written values", "rows keep the schema's declared order")
def t_row_order(env):
    out = R.spec_table(env, real_product())
    order = re.findall(r"<dt>([^<]+)</dt>", out)
    assert order == ["Composition", "Fit"], f"row order was {order}"


# ---------------------------------------------------------------------------
# What the fifteen blanks must not produce
# ---------------------------------------------------------------------------
@case("Blank fields", "no label renders for any unwritten spec field")
def t_no_blank_labels(env):
    out = R.spec_table(env, real_product())
    leaked = [k for k, label in BLANK_LABELS.items()
              if f"<dt>{label}</dt>" in out]
    assert not leaked, f"blank fields rendered a row: {leaked}"


@case("Blank fields", "no empty dd is emitted")
def t_no_empty_dd(env):
    out = R.spec_table(env, real_product())
    assert not re.search(r"<dd>\s*</dd>", out), \
        "an empty <dd> reached the page"


@case("Blank fields", "no benefits list when spec.benefits is unset")
def t_no_benefits(env):
    out = R.spec_table(env, real_product())
    assert "hv-spec__benefits" not in out, \
        "benefits list rendered with no benefits written"


@case("Blank fields", "no model sentence when height and size are unset")
def t_no_model(env):
    out = R.spec_table(env, real_product())
    assert "hv-spec__model" not in out and "wears size" not in out, \
        "model sentence rendered with no model data"


@case("Blank fields", "no placeholder text anywhere in the table")
def t_no_placeholder(env):
    out = R.spec_table(env, real_product())
    hit = [p for p in PLACEHOLDERS if p in out]
    assert not hit, f"placeholder text reached the page: {hit}"


@case("Blank fields", "no stray dash or em dash used as a value")
def t_no_dash_value(env):
    out = R.spec_table(env, real_product())
    assert not re.search(r"<dd>\s*[-–—]+\s*</dd>", out), \
        "a dash was used to stand in for a missing value"


# ---------------------------------------------------------------------------
# Size guide: no chart is bound, so nothing may render
# ---------------------------------------------------------------------------
@case("Size guide", "trigger renders nothing without a bound chart")
def t_no_trigger(env):
    out = R.size_guide(env, real_product(), "trigger").strip()
    assert out == "", f"size guide trigger rendered without a chart:\n{out!r}"


@case("Size guide", "dialog renders nothing without a bound chart")
def t_no_dialog(env):
    out = R.size_guide(env, real_product(), "dialog").strip()
    assert out == "", f"size guide dialog rendered without a chart:\n{out!r}"


@case("Size guide", "no body-weight range is presented as a measurement")
def t_no_weight_as_measure(env):
    out = R.spec_table(env, real_product()) + \
        R.size_guide(env, real_product(), "trigger") + \
        R.size_guide(env, real_product(), "dialog")
    assert "kg" not in out, \
        "a body-weight range leaked into the specification or size guide"


# ---------------------------------------------------------------------------
# Swatches still work against the real option values
# ---------------------------------------------------------------------------
@case("Swatches", "every real colour renders a control")
def t_colours(env):
    p = real_product()
    out = R.swatches(env, p, p["options_with_values"][0], option_index=1)
    missing = [c for c in COLOURS if c not in out]
    assert not missing, f"colours missing from the swatch row: {missing}"


@case("Swatches", "every real size renders a control")
def t_sizes(env):
    p = real_product()
    out = R.swatches(env, p, p["options_with_values"][1], option_index=2)
    missing = [s for s in SIZES if s not in out]
    assert not missing, f"sizes missing from the size row: {missing}"


@case("Swatches", "size order on the page matches the catalogue order")
def t_size_order_matches_catalogue(env):
    """The catalogue order is wrong (S, M, XL, XXL, L) and the template must
    not quietly hide that by re-sorting. Sorting here would mask a real data
    defect and make the admin and the storefront disagree."""
    p = real_product()
    out = R.swatches(env, p, p["options_with_values"][1], option_index=2)
    seen = [s for s in sorted(SIZES, key=lambda s: out.index(s)) if s in out]
    assert seen == SIZES, \
        f"template reordered the option values: {seen}"


# ---------------------------------------------------------------------------
# Provenance record must stay in step with what was written
# ---------------------------------------------------------------------------
DOC = pathlib.Path(__file__).resolve().parent.parent / \
    "docs" / "HIVOLT-PRODUCT-DATA-PROVENANCE.md"


@case("Provenance", "record exists")
def t_doc_exists(env):
    assert DOC.exists(), f"{DOC} is missing"


@case("Provenance", "record names the product it describes")
def t_doc_gid(env):
    assert PRODUCT_GID in DOC.read_text(), \
        "provenance record does not carry the product GID"


@case("Provenance", "every written value appears in the record")
def t_doc_written(env):
    body = DOC.read_text()
    missing = [v for v in WRITTEN.values() if v not in body]
    assert not missing, f"written values absent from the record: {missing}"


@case("Provenance", "every blank field is accounted for in the record")
def t_doc_blank(env):
    body = DOC.read_text()
    missing = [k for k in BLANK if f"`spec.{k}`" not in body]
    assert not missing, f"blank fields absent from the record: {missing}"


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
    print(f"\nHIVOLT REAL-PRODUCT GATE: {total - len(failed)}/{total} "
          f"{'PASS' if not failed else 'FAIL'}")
    if failed:
        print("\nFailed:")
        for group, name in failed:
            print(f"  [{group}] {name}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
