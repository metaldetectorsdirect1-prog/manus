#!/usr/bin/env python3
"""
Build the Google/Meta product-feed attributes HIVOLT's catalogue is missing.

Google Merchant Center REQUIRES `age_group` and `gender` on every item in
Apparel & Accessories. Without them the item is disapproved, not merely
downranked — so a feed submitted today would lose all 110 products. Meta's
catalogue reads the same two attributes, and the Facebook & Instagram channel
is already installed on this store, so these values take effect there
immediately rather than waiting on the Google channel being added.

Shopify's Google & YouTube channel reads the `mm-google-shopping` namespace.
Everything else Google wants is already correct on the store and needs no
work here:

    brand              <- vendor, "HIVOLT" on all 110
    google_category    <- Standard Product Taxonomy, assigned and specific
    color / size       <- option names are literally "Color" and "Size",
                          which is what makes them auto-map
    mpn                <- variant SKU
    image_link         <- supplier photography, after 102 fabricated images
                          were removed; this was the actual feed blocker
    condition          <- defaults to "new"

gender is derived from tags, and the tags resolve without ambiguity:

    tag:unisex                     ->  unisex   (20)
    tag:womens and not tag:unisex  ->  female   (68)
    tag:mens   and not tag:unisex  ->  male     (22)
                                              ----
                                                110

The 20 products tagged `unisex` are exactly the 20 carrying both `womens` and
`mens`, and no active product carries none of the three — so every product
lands in exactly one bucket with nothing left over. That check is asserted
below rather than assumed.

age_group is "adult" for the whole catalogue. Nothing in it is cut for
children, and the size runs (2XS-4XL, 4-12) are adult runs.

custom_product = "TRUE" tells Google the item legitimately has no
manufacturer GTIN. Every variant's barcode is null because these are
own-brand blanks, and without this flag Google reports them as missing an
identifier.

Usage:  python3 audit/build-google-feed-attrs.py
Writes: audit/google-feed-attrs.jsonl   (batches of 25 for metafieldsSet)
"""

import json
import pathlib

HERE = pathlib.Path(__file__).parent
NS = "mm-google-shopping"
TEXT = "single_line_text_field"
BATCH = 25

FEMALE = [
    9571188736232, 9571190604008, 9571199451368, 9571207282920, 9571222323432,
    9571230089448, 9571232645352, 9571235856616, 9571245654248, 9571251683560,
    9571271016680, 9571271114984, 9571271442664, 9571271508200, 9571271770344,
    9571271835880, 9571271934184, 9571272065256, 9571272163560, 9571272720616,
    9571272982760, 9571273375976, 9571274031336, 9571274326248, 9571274621160,
    9571274883304, 9571275735272, 9571276226792, 9571277144296, 9571277373672,
    9571277996264, 9571278848232, 9571285663976, 9571285958888, 9571286515944,
    9571288056040, 9571292184808, 9571293429992, 9571294511336, 9571294871784,
    9571295625448, 9571321086184, 9571330261224, 9571331440872, 9571333308648,
    9571334848744, 9571345236200, 9571348480232, 9571353329896, 9571355427048,
    9571358933224, 9571362799848, 9571364897000, 9571367977192, 9571672031464,
    9571672588520, 9571673047272, 9571676618984, 9571755393256, 9572273684712,
    9572281286888, 9572283744488, 9572290330856, 9572300325096, 9572304683240,
    9572309205224, 9572343742696, 9575188332776,
]

MALE = [
    9571193192680, 9571203285224, 9571232481512, 9571234054376, 9571237888232,
    9571243098344, 9571271344360, 9571272458472, 9571273146600, 9571276423400,
    9571277701352, 9571280388328, 9571286319336, 9571286778088, 9571296149736,
    9571307946216, 9571669999848, 9571676094696, 9571678879976, 9571679600872,
    9572296130792, 9572602642664,
]

UNISEX = [
    9571143418088, 9571188277480, 9571188572392, 9572358684904, 9572372545768,
    9572386111720, 9572387389672, 9572407967976, 9572427530472, 9572448272616,
    9572470259944, 9572474323176, 9572479631592, 9572482515176, 9572483203304,
    9572484219112, 9572488118504, 9572491985128, 9572492771560, 9572493590760,
]


def main():
    groups = {"female": FEMALE, "male": MALE, "unisex": UNISEX}

    everything = FEMALE + MALE + UNISEX
    assert len(everything) == 110, f"expected 110 products, got {len(everything)}"
    assert len(set(everything)) == 110, "a product landed in more than one gender bucket"
    assert len(FEMALE) == 68 and len(MALE) == 22 and len(UNISEX) == 20

    fields = []
    for gender, ids in groups.items():
        for pid in ids:
            owner = f"gid://shopify/Product/{pid}"
            fields.append({"ownerId": owner, "namespace": NS, "key": "gender",
                           "type": TEXT, "value": gender})

    for pid in sorted(everything):
        owner = f"gid://shopify/Product/{pid}"
        fields.append({"ownerId": owner, "namespace": NS, "key": "age_group",
                       "type": TEXT, "value": "adult"})
        fields.append({"ownerId": owner, "namespace": NS, "key": "custom_product",
                       "type": TEXT, "value": "TRUE"})

    out = HERE / "google-feed-attrs.jsonl"
    with out.open("w", encoding="utf-8") as fh:
        for i in range(0, len(fields), BATCH):
            fh.write(json.dumps({"metafields": fields[i:i + BATCH]},
                                ensure_ascii=False) + "\n")

    lines = -(-len(fields) // BATCH)
    print(f"gender   female {len(FEMALE)} · male {len(MALE)} · unisex {len(UNISEX)}")
    print(f"age_group      adult × {len(everything)}")
    print(f"custom_product TRUE  × {len(everything)}")
    print(f"metafields     {len(fields)}")
    print(f"batches        {lines}  ->  {out}")


if __name__ == "__main__":
    main()
