# HIVOLT Classic Cotton Polo — measurement request

**Status: OPEN. This is the blocking item for the product size guide.**

> **Do this first — it takes a minute and may make the rest unnecessary.**
>
> The product carries two images named `hv-h01-detail-1.webp` and
> `hv-h01-detail-2.webp`. Nobody has been able to look at them: the automation
> environment cannot reach Shopify's CDN, so their contents are unknown. If
> either turns out to be a supplier size chart or measurement diagram, the
> measurements may already exist and this request can be narrowed or dropped.
>
> Open Shopify Admin → Products → *HIVOLT Classic Cotton Polo — Men's Short
> Sleeve* → Media, and view the last two images. If either shows a size table
> or a measurement diagram, send a screenshot instead of completing §5.

The storefront size guide is built, tested and deployed to the draft theme. It
renders nothing on this product because no garment measurement exists for it —
not in the repository, not in Shopify, not in any supplier document we hold.
The supplier gives a **recommended body weight** per size and no garment
dimensions at all.

A body weight is not a garment measurement and cannot be converted into one.
Nothing will be published until the numbers below come back from someone with
a tape measure and the actual garment.

Hand this document to the supplier, or to whoever holds a physical sample.

---

## 1. Product identity

| | |
|---|---|
| Title | HIVOLT Classic Cotton Polo — Men's Short Sleeve |
| Handle | `hivolt-classic-cotton-polo-mens-short-sleeve` |
| Shopify product ID | `gid://shopify/Product/9603121774824` |
| Status | DRAFT — not visible to customers |
| SKU family | `HV-H01-…` |
| Variants | 20 (6 colours × 5 sizes, sparse) |
| Supplier listing on file | `https://www.aliexpress.com/item/1005002281827487.html` |
| Supplier colour codes on file | `PL208` (Navy, White, Light Blue, Dark Grey), `PL205` (Black), `AX-511` (Army Green) |

**Note the colour codes.** Three different supplier item codes appear across
six colourways. Confirm whether all six are cut from the same pattern. If they
are not, we need a separate measurement set per pattern, and the question in
§6 covers it.

---

## 2. Measurement basis — pick one and use it for every number

Measure the **garment laid flat**, not the wearer, and not the garment on a
body or hanger.

Lay the polo flat on a hard surface. Smooth it out without stretching the
fabric. Fasten the placket buttons. Every measurement below is taken in that
position.

If your production spec is recorded on a different basis — half-chest versus
full chest circumference, for instance — **tell us which**, and send the
numbers as you record them. We will store the basis you used rather than
convert it. Do not convert anything to match this document.

---

## 3. Measurements requested

These are **REQUESTED MEASUREMENTS**, not values we hold. Every cell is empty
because we have no data for it.

### Chest width
Garment flat, measured straight across from armhole seam to armhole seam,
approximately **2.5 cm (1 in) below the armhole**. Record the flat width, not
the doubled circumference. If your spec records full circumference instead,
say so and send the circumference.

### Shoulder width
Straight across the back, from the outer edge of one shoulder seam to the outer
edge of the other. Follow the straight line, not the curve of the seam.

### Body length
From the **highest point of the shoulder** — where the shoulder seam meets the
collar — straight down to the bottom hem. State whether it includes the collar.

### Sleeve length
From the shoulder seam at the armhole, along the outside of the sleeve, to the
sleeve opening.

If your spec sheet carries measurements we have not listed — collar height,
placket length, hem opening, cuff width — send them too. We will publish
whatever you can stand behind and leave out whatever you cannot.

---

## 4. Required unit

**Centimetres**, to one decimal place.

Send centimetres even if your spec is in inches, unless your production
document is authoritative in inches — in that case send inches and say so. The
storefront converts between the two at display time, so we store your original
unit and never a converted number. Sending us a converted value loses the
original precision for no benefit.

---

## 5. Data table — please fill in

The left column contains the **exact size values as they exist in our store
today**. Do not rename them. If your factory uses different labels for the same
garments, add a column mapping yours to ours rather than replacing ours.

| Shopify size value | Chest width | Shoulder | Body length | Sleeve length |
|---|---:|---:|---:|---:|
| `EUR S 60-70kg` | | | | |
| `EUR M 70-80kg` | | | | |
| `EUR L 80-90kg` | | | | |
| `EUR XL 90-100kg` | | | | |
| `EUR XXL 100-105kg` | | | | |

All values in cm. One decimal place. Leave a cell blank rather than estimating
it — a visible gap is worth more to us than a number nobody measured.

---

## 6. Questions about the size labels

Our store currently sells these garments under labels like
`EUR S 60-70kg`. Our own product description says the kilogram range is a
recommended body weight, but that description was transcribed from your listing
rather than from a specification document, and we have not been able to confirm
it with you. Please answer directly:

1. **What does `EUR S 60-70kg` mean?** Specifically, is `60-70kg` the
   recommended body weight of the wearer, or does it refer to something else?
2. **Does `EUR` denote a European sizing standard**, or is it part of your
   internal product code?
3. **Is there an equivalent international alpha size** (S / M / L / XL / XXL)
   that this garment is also sold under? If your `EUR S` is what another market
   would call `M`, we need to know before a customer orders.
4. **Is the same physical garment sold under any other size label** — a numeric
   EU size, a US size, a JP size?
5. **What production tolerance do you work to**, in ± cm, per measurement?
6. **Do all six colourways share one pattern?** The three supplier codes on
   file (`PL208`, `PL205`, `AX-511`) suggest they may not. If they differ, send
   one table per pattern.

---

## 7. Evidence we need alongside the numbers

A filled-in table is enough to get the size guide live, but we record where
every published number came from. Please send **one** of the following:

- your technical measurement sheet or spec sheet for this style, or
- the production tech pack, or
- a signed or emailed confirmation of the table above, or
- photographs of a physical sample being measured, with the tape readable.

Whatever you send is filed against the product so that anyone can later answer
"where did these measurements come from" without guessing.

---

## 8. What happens when this comes back

1. The numbers go into one `hivolt_size_chart` record in the exact unit and on
   the exact basis you used.
2. It is attached to this one product.
3. The size guide starts rendering on the product page — a table with a
   centimetre/inch toggle, and the basis stated on it.
4. Nothing is published to customers until that has been reviewed.

Until then the product page shows no size guide at all, which is the intended
behaviour. It will not show a generic polo chart, and it will not show
measurements derived from a body weight.

---

## Appendix — the other two draft polos

Recorded here so that the same question is not asked twice.

| Product | Supplier sizing data on file | Usable? |
|---|---|---|
| **Classic Cotton Polo** (this document) | Recommended body weight per size only | No — no garment dimension exists |
| **Slim-Fit Cotton Polo** (`9603122659560`) | Size labels M/L/XL/XXL, explicitly no measurements | No |
| **Anti-Wrinkle Polo** (`9603123216616`) | One numeric column, labelled "Length", 92–116 cm across S–4XL | **No — see below** |

The Anti-Wrinkle Polo's column is the only numeric garment data anywhere in the
catalogue, and it is internally consistent: every stated inch value matches its
centimetre value to two decimal places. It is still unusable, because the label
and the values disagree.

- It is labelled **Length**, but grades at a constant **4 cm per size**. Body
  length on a men's polo typically grades at about 2 cm per size; 4 cm is the
  step used for chest circumference.
- The range **92–116 cm** sits outside the normal body-length range for a men's
  polo (roughly 68–80 cm) and inside the normal chest-circumference range.
- The supplier states no measurement basis.

Publishing a column headed "Length" that is probably a chest circumference
would put a wrong number in front of a customer, which is worse than showing
nothing. **The same clarification is needed for that product**: what was
measured, and on what basis.
