#!/usr/bin/env python3
"""Assemble the HIVOLT Shopify theme from the loose files in site/.

The templates are authored flat (one agent per file, no path collisions).
Shopify needs a specific directory layout and a settings_schema.json, or the
admin rejects the upload. This script maps one to the other, concatenates the
per-agent stylesheets into a single assets/hivolt.css, and writes a zip that
Online Store → Themes → Add theme → Upload zip will accept.

Run:  python3 site/build-theme.py
Out:  HIVOLT-theme.zip

DEPLOYING WITHOUT THE ZIP
─────────────────────────
Writes to the live theme are refused, so the route is: themeDuplicate (the
payload field is `newTheme`, not `theme`), push files into the copy, then a
human publishes it. Pushing the files does NOT need base64 pasted through the
API — that costs ~4/3 of the file size in the request for every deploy. Instead:

    stagedUploadsCreate(resource: FILE, httpMethod: POST)   -> signed target
    curl -F ... -F file=@<path> <target url>                -> HTTP 201
    themeFilesUpsert(body: {type: URL, value: <resourceUrl>})

themeFilesUpsert returns an EMPTY upsertedThemeFiles list with no userErrors
even when it worked, so success is confirmed by re-reading checksumMd5 on the
theme file and comparing it to md5sum of the local build. The checksums match
exactly — there is no normalisation step to allow for.

DO NOT UPLOAD THIS ZIP OVER A THEME THAT HAS APPS INSTALLED
────────────────────────────────────────────────────────────
locales/en.default.json is written below as a two-key stub. The live theme's
copy is ~9x larger because GemPages writes its own strings into it. Uploading
the zip wholesale would delete them. The zip is for a fresh theme; an existing
theme takes individual file pushes, and locales/ is left alone.
"""
import json, pathlib, re, shutil, sys, zipfile

ROOT = pathlib.Path(__file__).resolve().parent          # site/
OUT = ROOT.parent / 'build' / 'hivolt-theme'
ZIP = ROOT.parent / 'HIVOLT-theme.zip'

# flat authored file  ->  path inside the theme
MAP = {
    # Password protection and gift cards each need their OWN document.
    # Shopify renders templates/password.liquid inside layout/password.liquid,
    # and gift_card.liquid declares `layout none` and carries its own <html>.
    # Neither shipped, so enabling either feature fell back to Shopify's
    # generic pages — a first gift card would have looked like another brand.
    'theme/layout-password.liquid':    'layout/password.liquid',
    'theme/password.liquid':           'templates/password.liquid',
    'theme/gift-card.liquid':          'templates/gift_card.liquid',
    'index.liquid':                    'templates/index.liquid',
    'product.liquid':                  'templates/product.liquid',
    'theme/collection.liquid':         'templates/collection.liquid',
    'theme/cart.liquid':               'templates/cart.liquid',
    'theme/search.liquid':             'templates/search.liquid',
    'theme/404.liquid':                'templates/404.liquid',
    'theme/list-collections.liquid':   'templates/list-collections.liquid',
    'theme/blog.liquid':               'templates/blog.liquid',
    'theme/article.liquid':            'templates/article.liquid',
    'theme/page.liquid':               'templates/page.liquid',
    'theme/page.fabric.liquid':        'templates/page.fabric.liquid',
    'theme/page.about.liquid':         'templates/page.about.liquid',
    'theme/page.contact.liquid':       'templates/page.contact.liquid',
    'theme/page.shipping.liquid':      'templates/page.shipping.liquid',
    'theme/page.returns.liquid':       'templates/page.returns.liquid',
    # Suffixes carried by live pages that would otherwise fall back to the
    # generic page.liquid and lose their layout. Checked against the store:
    # faq / size-guide / track-order / drops / membership all resolve to a
    # real page with content.
    'theme/page.faq.liquid':           'templates/page.faq.liquid',
    'theme/page.size-guide.liquid':    'templates/page.size-guide.liquid',
    'theme/page.track-order.liquid':   'templates/page.track-order.liquid',
    'theme/page.drops.liquid':         'templates/page.drops.liquid',
    'theme/page.membership.liquid':    'templates/page.membership.liquid',
    # One-product landing page for the Voltcore set. Reads price, sizes, stock
    # and spec straight off the live product, so the saving arithmetic cannot
    # drift out of step with the component prices the way the hand-typed
    # "$10.98" in the product description did.
    'theme/page.voltcore.liquid':      'templates/page.voltcore.liquid',
    'theme/layout-theme.liquid':       'layout/theme.liquid',
    # Footer email capture, rendered by layout/theme.liquid on every page.
    # A snippet rather than a section because the layout is not sectioned and
    # {% render %} is the only include the shell can use.
    'theme/newsletter.liquid':         'snippets/newsletter.liquid',
}
# customers-<name>.liquid -> templates/customers/<name>.liquid
CUSTOMER_RE = re.compile(r'^customers-(.+)\.liquid$')

# every stylesheet, concatenated in this order into assets/hivolt.css
CSS_ORDER = ['theme-hivolt.css', 'theme/layout.css', 'theme/collection.css',
             'theme/cart.css', 'theme/blog.css', 'theme/account.css',
             'theme/pages.css', 'theme/fabric.css']

SETTINGS_SCHEMA = [
    {"name": "theme_info",
     "theme_name": "HIVOLT",
     "theme_version": "1.0.0",
     "theme_author": "HIVOLT",
     "theme_documentation_url": "https://hivolt-usa.com",
     # /pages/contact does not exist and 404s. The live page is contact-us.
     "theme_support_url": "https://hivolt-usa.com/pages/contact-us"},
    {"name": "Brand",
     "settings": [
         {"type": "image_picker", "id": "logo", "label": "Logo"},
         # layout/theme.liquid reads settings.favicon and settings.share_image,
         # but neither was declared here — so the {% if %} guarding each one
         # never fired. No favicon rendered at all, and og:image had no
         # store-wide fallback, which is what Facebook and Instagram show when
         # a page without its own image is shared. Most of this store's real
         # traffic arrives from exactly those two.
         {"type": "image_picker", "id": "favicon", "label": "Favicon",
          "info": "Square PNG. Rendered at 32x32."},
         {"type": "image_picker", "id": "share_image", "label": "Social share image",
          "info": "Fallback og:image for pages with no image of their own. 1200x630."},
         {"type": "text", "id": "support_email", "label": "Support email",
          "default": "support@hivolt-usa.com"},
     ]},
    # These four feed sameAs in the Organization JSON-LD, which is how Google
    # links a social profile to this website as one brand entity. sameAs was
    # previously a hardcoded empty array, so it asserted nothing.
    #
    # Only the Facebook page is filled in, because it is the only profile that
    # could be verified (page id 482588221614644, "Hivolt USA"). The rest are
    # left blank deliberately: each one is emitted only when it holds a value,
    # and claiming a profile that does not exist is worse than claiming none.
    # Search Console verification. Left blank on purpose: the token has to come
    # from the owner's own Search Console property, and a wrong or invented
    # value fails verification rather than doing nothing. The meta-tag token is
    # a different string from the HTML-file token already in the store.
    {"name": "Search engine verification",
     "settings": [
         {"type": "text", "id": "google_site_verification",
          "label": "Google Search Console token",
          "info": "Search Console > Add property > URL prefix > HTML tag. Paste "
                  "ONLY the content=\"...\" value, not the whole tag."},
         {"type": "text", "id": "bing_site_verification",
          "label": "Bing Webmaster Tools token",
          "info": "Optional. Bing Webmaster Tools > Add site > Meta tag. Paste "
                  "only the content value."},
     ]},
    {"name": "Social profiles",
     "settings": [
         {"type": "text", "id": "social_facebook", "label": "Facebook page URL",
          "default": "https://www.facebook.com/482588221614644",
          "info": "Full URL. Feeds sameAs in structured data."},
         {"type": "text", "id": "social_instagram", "label": "Instagram profile URL",
          "info": "e.g. https://www.instagram.com/yourhandle — leave blank if none."},
         {"type": "text", "id": "social_tiktok", "label": "TikTok profile URL",
          "info": "e.g. https://www.tiktok.com/@yourhandle — leave blank if none."},
         {"type": "text", "id": "social_youtube", "label": "YouTube channel URL",
          "info": "Leave blank if none."},
     ]},
    {"name": "Announcements",
     "settings": [
         {"type": "checkbox", "id": "show_ticker", "label": "Show announcement ticker",
          "default": True},
         # The store has had three ACTIVE discount codes since July with zero
         # uses between them, because nothing on the storefront mentions any of
         # them. VOLT20 is the strongest (20% first order). Surfaced here as a
         # setting rather than hardcoded so it can be changed or switched off in
         # the theme editor without a redeploy — and so it disappears cleanly
         # rather than advertising a code that has been deleted in admin.
         {"type": "checkbox", "id": "promo_enabled", "label": "Show offer in ticker",
          "default": True},
         {"type": "text", "id": "promo_text", "label": "Offer text",
          "default": "20% off your first order",
          "info": "Leave blank to hide. Must describe a discount that actually exists."},
         {"type": "text", "id": "promo_code", "label": "Discount code",
          "default": "VOLT20",
          "info": "Must match a live code in Discounts. A dead code here is worse than no offer."},
     ]},
]


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    for d in ('assets', 'config', 'layout', 'locales', 'sections', 'snippets',
              'templates', 'templates/customers'):
        (OUT / d).mkdir(parents=True, exist_ok=True)

    written, missing = [], []

    for src, dst in MAP.items():
        p = ROOT / src
        if p.exists():
            (OUT / dst).write_text(p.read_text())
            written.append(dst)
        else:
            missing.append(f'{src}  ->  {dst}')

    for p in sorted((ROOT / 'theme').glob('customers-*.liquid')):
        name = CUSTOMER_RE.match(p.name).group(1)
        dst = f'templates/customers/{name}.liquid'
        (OUT / dst).write_text(p.read_text())
        written.append(dst)

    # one stylesheet
    css, seen = [], []
    for rel in CSS_ORDER:
        p = ROOT / rel
        if p.exists():
            css.append(f'/* ── {rel} ── */\n{p.read_text().rstrip()}\n')
            seen.append(rel)
        else:
            missing.append(f'{rel}  (stylesheet)')
    (OUT / 'assets/hivolt.css').write_text('\n'.join(css))
    written.append('assets/hivolt.css')

    (OUT / 'config/settings_schema.json').write_text(
        json.dumps(SETTINGS_SCHEMA, indent=2) + '\n')
    (OUT / 'config/settings_data.json').write_text(
        json.dumps({"current": {"show_ticker": True,
                                "promo_enabled": True,
                                "promo_text": "20% off your first order",
                                "promo_code": "VOLT20",
                                "support_email": "support@hivolt-usa.com",
                                # Only the verified profile. The other three
                                # social_* settings stay unset so sameAs omits
                                # them rather than asserting a dead URL.
                                "social_facebook":
                                    "https://www.facebook.com/482588221614644"}},
                   indent=2) + '\n')
    (OUT / 'locales/en.default.json').write_text(json.dumps({"general": {
        "meta": {"tags": "Tagged {{ tags }}", "page": "Page {{ page }}"}}}, indent=2) + '\n')
    written += ['config/settings_schema.json', 'config/settings_data.json',
                'locales/en.default.json']

    if ZIP.exists():
        ZIP.unlink()
    with zipfile.ZipFile(ZIP, 'w', zipfile.ZIP_DEFLATED) as z:
        for f in sorted(OUT.rglob('*')):
            if f.is_file():
                z.write(f, f.relative_to(OUT))

    print(f'built {ZIP.name}  —  {len(written)} files, '
          f'{ZIP.stat().st_size // 1024} KB')
    print(f'stylesheets merged: {len(seen)}')
    if missing:
        print(f'\nNOT YET WRITTEN ({len(missing)}) — theme is incomplete:')
        for m in missing:
            print(f'  · {m}')

    # layout/theme.liquid is the one file Shopify cannot boot without
    if not (OUT / 'layout/theme.liquid').exists():
        print('\nlayout/theme.liquid is missing — Shopify will REJECT this zip.')
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
