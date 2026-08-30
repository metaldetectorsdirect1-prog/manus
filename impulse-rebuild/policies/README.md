# policies/ — corrected policy bodies, BLOCKED on scope

**Reconstructed 2026-08-27.** The corrected bodies this README describes were
never committed (only this README survived); the live policies still carried
every flagged claim. The four `.html` files now present were rebuilt from the
live policy read-back + every documented correction below, **plus the Option A
changes**: Terms §1 now says women's clothing (activewear and the spec-first
publishing promises removed); shipping/delivery windows are now
**supplier-stated facts** from the live catalog — 2–6 business days
(US-warehouse items: Walmart 1–2d, Amazon 2–6d) and 10–15 business days
(international: AliExpress ~13d, private supplier 11–14d); unsourced
operational claims (PO Boxes, carriers, 24h tracking, 12h windows,
"production") stay deleted. Privacy remains untouched (Shopify template).
Paste procedure unchanged (below). **These same bodies are the source for the
GMC shipping/returns settings — mirror word-for-word.**

**These are not applied.** `shopPolicyUpdate` is denied to this connector:

```
Access denied for shopPolicyUpdate field.
Required access: `write_legal_policies` access scope.
```

All four writes were attempted in one request and all four were denied. Not
retried, not worked around.

## Smallest human action

Shopify admin → **Settings → Policies**. Four policies, paste each file's contents
into the matching editor, replacing the whole body:

| File | Policy |
|---|---|
| `contact.html` | Contact information |
| `refund.html` | Refund policy |
| `shipping.html` | Shipping policy |
| `terms.html` | Terms of service |

**Privacy policy is deliberately untouched.** It is Shopify's default Liquid
template, carries no HIVOLT-authored claim, and contains no entity misstatement —
`{{ shop_name }}` renders the trade name, which is correct.

## Already applied without needing this scope

The shipping **rate name** carried the same banned figure and rendered at
checkout: `FREE Tracked Shipping (8–14 business days)` → now `FREE Tracked
Shipping`. Verified by read-back; price `$0.00 USD` and active state unchanged.

## What changed and why — every edit

### Entity (§2.1)
`HIVOLT is a single member limited liability company registered in Illinois` and
the registered name `HIVOLT` → **`Dn Global Trading LLC (trading as HIVOLT)`**.
The legal-form assertion is **deleted, not adjusted**, per instruction. Address
unchanged: 10s225 Kaye Ln, Willowbrook, IL 60527.

Occurrences corrected: Terms §1, Terms §15, Contact, Refund, Shipping.

### Refund figure (§2.2)
`5-7 business days` → **`5 business days`** (owner-confirmed), plus the confirmed
bank-settlement clause: *"Depending on your bank, it can take a further 5-10 days
to appear on your statement."* Now agrees with `/pages/returns-refunds`.

Also: `We reply within one business day with a prepaid return label` → **`Once
your return is approved we send a prepaid return label within 2 business days`**
— the owner-confirmed value, replacing an unsourced one.

### Deleted, no replacement written (§2.3, §2.4)

| Deleted | Where | Why |
|---|---|---|
| `dispatched within 2-4 business days` | Shipping, Terms §5, Contact | ruled out for reuse |
| `8-14 business days after dispatch` | Shipping, Terms §5, Contact | ruled out for reuse |
| entire "Why the Window Is Not Two Days" section | Shipping | explains a window that no longer exists |
| `not arrived within 14 business days … replace the order or refund it in full` | Shipping | unsourced |
| `ship via USPS or UPS depending on your address` | Shipping | no carrier confirmed |
| `tracking link … within 24 hours`; `24-48 hours for the first carrier scan` | Shipping | unsourced |
| `we do not ship to PO Boxes`; `APO and FPO … longer than the windows below` | Shipping | unsourced; second clause referenced deleted windows |
| entire "Wrong Address" section (`within 12 hours`, `before … production`) | Shipping | unsourced |
| entire "Order Cancellations" section (`within 12 hours`, `enter production`) | Refund | unsourced; "production" describes manufacturing that does not happen |
| `within 30 days of delivery with photographs` | Refund | unsourced condition on a statutory remedy |
| `so you are not waiting on an inbound parcel before your replacement ships` | Refund | operational commitment |
| `Response Time: Within one business day` + hours + timezone | Contact | unsourced |
| `Orders are dispatched from Illinois` | Contact, Shipping | no fulfilment origin confirmed |
| `a person will answer` | Contact | unsourced operational claim |
| `see the confirmation email sent when your order was dispatched` | Contact | process step, zero orders ever placed |
| `We publish the fibre composition and fabric weight in g/m² for each style, taken from the supplier specification sheet` | Terms §1 | **§2.4** — promises data for a catalog of zero products |
| `We source manufacturer garments, specify them and sell them under our own name` | Terms §1 | sourcing model unconfirmed, no supplier selected |
| `Sizing follows the size guide published on each product page` | Terms §8 | there are no product pages; both size guides are unpublished |
| `including its fabric specification` | Terms §8 | same class as §2.4 |

Where a section was nothing but the deleted figure, the section is gone. No
replacement number was written anywhere.

### The one gap that is named rather than left silent

Shipping policy now carries, in place of the deleted windows:

> **Dispatch and Delivery** — We are not currently publishing dispatch or delivery
> windows. We would rather leave this blank than publish a window we cannot stand
> behind.

That is the §1.6 house standard, test 2 (*gaps are named, not filled*) and test 4
(*the provenance statement is published on the page*). It creates no obligation
and states no number.

### Kept, and why it is sourced

| Kept | Source |
|---|---|
| `Free on every order… no minimum… shown as $0.00` | **CONFIG** — verified live: General profile, US zone, one method, `DeliveryRateDefinition` price `0.0 USD` |
| `ships within the United States only` | **CONFIG** — market `International` is `enabled: false` |
| `60 days from delivery… free return shipping… no restocking fee` | **OWNER** |
| `Sale items are included` | OWNER-implied — 60 days "any reason", no exclusion ever supplied |
| `unworn, tags attached` | OWNER-implied + STANDARD |
| faulty goods remedy in addition to the 60 days | STANDARD (statutory) |
| `prices in US dollars`; `sales tax at checkout`; `no customs, all orders domestic` | CONFIG |
| Payment via Shopify Payments; no subscriptions; Illinois / DuPage County | CONFIG + pre-existing |
| Category → `women's and men's apparel` | **OWNER** (brand block) — replaced `technical activewear and gym apparel` |
