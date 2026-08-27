#!/usr/bin/env python3
"""Product Listing SOP validator — Google Merchant Center compliance.

Adjudicates a product (JSON) against the course Product Listing SOP before it
is published. Exit 1 = refusal; do not work around it. No network access —
fetch with the connector, adjudicate here (same model as
check-hivolt-theme-target.py).

Input product JSON shape (subset of Shopify product):
  {"title": str, "body_html": str, "handle": str, "vendor": str,
   "product_type": str, "tags": [str] | str,
   "variants": [{"price": "37.95", "compare_at_price": "59.95"|null, ...}],
   "images": [{"src": str, "alt": str|null}], "currency": "USD"}

Usage:
  python3 site/check-product-listing.py --product product.json [--report]
  python3 site/check-product-listing.py --self-test
"""
import argparse, json, re, sys, unicodedata

PSY95 = {"EUR", "USD", "GBP", "CAD", "CHF", "NZD"}   # prices end .95
ROUND05 = {"DKK", "PLN"}                              # prices end 0 or 5

PROMO_TITLE = re.compile(
    r"free\s+shipping|%\s*off|\b\d+\s*%|buy\s*\d+\s*get|\bsale\b|best\s*seller|"
    r"discount|clearance|hot\s*deal|limited", re.I)
CTA = re.compile(r"click\s+here|buy\s+now|order\s+now|shop\s+now|add\s+to\s+cart\s+now", re.I)
URGENCY = re.compile(
    r"limited\s+stock|flash\s+sale|last\s+pieces?|only\s+\d+\s+left|selling\s+fast|"
    r"while\s+(stocks?|supplies)\s+last|hurry", re.I)
MEDICAL = re.compile(
    r"cures?|heals?|therapeutic|orthopedic|orthopaedic|anti[- ]?bacterial|"
    r"medical[- ]grade|fda[- ]approved|clinically\s+proven", re.I)
SUPPLIER_VENDORS = re.compile(r"aliexpress|cj\s*drop|cjdropshipping|alibaba|temu|1688|taobao", re.I)

def _has_emoji_or_symbols(text):
    for ch in text:
        if ch in "™®★☆✓✔✖❌❤":  # ™ ® ★ ☆ ✓ ✔ ✖ ❌ ❤
            return ch
        cat = unicodedata.category(ch)
        if cat == "So" or (0x1F000 <= ord(ch) <= 0x1FAFF):
            return ch
    return None

def _slug(title):
    s = unicodedata.normalize("NFKD", title.lower())
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s

def check(product):
    errs, warns = [], []
    title = product.get("title") or ""
    body = product.get("body_html") or ""
    handle = product.get("handle") or ""
    vendor = product.get("vendor") or ""
    currency = (product.get("currency") or "USD").upper()

    # 2. Titles
    if not title:
        errs.append("TITLE: missing")
    if len(title) > 150:
        errs.append(f"TITLE: {len(title)} chars > 150 max")
    if title.isupper() and len(title) > 3:
        errs.append("TITLE: ALL CAPS")
    words = [w for w in re.findall(r"[A-Za-z]{4,}", title)]
    caps_words = [w for w in words if w.isupper()]
    if caps_words:
        errs.append(f"TITLE: all-caps word(s) {caps_words}")
    if PROMO_TITLE.search(title):
        errs.append(f"TITLE: promotional language: {PROMO_TITLE.search(title).group(0)!r}")
    bad = _has_emoji_or_symbols(title)
    if bad:
        errs.append(f"TITLE: symbol/emoji {bad!r}")

    # 3. Descriptions
    if re.search(r"<img\b", body, re.I):
        errs.append("DESC: <img> inside description (suspension trigger)")
    for m in re.finditer(r'href="([^"]+)"', body, re.I):
        url = m.group(1)
        if url.startswith("http") and "{{shop" not in url:
            errs.append(f"DESC: external link {url[:60]}")
    if CTA.search(body):
        errs.append(f"DESC: call-to-action: {CTA.search(body).group(0)!r}")
    if URGENCY.search(body):
        errs.append(f"DESC: urgency language: {URGENCY.search(body).group(0)!r}")
    if MEDICAL.search(body):
        errs.append(f"DESC: medical/health claim: {MEDICAL.search(body).group(0)!r}")
    if "✓" in body or "✔" in body:
        errs.append("DESC: checkmark characters — use bullet points")

    # 4. Pricing
    for i, v in enumerate(product.get("variants") or []):
        try:
            price = float(v.get("price"))
        except (TypeError, ValueError):
            errs.append(f"VARIANT {i}: unparseable price {v.get('price')!r}")
            continue
        cents = round(price * 100) % 100
        if currency in PSY95 and cents != 95:
            errs.append(f"VARIANT {i}: {price} {currency} — must end .95")
        if currency in ROUND05 and round(price) % 5 != 0:
            errs.append(f"VARIANT {i}: {price} {currency} — round to 0 or 5")
        cap = v.get("compare_at_price")
        if cap:
            try:
                cap = float(cap)
                if cap > 0 and price < cap:
                    disc = (cap - price) / cap * 100
                    if disc > 50.0:
                        errs.append(f"VARIANT {i}: discount {disc:.0f}% > 50% max")
            except (TypeError, ValueError):
                errs.append(f"VARIANT {i}: unparseable compare_at_price")

    # 5. Organization
    if not vendor:
        errs.append("VENDOR: missing — set to the store name")
    if SUPPLIER_VENDORS.search(vendor):
        errs.append(f"VENDOR: supplier name {vendor!r} — a named suspension trigger")
    if not product.get("product_type") and not product.get("tags"):
        errs.append("CATEGORY: no product_type and no tags — assign at least one category")
    if re.search(r"-\d{2,}$", handle):
        errs.append(f"HANDLE: trailing number {handle!r} — base URL on the title")
    if title and handle:
        tslug = _slug(title)
        if handle not in (tslug, tslug[:len(handle)]) and _slug(handle) not in tslug:
            # top automatic trigger: retitled product, stale handle
            errs.append(f"HANDLE: {handle!r} does not match title slug {tslug!r}")

    # 1. Images (what is checkable without fetching pixels)
    imgs = product.get("images") or []
    if not imgs:
        errs.append("IMAGES: none")
    for i, im in enumerate(imgs):
        src = (im.get("src") or "").lower()
        if re.search(r"alicdn|aliexpress|cjdropshipping", src):
            errs.append(f"IMAGE {i}: supplier CDN url")
        if not (im.get("alt") or "").strip():
            warns.append(f"IMAGE {i}: missing alt text")
    return errs, warns

def self_test():
    good = {"title": "Elena relaxed merino wool turtleneck sweater",
            "body_html": "<p>Merino wool knit.</p><ul><li>Ribbed cuffs</li></ul>",
            "handle": "elena-relaxed-merino-wool-turtleneck-sweater",
            "vendor": "HIVOLT", "product_type": "Knitwear", "tags": ["womens", "knitwear"],
            "variants": [{"price": "44.95", "compare_at_price": "59.95"}],
            "images": [{"src": "https://cdn.shopify.com/x.jpg", "alt": "sweater"}],
            "currency": "USD"}
    e, w = check(good)
    assert e == [], f"clean product failed: {e}"

    cases = [
        (dict(good, title="FREE SHIPPING Floral Dress ★ 50% OFF"), "TITLE"),
        (dict(good, title="x" * 151), "150"),
        (dict(good, body_html='<img src="x.jpg"><p>Hurry, limited stock! Click here</p>'), "DESC"),
        (dict(good, body_html="<p>✓ soft ✓ warm</p>"), "checkmark"),
        (dict(good, variants=[{"price": "44.99", "compare_at_price": None}]), ".95"),
        (dict(good, variants=[{"price": "24.95", "compare_at_price": "99.95"}]), "50%"),
        (dict(good, vendor="AliExpress"), "VENDOR"),
        (dict(good, handle="dress-231", title="Floral Summer Dress"), "HANDLE"),
        (dict(good, images=[{"src": "https://ae01.alicdn.com/x.jpg", "alt": "a"}]), "IMAGE"),
        (dict(good, currency="DKK", variants=[{"price": "251", "compare_at_price": None}]), "round"),
        (dict(good, body_html="<p>Orthopedic support, clinically proven.</p>"), "medical"),
    ]
    for prod, must in cases:
        e, _ = check(prod)
        assert any(must.lower() in x.lower() for x in e), f"expected {must!r} violation, got {e}"
    print(f"self-test: {1 + len(cases)}/{1 + len(cases)} passed")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--product")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()
    if a.self_test:
        self_test(); return 0
    if not a.product:
        ap.error("--product or --self-test required")
    p = json.load(open(a.product))
    errs, warns = check(p)
    if a.report or errs or warns:
        for e in errs: print(f"REFUSE  {e}")
        for w in warns: print(f"warn    {w}")
    if not errs:
        print("PASS — SOP compliant" + (f" ({len(warns)} warning(s))" if warns else ""))
    return 1 if errs else 0

if __name__ == "__main__":
    sys.exit(main())
