# Amazon is open after all — but only as "Generic", and that is a brand decision

2026-08-13.

## What I got wrong, or at least stopped short of

`audit/MARKETPLACE-2026-08-12.md` ruled Amazon out like this:

> Amazon apparel categories require a **GTIN** (UPC/EAN) per variant, and **541
> of 541 variants here carry a null barcode**. Listing on Amazon therefore
> needs either purchased GTINs or an approved GTIN exemption, both of which
> take days to weeks.

The barcode fact is right and still verified. The conclusion was lazy. I
mentioned the exemption in passing and then treated Amazon as closed without
checking whether HIVOLT qualifies. Amazon is the largest audience available —
2.6bn monthly visits — so that was the wrong thing to leave unexamined.

## The exemption exists, and this catalogue qualifies

Amazon grants GTIN exemptions for **private-label products, products you brand
or manufacture that have no barcode, and generic unbranded products**. HIVOLT
sources manufacturer blanks and sells them under its own name, which is
squarely private label.

The mechanics are far lighter than "days to weeks":

* apply during listing creation — tick *"I don't have a Product ID"* — or as a
  standalone application beforehand
* upload **2–9 real product photos**, all sides, no mockups, no visible barcode
* **approval within 48 hours**

The photo requirement is already met. HIVOLT publishes the supplier's studio
images of the exact garments — real photographs, not renders. (The fabricated
AI images were removed on 08-10, which is what makes this true.)

## The catch, and it is not small

Amazon requires **"product images or packaging photos proving your brand name
is present and non-removable"**, and the brand entered must exactly match what
is visible on the product.

**HIVOLT garments carry no logo.** The store says so itself, repeatedly and on
purpose — *"Manufacturer blanks, selected and specified by us — not made in a
HIVOLT factory… There is no logo printed on either piece."*

So there are two routes and they are not equivalent:

| route | possible? | what it costs |
|---|---|---|
| Apply as brand **HIVOLT** | **No.** The photos cannot prove a name that is not on the garment. Submitting anyway is claiming something false to Amazon, and the risk is not a rejected listing — it is a flagged seller account. | — |
| Apply as **Generic** | **Yes.** Amazon explicitly allows unbranded products; select *"This product does not have a brand name."* | Every listing reads **"By Generic"** under the title. No brand equity accrues, and repeat buyers have nothing to come back to. |
| Buy real **GS1 GTINs** | Yes, and lets the listings say HIVOLT | GS1 fees, and the name is still only a title field — Amazon **Brand Registry** needs a registered trademark, which HIVOLT does not have. |

## The decision, stated plainly because it is the owner's

Amazon can be open inside 48 hours, selling **as Generic**. That means the
garments compete as unbranded commodity apparel on photo and price, against
sellers doing exactly the same thing, with no brand being built.

That is not obviously wrong for this business. The store has **zero orders in
its entire history**, so there is currently no brand equity to protect. First
revenue and real reviews may be worth more than a name nobody has heard.

And the "published, not claimed" positioning survives better than expected:
fabric weight and fibre composition belong in Amazon's bullet points, which is
exactly where apparel shoppers look. What is lost is the *name* on the listing,
not the substance behind it.

But it is a genuine trade-off, it is strategic rather than technical, and it is
not mine to make. So it is written down rather than acted on.

## Not built yet, deliberately

I have not generated an Amazon flat file. The Generic-versus-GTIN decision
determines what goes in the brand column of every row, and building a file that
says "Generic" before the owner has chosen would be deciding it for them. Say
the word and it is the same generator as the eBay one with a different header
set.

## Order of operations, unchanged

eBay still goes first: **113 listings are complete and waiting**, GTIN is
"Does not apply", no exemption application, no brand question, no 48-hour wait.
Amazon is the bigger audience and the slower, more consequential door.
