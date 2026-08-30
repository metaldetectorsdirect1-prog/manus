#!/usr/bin/env python3
"""QA fixtures for the HIVOLT PDP release gate.

=============================================================================
THIS FILE CONTAINS NO REAL PRODUCT DATA.

Every measurement, composition, barcode and price below is invented for
testing. None of it came from a supplier, and none of it may be copied into
Shopify. The values are shaped like real ones so that layout, wrapping and
conversion are exercised realistically — that is the only reason they look
plausible. Each fixture product carries QA_MARKER in its title so a value that
ever escaped into the store would be obvious on sight.

This module is a plain Python file. It has no Shopify client and no network
call, so it cannot write to the store even by accident.
=============================================================================

The fixtures drive two consumers:

  site/check-hivolt-pdp.py    the release gate (assertions)
  site/render-pdp-preview.py  the browser QA page (Chromium)

Scenario coverage is deliberate. A PDP architecture that only works on a
fully populated product is not finished; the whole design intent is that
missing data removes UI rather than producing a blank or a placeholder. The
SCENARIOS table below is the list of ways data can be incomplete.
"""
from collections.abc import Mapping

QA_MARKER = "QA-FIXTURE"

# A real GTIN-13 check-digit-valid number is not needed — the resolver checks
# shape, not check digit — but using a well-known EAN keeps the value obviously
# synthetic rather than looking like a HIVOLT barcode.
FIXTURE_GTIN13 = "4006381333931"
FIXTURE_GTIN12 = "012345678905"


# ---------------------------------------------------------------------------
# Drops
# ---------------------------------------------------------------------------
def mf(value):
    """A metafield drop. Templates always read `.value`."""
    return {"value": value}


class OptionValue(Mapping):
    """Shopify's product_option_value: stringifies to its name, carries state.

    Liquid reaches `.available`, `.selected` and `.swatch` on it while `{{ v }}`
    prints the name, so the mock has to be both a mapping and a string.
    """

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

    def __repr__(self):
        return f"OptionValue({self._d['name']!r}, available={self._d['available']})"


def product(**over):
    """A minimal product drop. Scenarios override what they are testing."""
    base = {
        "id": 9900000000001,
        "title": f"{QA_MARKER} Pique Polo",
        "handle": "qa-fixture-pique-polo",
        "url": "/products/qa-fixture-pique-polo",
        "vendor": "HIVOLT",
        "description": "",
        "images": [],
        "featured_media": None,
        "variants": [],
        "options_with_values": [],
        "has_only_default_variant": False,
        "empty?": False,
        "selected_or_first_available_variant": None,
        "metafields": {"spec": {}, "custom": {}},
    }
    base.update(over)
    return base


def variant(**over):
    base = {
        "id": 4400000000001,
        "title": "Black / M",
        "sku": "",
        "barcode": None,
        "price": 6900,
        "available": True,
        "options": ["Black", "M"],
        "metafields": {"custom": {}, "mm-google-shopping": {}},
    }
    base.update(over)
    return base


# ---------------------------------------------------------------------------
# The golden product
# ---------------------------------------------------------------------------
# Colour axis. Two values carry real swatch colour, one carries a swatch image,
# one carries nothing at all (must fall back to a text button rather than a
# guessed CSS colour), and one is sold out in every size.
GOLDEN_COLOURS = [
    {"name": "Black",     "swatch": {"color": "#0f0f0f"}},
    {"name": "Bone",      "swatch": {"color": "#e8e4dc"}},
    {"name": "Volt",      "swatch": {"image": "/qa-fixture/volt-swatch.png"}},
    {"name": "Deep Sea",  "swatch": {}},                       # text fallback
    {"name": "Slate",     "swatch": {}, "sold_out": True},     # text + sold out
]

GOLDEN_SIZES = [
    {"name": "S"}, {"name": "M"}, {"name": "L"}, {"name": "XL"},
    {"name": "2XL", "sold_out": True, "surcharge": 500},
]


def _golden_variants():
    """Build the full colour x size matrix with per-variant identifier data.

    Identifier spread is the point of this matrix. Black carries a real
    barcode, Bone carries a per-variant MPN, Volt/M declares `none` as an
    override, and the rest fall through to the product default. One product
    therefore exercises every resolution path in a single JSON-LD render.
    """
    out = []
    vid = 4400000000001
    for c in GOLDEN_COLOURS:
        for s in GOLDEN_SIZES:
            available = not (c.get("sold_out") or s.get("sold_out"))
            price = 6900 + s.get("surcharge", 0)
            metafields = {"custom": {}, "mm-google-shopping": {}}

            barcode = None
            if c["name"] == "Black":
                barcode = FIXTURE_GTIN13
            elif c["name"] == "Bone" and s["name"] == "L":
                # A 12-digit UPC, to prove the length branch is not hardcoded to 13.
                barcode = FIXTURE_GTIN12

            if c["name"] == "Bone" and s["name"] != "L":
                metafields["mm-google-shopping"]["mpn"] = mf("QA-MPN-BONE-001")
            if c["name"] == "Volt" and s["name"] == "M":
                metafields["custom"]["identifier_mode"] = mf("none")
            if c["name"] == "Deep Sea" and s["name"] == "S":
                # Declares gtin but has no barcode: must fall through to none.
                metafields["custom"]["identifier_mode"] = mf("gtin")

            out.append(variant(
                id=vid,
                title=f"{c['name']} / {s['name']}",
                sku=f"QA-PQ-{c['name'][:3].upper()}-{s['name']}",
                barcode=barcode,
                price=price,
                available=available,
                options=[c["name"], s["name"]],
                metafields=metafields,
            ))
            vid += 1
    return out


def _option_values(axis, variants, index, selected_name=None):
    """Derive option values from the variant matrix, the way Shopify does.

    `available` is not asserted by the fixture — it is computed from whether any
    variant carrying that value is purchasable, so a test that changes the
    matrix cannot leave a stale availability flag behind.
    """
    values = []
    for entry in axis:
        available = any(v["available"] and v["options"][index] == entry["name"]
                        for v in variants)
        values.append(OptionValue(
            entry["name"],
            available=available,
            selected=(entry["name"] == selected_name),
            swatch=entry.get("swatch") or {},
        ))
    return values


GOLDEN_CHART = {
    "title": mf(f"{QA_MARKER} pique polo - unisex adult"),
    "measurement_basis": mf("garment_flat"),
    "source_unit": mf("cm"),
    "columns": mf([
        {"key": "chest", "label": "Chest"},
        {"key": "length", "label": "Length"},
        {"key": "sleeve", "label": "Sleeve"},
    ]),
    "rows": mf([
        # 51 is load-bearing: 51 / 2.54 = 20.07... which must render as 20.1.
        {"size": "S",   "values": {"chest": 51, "length": 70, "sleeve": 21}},
        {"size": "M",   "values": {"chest": 54, "length": 72, "sleeve": 21.5}},
        {"size": "L",   "values": {"chest": 57.5, "length": 74, "sleeve": 22}},
        # XL is missing one measurement: the cell must be a dash, not a guess.
        {"size": "XL",  "values": {"chest": 60.5, "length": 76}},
        {"size": "2XL", "values": {"chest": 64, "length": 78, "sleeve": 23}},
        # An entirely unmeasured size must be dropped from the table.
        {"size": "3XL", "values": {}},
    ]),
    "note": mf(f"{QA_MARKER} data. Measured flat across the chest, "
               "one inch below the armhole."),
    "source_reference": mf(f"{QA_MARKER} - not a supplier document"),
}

GOLDEN_SPEC = {
    "size_chart": mf(GOLDEN_CHART),
    "composition": mf("60% combed cotton / 40% recycled polyester"),
    "gsm": mf(220),
    "knit": mf("Pique"),
    "fit": mf("Regular"),
    "collar": mf("Ribbed knit-on collar with fused interlining"),
    "placket": mf("3-button, 15 cm, matched resin buttons"),
    "cuff": mf("Ribbed cuff"),
    "hem": mf("Straight hem with side vents"),
    "finish": mf("Garment-dyed"),
    "seams": mf("Flatlock, 4-thread"),
    "opacity": mf("Opaque under stretch"),
    "care": mf("Cold wash, hang dry, warm iron on reverse"),
    "origin": mf("Portugal"),
    "model_height_cm": mf(186),
    "model_wears_size": mf("M"),
    "benefits": mf([
        "220 g/m2 pique, published in the table below",
        "Measured size chart for every size in the range",
        "Garment-dyed, so the colour settles rather than fades",
    ]),
}

GOLDEN_IMAGES = [
    "/qa-fixture/polo-front.jpg",
    "/qa-fixture/polo-back.jpg",
    "/qa-fixture/polo-collar-detail.jpg",
]


def golden_product(**over):
    """A fully populated PDP: every implemented system has data to render."""
    variants = _golden_variants()
    first_available = next(v for v in variants if v["available"])
    options = [
        {"name": "Color",
         "values": _option_values(GOLDEN_COLOURS, variants, 0,
                                  selected_name=first_available["options"][0]),
         "selected_value": first_available["options"][0]},
        {"name": "Size",
         "values": _option_values(GOLDEN_SIZES, variants, 1,
                                  selected_name=first_available["options"][1]),
         "selected_value": first_available["options"][1]},
    ]
    p = product(
        title=f"{QA_MARKER} Pique Polo",
        description=("A short-sleeve pique polo. This description exists so the "
                     "structured data has something to truncate; it is fixture "
                     "text, not product copy."),
        images=GOLDEN_IMAGES,
        featured_media=GOLDEN_IMAGES[0],
        variants=variants,
        options_with_values=options,
        selected_or_first_available_variant=first_available,
        metafields={
            "spec": dict(GOLDEN_SPEC),
            "custom": {
                "feed_title": mf(f"{QA_MARKER} Pique Polo Shirt - Men's Short Sleeve"),
                "identifier_mode": mf("auto"),
                "mpn": mf("QA-MPN-PQ-DEFAULT"),
            },
        },
    )
    p.update(over)
    return p


# ---------------------------------------------------------------------------
# Degraded scenarios
# ---------------------------------------------------------------------------
# Each returns a product drop. The names match the release-QA document so a
# failing gate points straight at a documented scenario.
def _strip_spec(p, keep=()):
    spec = {k: v for k, v in p["metafields"]["spec"].items() if k in keep}
    p["metafields"] = {**p["metafields"], "spec": spec}
    return p


def scenario_a_full():
    return golden_product()


def scenario_b_no_specs():
    """Specs entirely absent. The whole specification block must disappear."""
    p = golden_product()
    return _strip_spec(p, keep=("size_chart",))


def scenario_c_specs_no_chart():
    """Specs present, no size chart. No trigger, no dialog, specs still render."""
    p = golden_product()
    spec = {k: v for k, v in p["metafields"]["spec"].items() if k != "size_chart"}
    p["metafields"] = {**p["metafields"], "spec": spec}
    return p


def scenario_d_no_swatches():
    """No option value carries swatch data: every value becomes a text button."""
    p = golden_product()
    variants = p["variants"]
    plain = [{"name": c["name"], "swatch": {}, **({"sold_out": True} if c.get("sold_out") else {})}
             for c in GOLDEN_COLOURS]
    first = p["selected_or_first_available_variant"]
    p["options_with_values"] = [
        {"name": "Color",
         "values": _option_values(plain, variants, 0, selected_name=first["options"][0]),
         "selected_value": first["options"][0]},
        p["options_with_values"][1],
    ]
    return p


def scenario_e_one_sold_out_variant():
    """A single sold-out variant among available ones."""
    p = golden_product()
    for v in p["variants"]:
        v["available"] = True
    p["variants"][3]["available"] = False
    first = next(v for v in p["variants"] if v["available"])
    p["selected_or_first_available_variant"] = first
    return p


def scenario_f_declared_gtin_no_barcode():
    """Product declares gtin mode but no variant has a barcode."""
    p = golden_product()
    for v in p["variants"]:
        v["barcode"] = None
        v["metafields"]["mm-google-shopping"] = {}
        v["metafields"]["custom"] = {}
    p["metafields"]["custom"] = {**p["metafields"]["custom"],
                                 "identifier_mode": mf("gtin"),
                                 "mpn": mf("")}
    return p


def scenario_g_no_identifier():
    """Nothing identifies the item: identifier_exists must be no."""
    p = scenario_f_declared_gtin_no_barcode()
    p["metafields"]["custom"] = {**p["metafields"]["custom"],
                                 "identifier_mode": mf("auto")}
    return p


def scenario_h_blank_feed_title():
    p = golden_product()
    p["metafields"]["custom"] = {**p["metafields"]["custom"], "feed_title": mf("")}
    return p


def scenario_i_single_variant():
    """A simple product: one default variant, no options."""
    v = variant(id=4400000009999, title="Default Title", sku="QA-SIMPLE-001",
                barcode=None, price=4900, available=True, options=["Default Title"])
    return product(
        title=f"{QA_MARKER} Simple Product",
        handle="qa-fixture-simple",
        url="/products/qa-fixture-simple",
        description="A single-variant fixture product.",
        images=["/qa-fixture/simple.jpg"],
        variants=[v],
        options_with_values=[],
        has_only_default_variant=True,
        selected_or_first_available_variant=v,
        metafields={"spec": {}, "custom": {}},
    )


def scenario_j_bare_minimum():
    """Optional structured-data inputs entirely absent: no description, no
    images, no vendor, no sku, no identifier."""
    v = variant(id=4400000008888, title="Default Title", sku="", barcode=None,
                price=2500, available=False, options=["Default Title"])
    return product(
        title=f"{QA_MARKER} Bare Product",
        handle="qa-fixture-bare",
        url="/products/qa-fixture-bare",
        vendor="",
        description="",
        images=[],
        variants=[v],
        options_with_values=[],
        has_only_default_variant=True,
        selected_or_first_available_variant=v,
        metafields={"spec": {}, "custom": {}},
    )


SCENARIOS = {
    "A_full": scenario_a_full,
    "B_no_specs": scenario_b_no_specs,
    "C_specs_no_chart": scenario_c_specs_no_chart,
    "D_no_swatches": scenario_d_no_swatches,
    "E_one_sold_out": scenario_e_one_sold_out_variant,
    "F_declared_gtin_no_barcode": scenario_f_declared_gtin_no_barcode,
    "G_no_identifier": scenario_g_no_identifier,
    "H_blank_feed_title": scenario_h_blank_feed_title,
    "I_single_variant": scenario_i_single_variant,
    "J_bare_minimum": scenario_j_bare_minimum,
}
