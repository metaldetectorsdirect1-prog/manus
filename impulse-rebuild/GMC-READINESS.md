# GMC-READINESS.md

Google Merchant Center readiness audit for HIVOLT, run against the `topgoogle`
playbook's Checklist A (approval) and Checklist B (compliance), 2026-08-26.

Verified against live Shopify state. Items I cannot see from here are marked
**owner-side** rather than guessed.

---

## Phase diagnosis

The playbook's first rule is that almost every failure is a step done **in the
wrong order**. So, precisely where HIVOLT sits:

| | |
|---|---|
| Store built | ✅ live since 2026-08-25T01:37Z |
| GMC exists | ✅ `merchant_id 5838274874`, on file in `mm_google_shopping_extension` |
| GMC status | **owner-side — I cannot query Merchant Center** |
| Products in feed | **0** |
| Misrep campaign | not run |

**HIVOLT is at Phase 0/1, not Phase 5.** The store is built and live, the GMC
exists, and the feed is empty.

### 🔴 The sequencing trap, stated before anything else

The playbook is explicit that the misrepresentation suspension is **coming
regardless**, and that the goal is to trigger it *now* — while the store is
"five clean products in one niche, the easiest possible state to appeal from."

**HIVOLT has zero products, so it cannot yet run that campaign.** The correct
order is:

1. Import **~5 clean products in one tight category** — not the full catalogue
2. Get them **green** in GMC (not "in review")
3. Run PMax at **€5/day** to provoke the misrep within 5–7 days
4. Appeal — **you get 3 appeals per GMC, then it is dead**
5. Only then: 4-week freeze, then import at 25/day

**Importing the full catalogue before step 4 is the documented way to lose the
GMC**, because you then have to appeal a suspension across hundreds of products
instead of five. Whatever the supplier decision turns out to be, the first
import must be small and narrow.

---

## Checklist A — approval

### Fixed this session

| Item | Was | Now |
|---|---|---|
| "Collections named specifically — never **All Products**" — an explicit checklist prohibition | collection titled literally **"All Products"** | **"Women's & Men's Apparel"** |
| Legal pages named exactly, incl. **Payment Policy** | **Payment Policy did not exist** | `/pages/payment-policy` created and published |
| Legal pages reachable | Terms pointed at the page, not the policy; no payment policy in nav | footer "About" column now carries Terms, Privacy, Refund, Shipping, Payment + privacy choices |
| Company↔store relationship in plain language | implied | *"HIVOLT is owned and operated by Dn Global Trading LLC"* — the checklist's exact phrasing |

### 🔴 Blocked at the tool layer — owner must do these

| # | Item | Why it is blocked |
|---|---|---|
| 1 | **Unpublish the 14 empty collections** | `publishableUnpublish` is refused by connector policy: *"Unpublishing is blocked to prevent accidental storefront catalog removal."* Not worked around. |
| 2 | **Paste the four corrected policy bodies** | `shopPolicyUpdate` needs `write_legal_policies`, denied. Bodies ready in `policies/`. |

### 🔴 The policy mismatch is now a GMC blocker, and I made one half of it worse

Checklist A ends with: *"Returns/shipping values in GMC match the on-site
policies **word for word**."*

They currently do not match each other, let alone GMC:

| Claim | Shop policy (`/policies/*`) | Page (`/pages/*`, fixed) |
|---|---|---|
| Refund timing | "5-7 business days" | **5 business days** |
| Dispatch window | "2-4 business days" | **no window published** |
| Delivery window | "8-14 business days" | **no window published** |
| Registered entity | "HIVOLT is a single member LLC" | **Dn Global Trading LLC** |

**Disclosure:** fixing the pages while being unable to fix the policies *widened*
the dispatch/delivery gap — the pages now correctly publish no window while the
policies still publish the ruled-out one. That was the right call for honesty and
the wrong shape for GMC, and it resolves the moment the policy bodies are pasted.
It is the single highest-value owner action on this page.

### 🟠 Cannot verify from here — owner-side

| Item | Note |
|---|---|
| Dead-link scan (deadlinkchecker.com) | storefront egress is 403 by network policy |
| PageSpeed > 70 | same |
| ScamAdviser 95–100 | same |
| Email deliverability check | same |
| Domain age / registrar | playbook wants `.com`, 3+ years, GoDaddy, **never Namecheap** |
| GMC current status | no Merchant Center connector |

### 🟠 Present but weak, or absent

| Item | State |
|---|---|
| **Warehouse address in the selling country** | **none.** No fulfilment partner selected. Checklist asks for business address *and* warehouse address |
| **Instagram, 25+ posts, linked in footer** | **absent.** All ten social settings are empty, `toolbar_social: false` |
| **Trustpilot, 10+ reviews** | **absent** |
| Callable local phone | present — **+1 914-650-2041**. Area code 914 is **New York**; the registered address is **Illinois**. Not fatal, but it is the kind of mismatch a manual reviewer notices |
| Search-traffic campaign already running | owner-side |

---

## Checklist B — compliance. This is where HIVOLT is unusually strong

Everything the prior sessions removed maps directly onto Google's prohibited list.

| Prohibited | HIVOLT |
|---|---|
| **Fake reviews** | ✅ **zero.** Five fabricated testimonials came off the live storefront with the 2026-08-25 theme swap; no review app is installed, so none can exist |
| **Countdown timers** | ✅ `sections/countdown.liquid` exists but is referenced by no template |
| **Falsifiable stock counters** | ✅ `inventory_enable: false` in theme settings |
| **AliExpress/CJ named as vendor** | ✅ `vendor_enable: false` |
| **Permanent "clearance"/"everything must go"** | ✅ none. The "extra 10% off — limited time" banner came off with the theme swap |
| **Images inside product descriptions** | n/a — zero products. **Enforce at import** |
| **URL handle not matching retitled product** | n/a — *"a top automatic trigger"*. **Enforce at import** |
| **Max discount 50%** | ✅ the only automatic discount is 15% |
| **Empty collections** | 🔴 **14 live.** The one unfixed prohibition — see blocked item 1 |

**Discounts audited.** Four are active: 10% welcome, 10% abandoned-cart, 20%
launch, and the automatic 15% two-or-more. All well under the 50% ceiling. Two
overlapping *first-order* codes (10% and 20%) are both live with no end date —
worth a tidy, not a compliance issue.

---

## 🟠 Feed apps: two are installed, and the playbook wants one

- **Simprosys** — present (`mm-google-shopping` product metafields, `mm_google_shopping_extension` shop metafields). This is the app the playbook explicitly recommends.
- **"Google & YouTube" sales channel** — also present as a publication.

The playbook says to sync the feed with **Simprosys, not the Google & YouTube
app**. Both being installed risks two systems submitting the same products to one
Merchant Center. **Confirm which one actually owns the feed before importing
anything**, and disable the other.

---

## Owner action list, in order

1. **Paste the four policy bodies** from `policies/` into Settings → Policies. Closes the word-for-word mismatch.
2. **Unpublish the 14 empty collections** — each collection → Sales channels → uncheck Online Store. Republish as they populate.
3. **Decide the feed owner** — Simprosys or Google & YouTube, not both.
4. **Check GMC status** for `5838274874`, and how many of the 3 appeals remain.
5. Add a **warehouse address**, once a fulfilment partner exists.
6. Stand up **Instagram (25+ posts)** and **Trustpilot (10+ reviews)**, link both in the footer.
7. Run the external scans — dead links, PageSpeed, ScamAdviser, email deliverability.
8. **Then** import ~5 clean products in one category and trigger the misrep campaign deliberately.

---

## Honesty note on the source material

The playbook records one practitioner team's method. Parts of it sit in grey
areas — anti-detect browsers and proxies for Gmail creation, purchased followers,
purchased reviews, paid insider approvals. Those are recorded in the source as
part of the method; they are **not** applied here and not recommended. Purchased
or fabricated reviews in particular are the exact defect class this rebuild has
spent six sessions removing, and they carry both account-loss and
consumer-protection risk. The compliant path is the one above.
