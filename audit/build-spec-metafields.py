#!/usr/bin/env python3
"""
Build the spec.* metafield payload for HIVOLT's active catalogue.

Every value here was transcribed from the Tapstitch supplier copy already
published in the product's own Shopify description. Nothing is inferred,
converted, or averaged. A product whose description does not state a figure
is absent from SPEC and gets no metafield — the product template renders a
specification row only where a value exists, so those sheets stay short
rather than wrong.

Two deliberate omissions, both recorded rather than filled:

  performance-short-sleeve-t-shirt   description publishes no spec at all
  womens-open-back-tennis-dress      same

  soft-hooded-sports-jacket          publishes "3.8 oz/yd²" but never a g/m²
                                     figure. 3.8 oz/yd² is 130 g/m² elsewhere
                                     in this same catalogue, but converting a
                                     unit is not the same as quoting a source,
                                     so gsm is left unset and composition only
                                     is written.

One sourcing note:

  women-s-high-rise-topstitching-leggings takes gsm from its hivolt.lede
  metafield, which already states 220 g/m² on the live product page, rather
  than from the description. Leaving it blank would put the spec sheet in
  contradiction with the lede directly above it on the same page.

Usage:  python3 audit/build-spec-metafields.py
Writes: audit/spec-metafields.jsonl   (bulkOperationRunMutation variables)
"""

import json
import pathlib

HERE = pathlib.Path(__file__).parent

# The care string is byte-identical across every Tapstitch-format description.
# It is applied only to the products confirmed by full-text search to carry it.
CARE = ("Machine wash at 30°C, gentle cycle · Do not bleach · Tumble dry low · "
        "Iron low, avoid the print · Do not dry clean")

ID = {
    "performance-short-sleeve-t-shirt": 9571143418088,
    "soft-hooded-sports-jacket": 9571188277480,
    "performance-long-sleeve-t-shirt": 9571188572392,
    "women-s-cropped-sports-bra": 9571188736232,
    "womens-performance-crop-t-shirt": 9571190604008,
    "men-s-jacquard-slim-mesh-t-shirt": 9571193192680,
    "womens-high-rise-flared-yoga-pants": 9571199451368,
    "mens-drawstring-shorts": 9571203285224,
    "cropped-half-zip-hoodie": 9571207282920,
    "women-s-high-rise-topstitching-leggings": 9571222323432,
    "womens-full-zip-sports-jacket": 9571230089448,
    "mens-regular-fit-performance-t-shirt": 9571232481512,
    "womens-topstitching-yoga-tank-top": 9571232645352,
    "men-s-quarter-zip-raglan-training-t-shirt": 9571234054376,
    "womens-u-neck-yoga-romper": 9571235856616,
    "classic-stripe-trim-basketball-shorts": 9571237888232,
    "men-s-lightweight-sport-jersey": 9571243098344,
    "womens-halter-neck-yoga-sports-bra": 9571245654248,
    "womens-yoga-tank-top": 9571251683560,
    "women-s-color-block-yoga-sports-bra": 9571271016680,
    "womens-halter-v-neck-yoga-tank-top": 9571271114984,
    "mens-performance-tank-top": 9571271344360,
    "womens-flared-drawstring-yoga-pants": 9571271442664,
    "womens-high-rise-ankle-length-leggings": 9571271508200,
    "womens-yoga-cropped-tube-top": 9571271770344,
    "womens-color-block-yoga-tank-top": 9571271835880,
    "women-s-color-block-yoga-tank-top": 9571271934184,
    "cropped-half-zip-sweatshirt": 9571272065256,
    "cropped-zip-through-hoodie": 9571272163560,
    "men-s-jacquard-performance-tank-top": 9571272458472,
    "womens-high-rise-yoga-pants": 9571272720616,
    "womens-high-rise-pocket-yoga-shorts": 9571272982760,
    "mens-color-block-raglan-t-shirt": 9571273146600,
    "womens-color-block-performance-t-shirt": 9571273375976,
    "womens-cutout-long-sleeve-yoga-shrug": 9571274031336,
    "womens-color-block-yoga-sports-bra": 9571274326248,
    "women-s-slim-fit-full-zip-yoga-jacket": 9571274621160,
    "women-s-quarter-zip-yoga-pullover": 9571274883304,
    "women-s-polo-yoga-tank-top": 9571275735272,
    "women-s-tight-cropped-sports-bra": 9571276226792,
    "men-s-slim-fit-topstitch-tank-top": 9571276423400,
    "womens-topstitching-yoga-sports-bra": 9571277144296,
    "womens-high-rise-flared-leggings": 9571277373672,
    "men-s-quarter-zip-performance-polo-shirt": 9571277701352,
    "womens-slim-fit-quarter-zip-polo-shirt": 9571277996264,
    "womens-color-block-yoga-leggings": 9571278848232,
    "mens-piping-straight-leg-sweatpants": 9571280388328,
    "women-s-twist-front-v-neck-sports-bra": 9571285663976,
    "womens-cropped-v-neck-sports-bra": 9571285958888,
    "mens-lightweight-performance-t-shirt": 9571286319336,
    "women-s-high-rise-color-block-yoga-shorts": 9571286515944,
    "mens-raglan-sleeve-performance-t-shirt": 9571286778088,
    "womens-u-neck-yoga-sports-bra": 9571288056040,
    "womens-ruched-halter-neck-sports-bra": 9571292184808,
    "womens-ruched-halter-neck-yoga-tank-top": 9571293429992,
    "women-s-pleated-a-line-tennis-skirt": 9571294511336,
    "womens-drawstring-bermuda-shorts": 9571294871784,
    "womens-criss-cross-band-sports-bra": 9571295625448,
    "men-s-tapered-leg-drawstring-joggers": 9571296149736,
    "men-s-quarter-zip-performance-long-sleeve-t-shirt": 9571307946216,
    "women-s-cropped-sports-bra-1": 9571321086184,
    "womens-tight-yoga-sports-bra": 9571330261224,
    "womens-full-zip-ruched-bodysuit": 9571331440872,
    "womens-yoga-sports-bra": 9571333308648,
    "womens-high-rise-ankle-length-yoga-leggings": 9571334848744,
    "womens-halter-yoga-tank-top": 9571345236200,
    "women-s-color-block-ruched-v-neck-sports-bra": 9571348480232,
    "womens-regular-fit-crewneck-t-shirt": 9571353329896,
    "women-s-faux-denim-sports-bra": 9571355427048,
    "womens-high-rise-straight-leg-yoga-pants": 9571358933224,
    "womens-halter-yoga-sports-bra": 9571362799848,
    "womens-pleated-a-line-skirt": 9571364897000,
    "women-s-faux-denim-zip-fly-leggings": 9571367977192,
    "mens-drawstring-joggers": 9571669999848,
    "womens-cropped-yoga-tank-top": 9571672031464,
    "womens-high-rise-a-line-skirt": 9571672588520,
    "womens-high-rise-wide-leg-pants": 9571673047272,
    "mens-regular-fit-performance-shorts": 9571676094696,
    "womens-quarter-zip-yoga-romper": 9571676618984,
    "men-s-tight-cycling-shorts": 9571678879976,
    "mens-drawstring-basketball-shorts": 9571679600872,
    "womens-high-rise-yoga-shorts": 9571755393256,
    "women-s-high-waisted-ankle-leggings": 9572273684712,
    "women-s-raglan-training-t-shirt": 9572281286888,
    "womens-open-back-tennis-dress": 9572283744488,
    "women-s-color-block-a-line-skirt": 9572290330856,
    "men-s-raglan-reflective-t-shirt": 9572296130792,
    "women-s-high-waisted-pocket-biker-shorts": 9572300325096,
    "women-s-high-waisted-flare-leggings": 9572304683240,
    "women-s-solid-high-rise-leggings": 9572309205224,
    "womens-high-rise-tight-yoga-shorts": 9572343742696,
    "two-tone-fleeced-varsity-jacket": 9572358684904,
    "two-tone-raglan-sleeve-varsity-jacket": 9572372545768,
    "unisex-raglan-sleeve-mesh-boxy-t-shirt": 9572386111720,
    "unisex-color-block-polo-shirt": 9572387389672,
    "unisex-striped-raglan-jersey": 9572407967976,
    "unisex-boxy-v-neck-soccer-jersey": 9572427530472,
    "unisex-color-block-jacquard-soccer-jersey": 9572448272616,
    "unisex-striped-raglan-long-sleeve-t-shirt": 9572470259944,
    "unisex-paneled-long-sleeve-jersey": 9572474323176,
    "unisex-boxy-striped-collared-soccer-jersey": 9572479631592,
    "unisex-paneled-raglan-soccer-jersey": 9572482515176,
    "unisex-mesh-basketball-shorts": 9572483203304,
    "unisex-color-block-long-sleeve-jersey": 9572484219112,
    "unisex-panel-mesh-sleeveless-hoodie": 9572488118504,
    "unisex-color-block-v-neck-t-shirt": 9572491985128,
    "unisex-color-block-v-neck-t-shirt-1": 9572492771560,
    "unisex-color-block-raglan-t-shirt": 9572493590760,
    "men-s-lightweight-performance-t-shirt": 9572602642664,
    "voltcore-2-piece-set-twist-front-bra-flare-leggings": 9575188332776,
}

# handle -> (gsm or None, composition or None, seams or None)
SPEC = {
    "soft-hooded-sports-jacket": (None, "100% polyester", None),
    "performance-long-sleeve-t-shirt": (200, "87% polyester, 13% spandex", None),
    "women-s-cropped-sports-bra": (230, "89% polyester, 11% spandex", None),
    "womens-performance-crop-t-shirt": (220, "82% polyamide, 18% elastane", None),
    "men-s-jacquard-slim-mesh-t-shirt": (180, "92% polyester, 8% spandex", None),
    "womens-high-rise-flared-yoga-pants": (220, "78% polyamide, 22% elastane", None),
    "mens-drawstring-shorts": (165, "77% nylon, 23% spandex", None),
    "cropped-half-zip-hoodie": (320, "28% cotton, 72% polyester", None),
    "women-s-high-rise-topstitching-leggings": (220, "78% polyamide, 22% elastane", None),
    "womens-full-zip-sports-jacket": (230, "78% polyamide, 22% elastane", None),
    "mens-regular-fit-performance-t-shirt": (130, "100% polyester", None),
    "womens-topstitching-yoga-tank-top": (220, "78% polyamide, 22% elastane", None),
    "men-s-quarter-zip-raglan-training-t-shirt": (220, "96% polyester, 4% spandex", None),
    "womens-u-neck-yoga-romper": (220, "75% nylon, 25% elastane", None),
    "classic-stripe-trim-basketball-shorts": (160, "100% polyester", None),
    "men-s-lightweight-sport-jersey": (160, "100% polyester", None),
    "womens-halter-neck-yoga-sports-bra": (220, "78% polyamide, 22% elastane", None),
    "womens-yoga-tank-top": (220, "80% nylon, 20% spandex", None),
    "women-s-color-block-yoga-sports-bra": (220, "78% polyamide, 22% elastane", None),
    "womens-halter-v-neck-yoga-tank-top": (220, "80% nylon, 20% spandex", None),
    "mens-performance-tank-top": (185, "87% polyester, 13% spandex", None),
    "womens-flared-drawstring-yoga-pants": (240, "79% nylon, 21% spandex", None),
    "womens-high-rise-ankle-length-leggings": (230, "89% polyester, 11% spandex", None),
    "womens-yoga-cropped-tube-top": (220, "80% nylon, 20% spandex", None),
    "womens-color-block-yoga-tank-top": (225, "Outer 78% polyamide, 22% elastane · Inner 82% polyamide, 18% elastane · Cup lining 95% polyamide, 5% elastane", None),
    "women-s-color-block-yoga-tank-top": (220, "Outer 82% polyamide, 18% elastane · Inner 80% polyester, 20% elastane", None),
    "cropped-half-zip-sweatshirt": (320, "28% cotton, 72% polyester", None),
    "cropped-zip-through-hoodie": (320, "28% cotton, 72% polyester", None),
    "men-s-jacquard-performance-tank-top": (180, "92% polyester, 8% spandex", None),
    "womens-high-rise-yoga-pants": (220, "80% nylon, 20% spandex", None),
    "womens-high-rise-pocket-yoga-shorts": (230, "78% polyamide, 22% elastane", None),
    "mens-color-block-raglan-t-shirt": (175, "87.5% polyester, 12.5% spandex", None),
    "womens-color-block-performance-t-shirt": (220, "82% polyamide, 18% elastane", None),
    "womens-cutout-long-sleeve-yoga-shrug": (220, "75% nylon, 25% spandex", None),
    "womens-color-block-yoga-sports-bra": (250, "Outer 80% polyester, 20% elastane · Inner 94% polyester, 6% elastane", None),
    "women-s-slim-fit-full-zip-yoga-jacket": (230, "75% nylon, 25% spandex", None),
    "women-s-quarter-zip-yoga-pullover": (165, "91% polyester, 9% spandex", None),
    "women-s-polo-yoga-tank-top": (320, "Outer 92% nylon, 8% elastane · Inner 92% nylon, 8% elastane", None),
    "women-s-tight-cropped-sports-bra": (220, "80% nylon, 20% spandex", None),
    "men-s-slim-fit-topstitch-tank-top": (180, "87% polyester, 13% spandex", None),
    "womens-topstitching-yoga-sports-bra": (220, "78% polyamide, 22% elastane", None),
    "womens-high-rise-flared-leggings": (220, "80% nylon, 20% spandex", None),
    "men-s-quarter-zip-performance-polo-shirt": (175, "79.2% nylon, 20.8% spandex", None),
    "womens-slim-fit-quarter-zip-polo-shirt": (160, "91% polyamide, 9% elastane", None),
    "womens-color-block-yoga-leggings": (250, "80% polyester, 20% elastane", None),
    "mens-piping-straight-leg-sweatpants": (285, "92% polyester, 8% spandex", None),
    "women-s-twist-front-v-neck-sports-bra": (220, "75% nylon, 25% spandex", "Flatlock"),
    "womens-cropped-v-neck-sports-bra": (220, "75% nylon, 25% spandex", None),
    "mens-lightweight-performance-t-shirt": (170, "87% nylon, 13% spandex", None),
    "women-s-high-rise-color-block-yoga-shorts": (220, "82% polyamide, 18% elastane", None),
    "mens-raglan-sleeve-performance-t-shirt": (120, "100% polyester", None),
    "womens-u-neck-yoga-sports-bra": (220, "80% nylon, 20% spandex", None),
    "womens-ruched-halter-neck-sports-bra": (220, "75% nylon, 25% spandex", None),
    "womens-ruched-halter-neck-yoga-tank-top": (220, "75% nylon, 25% elastane", None),
    "women-s-pleated-a-line-tennis-skirt": (320, "92% nylon, 8% elastane, outer and inner", None),
    "womens-drawstring-bermuda-shorts": (140, "Outer 88% polyester, 12% elastane · Inner 80% nylon, 20% elastane", None),
    "womens-criss-cross-band-sports-bra": (250, "Outer 80% polyester, 20% elastane · Inner 94% polyester, 6% elastane", None),
    "men-s-tapered-leg-drawstring-joggers": (330, "92% polyester, 8% spandex", None),
    "men-s-quarter-zip-performance-long-sleeve-t-shirt": (190, "93% polyester, 7% spandex", None),
    "women-s-cropped-sports-bra-1": (220, "75% nylon, 25% spandex", None),
    "womens-tight-yoga-sports-bra": (220, "78% polyamide, 22% elastane", None),
    "womens-full-zip-ruched-bodysuit": (315, "83% nylon, 17% spandex", None),
    "womens-yoga-sports-bra": (220, "75% nylon, 25% spandex", None),
    "womens-high-rise-ankle-length-yoga-leggings": (270, "80% polyester, 20% elastane", None),
    "womens-halter-yoga-tank-top": (220, "80% nylon, 20% spandex", None),
    "women-s-color-block-ruched-v-neck-sports-bra": (230, "75% nylon, 25% spandex", None),
    "womens-regular-fit-crewneck-t-shirt": (130, "100% polyester", None),
    "women-s-faux-denim-sports-bra": (200, "86% nylon, 14% spandex", None),
    "womens-high-rise-straight-leg-yoga-pants": (230, "80% nylon, 20% spandex", None),
    "womens-halter-yoga-sports-bra": (270, "80% polyester, 20% elastane", None),
    "womens-pleated-a-line-skirt": (220, "80% polyester, 20% elastane", None),
    "women-s-faux-denim-zip-fly-leggings": (200, "86% nylon, 14% spandex", None),
    "mens-drawstring-joggers": (130, "95% polyester, 5% spandex", None),
    "womens-cropped-yoga-tank-top": (240, "79% nylon, 21% spandex", None),
    "womens-high-rise-a-line-skirt": (220, "78% polyamide, 22% elastane", None),
    "womens-high-rise-wide-leg-pants": (140, "88% nylon, 12% spandex", None),
    "mens-regular-fit-performance-shorts": (120, "90% nylon, 10% spandex", None),
    "womens-quarter-zip-yoga-romper": (230, "75% nylon, 25% elastane", None),
    "men-s-tight-cycling-shorts": (180, "87% polyester, 13% spandex", "Flatlock"),
    "mens-drawstring-basketball-shorts": (120, "90.6% nylon, 9.4% spandex", None),
    "womens-high-rise-yoga-shorts": (220, "80% nylon, 20% spandex", None),
    "women-s-high-waisted-ankle-leggings": (220, "80% nylon, 20% spandex", None),
    "women-s-raglan-training-t-shirt": (170, "47% lyocell, 47% cotton, 6% spandex", None),
    "women-s-color-block-a-line-skirt": (220, "78% polyamide, 22% elastane", None),
    "men-s-raglan-reflective-t-shirt": (91, "100% polyester", None),
    "women-s-high-waisted-pocket-biker-shorts": (210, "80% polyester, 20% spandex", None),
    "women-s-high-waisted-flare-leggings": (220, "80% nylon, 20% spandex", None),
    "women-s-solid-high-rise-leggings": (220, "75% nylon, 25% spandex", None),
    "womens-high-rise-tight-yoga-shorts": (220, "80% nylon, 20% spandex", None),
    "two-tone-fleeced-varsity-jacket": (380, "70% polyester, 30% cotton", None),
    "two-tone-raglan-sleeve-varsity-jacket": (380, "Main 61.9% cotton, 38.1% polyester · Contrast 100% polyester", None),
    "unisex-raglan-sleeve-mesh-boxy-t-shirt": (255, "100% polyester", None),
    "unisex-color-block-polo-shirt": (330, "71% cotton, 29% polyester", None),
    "unisex-striped-raglan-jersey": (150, "100% polyester", None),
    "unisex-boxy-v-neck-soccer-jersey": (220, "93% polyester, 7% spandex", None),
    "unisex-color-block-jacquard-soccer-jersey": (150, "100% polyester", None),
    "unisex-striped-raglan-long-sleeve-t-shirt": (220, "100% polyester", None),
    "unisex-paneled-long-sleeve-jersey": (225, "100% polyester", None),
    "unisex-boxy-striped-collared-soccer-jersey": (170, "100% polyester", None),
    "unisex-paneled-raglan-soccer-jersey": (250, "100% polyester", None),
    "unisex-mesh-basketball-shorts": (240, "100% polyester", None),
    "unisex-color-block-long-sleeve-jersey": (170, "100% polyester", None),
    "unisex-panel-mesh-sleeveless-hoodie": (240, "Fabric A 100% polyester · Fabric B 83% cotton, 17% polyester", None),
    "unisex-color-block-v-neck-t-shirt": (230, "100% cotton", None),
    "unisex-color-block-v-neck-t-shirt-1": (230, "100% cotton", None),
    "unisex-color-block-raglan-t-shirt": (230, "100% cotton", None),
    "men-s-lightweight-performance-t-shirt": (170, "77% nylon, 23% spandex", None),
    "voltcore-2-piece-set-twist-front-bra-flare-leggings": (220, "78% polyamide, 22% elastane", None),
}

# Confirmed by full-text search to carry the standard Tapstitch care line.
CARE_HANDLES = {
    "womens-yoga-tank-top", "women-s-color-block-yoga-sports-bra",
    "womens-halter-v-neck-yoga-tank-top", "mens-performance-tank-top",
    "womens-flared-drawstring-yoga-pants", "womens-high-rise-ankle-length-leggings",
    "womens-yoga-cropped-tube-top", "womens-color-block-yoga-tank-top",
    "women-s-color-block-yoga-tank-top", "cropped-half-zip-sweatshirt",
    "cropped-zip-through-hoodie", "men-s-jacquard-performance-tank-top",
    "womens-high-rise-yoga-pants", "womens-high-rise-pocket-yoga-shorts",
    "mens-color-block-raglan-t-shirt", "womens-color-block-performance-t-shirt",
    "womens-cutout-long-sleeve-yoga-shrug", "womens-color-block-yoga-sports-bra",
    "women-s-slim-fit-full-zip-yoga-jacket", "women-s-quarter-zip-yoga-pullover",
    "women-s-polo-yoga-tank-top", "women-s-tight-cropped-sports-bra",
    "men-s-slim-fit-topstitch-tank-top", "womens-topstitching-yoga-sports-bra",
    "womens-high-rise-flared-leggings", "men-s-quarter-zip-performance-polo-shirt",
    "womens-slim-fit-quarter-zip-polo-shirt", "womens-color-block-yoga-leggings",
    "mens-piping-straight-leg-sweatpants", "womens-cropped-v-neck-sports-bra",
    "mens-lightweight-performance-t-shirt", "women-s-high-rise-color-block-yoga-shorts",
    "mens-raglan-sleeve-performance-t-shirt", "womens-u-neck-yoga-sports-bra",
    "womens-ruched-halter-neck-sports-bra", "womens-ruched-halter-neck-yoga-tank-top",
    "womens-drawstring-bermuda-shorts", "womens-criss-cross-band-sports-bra",
    "womens-tight-yoga-sports-bra", "womens-full-zip-ruched-bodysuit",
    "womens-yoga-sports-bra", "womens-high-rise-ankle-length-yoga-leggings",
    "womens-halter-yoga-tank-top", "women-s-color-block-ruched-v-neck-sports-bra",
    "womens-regular-fit-crewneck-t-shirt", "womens-high-rise-straight-leg-yoga-pants",
    "womens-halter-yoga-sports-bra", "womens-pleated-a-line-skirt",
    "mens-drawstring-joggers", "womens-cropped-yoga-tank-top",
    "womens-high-rise-a-line-skirt", "womens-high-rise-wide-leg-pants",
    "womens-quarter-zip-yoga-romper", "mens-drawstring-basketball-shorts",
    "womens-high-rise-yoga-shorts", "women-s-high-waisted-ankle-leggings",
    "women-s-raglan-training-t-shirt", "women-s-color-block-a-line-skirt",
    "men-s-raglan-reflective-t-shirt", "women-s-high-waisted-pocket-biker-shorts",
    "women-s-solid-high-rise-leggings", "womens-high-rise-tight-yoga-shorts",
    "two-tone-raglan-sleeve-varsity-jacket", "unisex-raglan-sleeve-mesh-boxy-t-shirt",
    "unisex-color-block-polo-shirt", "unisex-striped-raglan-jersey",
    "unisex-boxy-v-neck-soccer-jersey", "unisex-color-block-jacquard-soccer-jersey",
    "unisex-striped-raglan-long-sleeve-t-shirt", "unisex-paneled-long-sleeve-jersey",
    "unisex-boxy-striped-collared-soccer-jersey", "unisex-paneled-raglan-soccer-jersey",
    "unisex-mesh-basketball-shorts", "unisex-color-block-long-sleeve-jersey",
    "unisex-panel-mesh-sleeveless-hoodie", "unisex-color-block-v-neck-t-shirt",
    "unisex-color-block-v-neck-t-shirt-1", "unisex-color-block-raglan-t-shirt",
    "men-s-lightweight-performance-t-shirt",
}

BATCH = 25  # metafieldsSet accepts at most 25 metafields per call


def main():
    unknown = (set(SPEC) | CARE_HANDLES) - set(ID)
    if unknown:
        raise SystemExit(f"handles with no product id: {sorted(unknown)}")

    fields = []
    for handle, (gsm, composition, seams) in sorted(SPEC.items()):
        owner = f"gid://shopify/Product/{ID[handle]}"
        if gsm is not None:
            fields.append({"ownerId": owner, "namespace": "spec", "key": "gsm",
                           "type": "number_integer", "value": str(gsm)})
        if composition:
            fields.append({"ownerId": owner, "namespace": "spec", "key": "composition",
                           "type": "single_line_text_field", "value": composition})
        if seams:
            fields.append({"ownerId": owner, "namespace": "spec", "key": "seams",
                           "type": "single_line_text_field", "value": seams})

    for handle in sorted(CARE_HANDLES):
        fields.append({"ownerId": f"gid://shopify/Product/{ID[handle]}",
                       "namespace": "spec", "key": "care",
                       "type": "single_line_text_field", "value": CARE})

    out = HERE / "spec-metafields.jsonl"
    with out.open("w", encoding="utf-8") as fh:
        for i in range(0, len(fields), BATCH):
            fh.write(json.dumps({"metafields": fields[i:i + BATCH]},
                                ensure_ascii=False) + "\n")

    lines = -(-len(fields) // BATCH)
    covered = len(SPEC)
    print(f"products with at least one published figure : {covered} of 110 active")
    print(f"  gsm         : {sum(1 for v in SPEC.values() if v[0] is not None)}")
    print(f"  composition : {sum(1 for v in SPEC.values() if v[1])}")
    print(f"  seams       : {sum(1 for v in SPEC.values() if v[2])}")
    print(f"  care        : {len(CARE_HANDLES)}")
    print(f"metafields    : {len(fields)}")
    print(f"jsonl lines   : {lines}  ->  {out}")
    print(f"bytes         : {out.stat().st_size}")


if __name__ == "__main__":
    main()
