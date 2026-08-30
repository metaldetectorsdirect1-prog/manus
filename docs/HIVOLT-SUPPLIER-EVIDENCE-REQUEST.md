# Supplier evidence request — ready to send

**Status: PREPARED — NOT SENT. Send access unavailable from the automation
environment.**

> ## Owner action: copy one of the two messages below into the supplier chat.
>
> Nothing needs rewriting or reconstructing. Both versions are complete and
> sized for a chat window. Send the Chinese one if the seller replies in
> Chinese, the English one otherwise — or both, which costs nothing.

| | |
|---|---|
| Supplier item | **`1005002281827487`** |
| Listing on file | `https://www.aliexpress.com/item/1005002281827487.html` |
| Our product | HIVOLT Classic Cotton Polo — Men's Short Sleeve |
| Shopify GID | `gid://shopify/Product/9603121774824` (status `DRAFT`) |
| Supplier colour codes on file | `PL208` (Navy, White, Light Blue, Dark Grey), `PL205` (Black), `AX-511` (Army Green) |
| Blockers this unblocks | Garment measurements / size chart **and** fibre composition |

The detailed specification behind this request is
`docs/HIVOLT-POLO-MEASUREMENT-REQUEST.md`. This file is the message; that file
is the reasoning.

## Why this could not be sent automatically

Checked this session, in order:

| Surface | Result |
|---|---|
| AliExpress web / message hosts | **403 at CONNECT.** The proxy logged `gateway answered 403 to CONNECT (policy denial)` for `www.aliexpress.com:443`, `msg.aliexpress.com:443`, `message.aliexpress.com:443` |
| AutoDS integration | 11 tools, all product/store operations — upload, list, search, publish, bulk actions. **No messaging or supplier-contact tool exists** |
| Local mail transport | none installed; no supplier email address on file, and guessing one is not acceptable |
| Other connected `contact_*` tools | Supermetrics support, Windsor.ai support — **unrelated third parties**, not this supplier |
| Browser automation | Playwright is installed, but has nowhere to reach: it would hit the same 403 |

The 403 is an organizational network-policy denial. It was reported, not
worked around — no proxy, mirror, tunnel or third-party relay was used, and no
credentials were touched.

---

## Message — English

```
Hello,

We are preparing this polo for retail sale in the United States and need the
factory specifications for item 1005002281827487.

Please confirm first: everything below should be for THIS item only
(1005002281827487), not a similar polo from your catalogue.

1. SIZE MEASUREMENT TABLE

Please measure the garment laid flat, and send measurements in CENTIMETRES for
each size we sell:

  EUR S 60-70kg
  EUR M 70-80kg
  EUR L 80-90kg
  EUR XL 90-100kg
  EUR XXL 100-105kg

For each size, if your factory specifies them:
  - Chest width (flat, armhole seam to armhole seam) — please say whether this
    is the flat half-width or the full circumference
  - Shoulder width (seam to seam)
  - Body length (highest point of shoulder to bottom hem)
  - Sleeve length (shoulder seam to sleeve opening)

Please send only the measurements your factory actually works to. Leave
anything else blank — we would rather have a gap than an estimate.

Also please tell us:
  - Are these GARMENT measurements or BODY measurements?
  - What production tolerance do you work to (± cm)?
  - If you have a measurement diagram or spec sheet, please send it.

2. WHAT THE SIZE NAMES MEAN

Our sizes are labelled like "EUR S 60-70kg". Please tell us:
  - Is 60-70kg the recommended body weight of the wearer?
  - What does "EUR" mean here — a European sizing standard, or your own
    internal product code?
  - Is the same garment also sold as S/M/L/XL/XXL, or under any US or EU
    numeric size?
  - What size label is physically sewn into the garment?

3. FABRIC LABEL PHOTOS

Please send clear photos, with the text readable, of:
  - the sewn-in fibre composition label (the one with the percentages)
  - the care label

Our listing currently says 100% Cotton, taken from your listing's Material
field. To sell in the US we have to verify that against the actual label, so we
need a photograph — a "yes, it is cotton" reply is not enough on its own.

Two more questions:
  - Is the fibre content the same for all six colours? Black (PL205) and Army
    Green (AX-511) have different codes from the other four (PL208).
  - What country of manufacture is printed on the label?

4. FACTORY DOCUMENTS (if you have them)

  - specification sheet or tech pack for this style
  - material or composition test certificate
  - production sheet

Thank you. We cannot list this product for sale until we have the measurements
and the label photo, so anything you can send helps.
```

---

## Message — Simplified Chinese / 简体中文

```
您好，

我们正在准备将这款 POLO 衫在美国零售销售，需要商品编号 1005002281827487 的
工厂规格资料。

请先确认：以下所有资料都必须是【这一款商品 1005002281827487】的，而不是贵司
目录中其他相似款式的 POLO 衫。

一、尺寸测量表

请将衣服平铺测量，并以【厘米 cm】提供我们在售的每个尺码的数据：

  EUR S 60-70kg
  EUR M 70-80kg
  EUR L 80-90kg
  EUR XL 90-100kg
  EUR XXL 100-105kg

每个尺码，如果贵厂确实按这些规格生产：
  - 胸围（平铺，腋下缝到腋下缝）——请说明这是【平铺半胸宽】还是【整圈胸围】
  - 肩宽（肩缝到肩缝）
  - 衣长（肩部最高点到下摆）
  - 袖长（肩缝到袖口）

请只提供贵厂实际生产时使用的数据。没有的项目请留空——我们宁可留空，也不要
估算的数字。

另请告知：
  - 这些是【成衣尺寸】还是【人体尺寸】？
  - 生产公差是多少（± cm）？
  - 如果有测量示意图或规格表，请一并发送。

二、尺码名称的含义

我们的尺码标注为 "EUR S 60-70kg"。请说明：
  - 60-70kg 是否指建议穿着者的体重？
  - 这里的 "EUR" 是什么意思——欧洲尺码标准，还是贵司内部的货号？
  - 同一件衣服是否也按 S/M/L/XL/XXL，或美码、欧码数字尺码销售？
  - 衣服上实际缝制的尺码标签写的是什么？

三、面料标签照片

请提供文字清晰可辨认的照片：
  - 缝在衣服内的【成分标】（标注面料成分百分比的标签）
  - 【洗水标】（洗涤说明标签）

我们的商品页目前写的是 100% 棉，这个信息来自贵司listing的"材质"栏。要在美国
销售，我们必须用实际标签核实，因此需要照片——仅回复"是纯棉的"不足以作为依据。

另有两个问题：
  - 六个颜色的面料成分是否完全相同？黑色（PL205）和军绿色（AX-511）与其余
    四色（PL208）的货号不同。
  - 标签上印的产地是哪里？

四、工厂文件（如有）

  - 该款式的规格表或技术资料包（tech pack）
  - 面料或成分检测证书
  - 生产单

谢谢。在拿到尺寸数据和标签照片之前，我们无法上架销售这款商品，所以您能提供
的任何一项都对我们有帮助。
```

---

## Evidence acceptance gate

Defined **now**, before any reply arrives, so the standard cannot drift to fit
whatever turns up.

### Measurements — ACCEPT only if all six hold

1. The reply states the data is for item `1005002281827487`, or is
   unambiguously attached to that item's chat thread.
2. Every row maps to one of our five Size values. A partial table is acceptable
   — three mapped sizes beat five invented ones — but an unmappable row is not.
3. Units are stated (cm or inch). An unlabelled number is not a measurement.
4. Every column's meaning is unambiguous, including whether chest is flat
   half-width or full circumference.
5. Garment-flat vs body basis is known.
6. The numbers are internally coherent: monotonic across sizes, plausible for a
   men's polo, and consistent with each other.

### Measurements — REJECT on any of these

- Body weight only, in any form. **This is what we already have.**
- A table from a different product, including a near-identical style.
- Column labels that contradict their own values — the trap the Anti-Wrinkle
  Polo's "Length" column set: labelled length, grading at 4 cm/size across
  92–116 cm, which is chest-circumference behaviour.
- Basis undeterminable after one clarifying question.
- Internally contradictory values.

A rejected reply is not a failure of the process. It is the process working,
and it is recorded with the reason.

### Fibre composition — evidence classes

| Class | Evidence | Effect |
|---|---|---|
| **A** | Clear photo of the sewn-in composition label, text readable · factory tech pack · production or material specification naming this style · composition test certificate | **Upgrade `spec.composition` to Class A.** Clears the Gate 2 publication blocker |
| **B** | Written supplier technical statement explicitly tied to item `1005002281827487`, without a photograph or document | Stays Class B. **Does not clear the blocker.** Recorded as corroboration |
| **C** | The listing's `Material` dropdown · a chat reply saying "yes, 100% cotton" · another product's label · inference from how the fabric looks in a photo | No effect. **This is exactly what we hold today** |

**`100% Cotton` is not upgraded to Class A without Class A evidence.** A
confident supplier reply is Class B no matter how confident it sounds.

If the label **contradicts** `100% Cotton` — say it reads 95% cotton / 5%
elastane — the label wins, `spec.composition` is corrected to match it, and the
correction is recorded in
`docs/HIVOLT-PRODUCT-DATA-PROVENANCE.md` with the photo as the source.

---

## What runs when valid evidence arrives

Not now. This session sends a request; it changes no product data. The
sequence below runs only against a reply that clears the gate above.

1. **Classify** every value against the gate. Class C stops here.
2. **Transcribe verbatim** — the supplier's numbers, the supplier's unit, the
   supplier's basis. No conversion, no rounding, no "tidying".
3. **Validate** units and semantics; ask one clarifying question if a column is
   ambiguous. Two unresolved ambiguities means REJECT, not a guess.
4. **Record provenance** in `docs/HIVOLT-PRODUCT-DATA-PROVENANCE.md`: what
   arrived, from whom, when, in what form, and its class.
5. **Create one `hivolt_size_chart` metaobject** — one, for this product.
6. **Attach** it to `spec.size_chart` on `9603121774824`.
7. **Independent read-back** — fresh query, not the mutation payload. Confirm
   the value, confirm `updatedAt` moved, confirm the 20-variant matrix is
   untouched. `userErrors: []` proves nothing.
8. **Real-product QA** — `python3 site/check-hivolt-real-product.py`, extended
   with assertions for the now-rendering size guide.
9. **Composition upgrade, only if Class A evidence arrived.** Otherwise
   `spec.composition` stays exactly as it is, at Class B.
10. **Update the publication gate** — close what actually closed, and only that.

Steps 5–9 are Shopify mutations and are out of scope until the evidence exists.

---

## Response log

Fill in when a reply arrives. Empty means no reply yet.

| Date | Channel | What arrived | Class | Accepted? | Notes |
|---|---|---|---|---|---|
| | | | | | |
