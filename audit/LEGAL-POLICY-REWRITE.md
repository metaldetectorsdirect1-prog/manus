# HIVOLT — the legal policies describe a different business

Found 2026-08-07 while investigating why 24 checkout arrivals produced zero
completed orders.

**These cannot be fixed through the API.** `shopPolicyUpdate` requires the
`write_legal_policies` access scope, which this connector does not hold. The
replacement text is below; it has to be pasted in manually at
**Settings → Policies**.

> Retried 2026-08-09. Still `Access denied for shopPolicyUpdate field. Required
> access: write_legal_policies`. Nothing has changed; all four policies are
> still live in their original form.

**The text to paste now lives as four files in `audit/policies/`** — copy those,
not the code blocks below, which are kept for the diff they document. Three
corrections were made when the files were written:
>
> - **The mailing address was wrong in both directions.** The live Contact
>   policy says `Addison, IL 60101`; the draft below repeated it. The store's
>   billing address and its only fulfilment location are both
>   `10s225 Kaye Ln, Willowbrook, IL 60527`. The file says
>   **Willowbrook, IL 60527** — city and ZIP only, the same granularity the
>   live policy already publishes, so correcting it does not newly expose a
>   street address.
> - **The draft Terms kept the 5–8 day window** this very document flags as
>   wrong four paragraphs later. Every storefront surface says 8–14, including
>   two JSON-LD blocks, and 8–14 is the window the store deliberately chose to
>   quote. The file says **8–14 business days**.
> - **A shipping policy was missing.** The live one is the only policy not
>   describing a supplement business, which is why the first pass skipped it —
>   but its 5–8 day window contradicts all four storefront surfaces, so it
>   needs replacing too. `audit/policies/shipping-policy.html` is aligned to
>   the storefront: free, no minimum, continental US, 8–14 days, tracked from
>   dispatch, no expedited option.

---

## What is live right now

### Terms of Service

> **"HIVOLT sells dietary supplement products.** Our products are not intended
> to diagnose, treat, cure, or prevent any disease. Consult your healthcare
> provider before starting any supplement regimen."

> **"Subscriptions.** Subscription orders are billed automatically at the
> frequency you select."

> "We offer a **90-day** money-back guarantee on all purchases."

### Refund Policy

> "We stand behind the quality of **HIVOLT Collagen Peptides**."

> "Products must be returned in their **original packaging**."
> "**Opened containers** are eligible for refund under our 90-day guarantee."

> "**Subscription Cancellations.** You may cancel your subscription at any time."

### Contact Information

> "**Subscription changes:** Log into your account to pause, skip, or cancel."

---

## Why this matters more than it looks

The store sells activewear. It has no supplements, no subscriptions, and no
recurring billing of any kind.

1. **It reads as a hijacked storefront.** Shopify links the Refund Policy from
   the checkout page. A buyer about to enter a card clicks it and finds a
   supplement subscription policy on a leggings store. That is exactly what a
   scraped or resold store looks like, and it is the last thing they see before
   deciding. 24 sessions reached checkout in 40 days and none completed.

2. **"Subscription orders are billed automatically"** is the single most
   alarming sentence you can put in front of someone entering card details on a
   brand they have never bought from.

3. **The return window contradicts itself.** Product pages and the
   `60-day-love-it-guarantee` page both say 60 days. The binding legal document
   says 90. The legal document is what governs, and the two disagree.

4. **The Terms describe goods the store does not sell**, including a health
   disclaimer for products that do not exist.

5. **Google Merchant Center reviews the return policy.** A supplement
   subscription policy on an apparel feed is a review failure, on top of the
   `age_group`/`gender` gap already fixed.

The Shipping Policy is the only one not describing a supplement business — but
**it is not "fine", and an earlier version of this document wrongly said it
was.** Its transit window contradicts every storefront surface:

| Source | Claim |
|---|---|
| Shipping Policy | **5-8 business days** after 1-2 days processing |
| Homepage FAQ + its JSON-LD | **8-14 business days** |
| Shipping page + its JSON-LD | **8-14 business days** |

Both are emitted as structured data, so Google can surface either. Decide which
window the fulfilment partner actually hits, then make it identical in all four
places. Free US shipping with no minimum, and United States only, are
consistent everywhere and need no change.

---

## Replacement text

Paste each into **Settings → Policies**. Nothing below is newly invented: every
term is taken from the store's own already-published customer-facing pages
(`returns-refunds` and `60-day-love-it-guarantee`), so the legal document and
the storefront finally agree. Have someone qualified review before publishing —
this is an alignment pass, not legal drafting.

### Refund policy

```html
<h2>HIVOLT Return &amp; Refund Policy</h2>
<p><strong>60-Day Love-It Guarantee.</strong> You have 60 days from delivery to return any item, including items you have worn and washed.</p>

<h3>Return window</h3>
<p>60 days from the delivery date, on every order. Performance apparel cannot be judged in a fitting room, so wearing and washing an item does not void the return.</p>

<h3>How to start a return</h3>
<p>Email <a href="mailto:support@hivolt-usa.com">support@hivolt-usa.com</a> with your order number and the items you are returning. We reply with a prepaid return label within one business day. If you have an account, your order numbers are in your order history.</p>

<h3>Return shipping</h3>
<p>Free within the United States — we provide a prepaid label. HIVOLT ships within the United States only, so no other return destinations apply.</p>

<h3>Refund timing</h3>
<p>We process refunds within 2 business days of the return arriving at our warehouse. Your bank typically takes a further 3–5 business days to post it. Refunds are issued to the original payment method and cannot be redirected elsewhere.</p>

<h3>Exchanges</h3>
<p>Exchanges ship as soon as your return scans with the carrier, so you are not waiting on the refund cycle. Tell us the size or style you want when you email.</p>

<h3>Faulty items</h3>
<p>If a seam, zip or fabric fails under normal training use, we cover it at any point within the 60 days. Send a photo with your email and we will replace the item or refund you, your choice, with no return shipping required.</p>

<h3>Wrong or missing items</h3>
<p>Email us within 14 days of delivery with your order number and a photo. We ship the correct item immediately at our cost.</p>

<h3>What is excluded</h3>
<ul>
<li>Items marked Final Sale on the product page</li>
<li>Gift cards</li>
<li>Items damaged beyond normal wear — tears, burns, or staining not caused by the garment</li>
</ul>

<h3>Questions</h3>
<p><a href="mailto:support@hivolt-usa.com">support@hivolt-usa.com</a> — we reply within one business day.</p>

<p><em>Last updated: August 2026</em></p>
```

### Terms of service

```html
<h2>HIVOLT Terms of Service</h2>
<p><strong>Effective date: August 2026</strong></p>
<p>Welcome to HIVOLT. By accessing our website or purchasing our products, you agree to be bound by these Terms of Service. Please read them carefully.</p>

<h3>1. Products</h3>
<p>HIVOLT sells training and studio activewear for men and women. Each product page publishes the fibre composition and fabric weight supplied by the manufacturer. Colours may vary slightly between screens and between production runs.</p>

<h3>2. Orders and payment</h3>
<p>All orders are subject to acceptance and availability. We reserve the right to refuse or cancel any order. Prices are listed in US dollars and are subject to change without notice. Payment is processed securely through Shopify Payments. We do not store your card details.</p>

<h3>3. Shipping</h3>
<p>We ship within the United States only. Orders are typically processed within 1–2 business days and delivered within 5–8 business days. Standard shipping is free on every order. We are not responsible for delays caused by carriers.</p>

<h3>4. Returns and refunds</h3>
<p>Every order is covered by our 60-Day Love-It Guarantee, including items you have worn and washed. Full terms are in our Refund Policy.</p>

<h3>5. Intellectual property</h3>
<p>All content on this website, including text, images, logos and branding, is the property of HIVOLT and is protected by intellectual property laws. You may not reproduce, distribute or use our content without written permission.</p>

<h3>6. Limitation of liability</h3>
<p>HIVOLT shall not be liable for any indirect, incidental or consequential damages arising from the use of our products or website. Our total liability shall not exceed the amount you paid for the product in question.</p>

<h3>7. Governing law</h3>
<p>These terms are governed by the laws of the State of Illinois, United States. Any disputes shall be resolved in the courts of DuPage County, Illinois.</p>

<h3>8. Changes to these terms</h3>
<p>We reserve the right to update these terms at any time. Continued use of our website after changes constitutes acceptance of the new terms.</p>

<h3>9. Contact</h3>
<p>For questions about these Terms of Service, email <a href="mailto:support@hivolt-usa.com">support@hivolt-usa.com</a>.</p>

<p><em>Last updated: August 2026</em></p>
```

### Contact information

```html
<h2>Contact HIVOLT</h2>
<p>We're here to help with any questions about our products or orders.</p>

<h3>Email</h3>
<p><a href="mailto:support@hivolt-usa.com">support@hivolt-usa.com</a></p>

<h3>Response time</h3>
<p>We reply within one business day (Monday–Friday, 9 AM – 5 PM CST).</p>

<h3>Mailing address</h3>
<p>HIVOLT<br>Addison, IL 60101<br>United States</p>

<h3>Common questions</h3>
<ul>
<li><strong>Order status:</strong> your confirmation email carries a live status link, and signed-in customers can see every order under Track Your Order.</li>
<li><strong>Returns:</strong> email us with your order number and we send a prepaid label within one business day.</li>
<li><strong>Sizing:</strong> every product page carries the manufacturer's measured size table for that style.</li>
</ul>

<p><em>Last updated: August 2026</em></p>
```

---

## Decide this before pasting: which mailbox is real

The store currently advertises **two different support addresses**:

| Address | Where it appears |
|---|---|
| `support@hivolt-usa.com` | Returns & Refunds page, 60-Day Guarantee page — what customers are told to use |
| `metaldetectorsdirect1@gmail.com` | The current Contact, Refund and Terms policies |

The replacement text above uses `support@hivolt-usa.com`, because that is what
the customer-facing pages already instruct people to use and it is on the
brand's own domain. **If that mailbox does not exist or is not monitored, every
return request silently disappears.** Confirm it works, or swap the address
throughout before pasting.

---

## Three smaller inconsistencies found alongside

1. **The Returns & Refunds page offers Canada and international returns** —
   "Canada: free on orders over $150, otherwise $12 deducted" and
   "International: customer arranges return shipping". The store ships to the
   United States only, and both the shipping policy and the delivery profiles
   agree on that. Those two table rows describe a service that cannot be bought.

2. **The `learn` blog is linked in the footer and has zero articles.** The
   footer "About" menu points at `/blogs/learn`, which is empty. The other blog,
   `news` ("Training Journal"), holds 500 articles.

3. **Orphan pages from a previous build are still live**, reachable by direct
   URL and to search engines even though nothing links to them: `help` (empty
   duplicate of `faq`), `halal` ("Halal & Certifications"), `ingredients`
   ("Ingredients & Science"), `ambassador` ("The YUBBEX Parent Crew"),
   `share-photo`, `quality`, `press`, `reviews`. Several name a different brand
   entirely. Delete or redirect them.
