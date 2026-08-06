#!/usr/bin/env python3
"""Assemble the HIVOLT Shopify theme from the loose files in site/.

The templates are authored flat (one agent per file, no path collisions).
Shopify needs a specific directory layout and a settings_schema.json, or the
admin rejects the upload. This script maps one to the other, concatenates the
per-agent stylesheets into a single assets/hivolt.css, and writes a zip that
Online Store → Themes → Add theme → Upload zip will accept.

Run:  python3 site/build-theme.py
Out:  HIVOLT-theme.zip
"""
import json, pathlib, re, shutil, sys, zipfile

ROOT = pathlib.Path(__file__).resolve().parent          # site/
OUT = ROOT.parent / 'build' / 'hivolt-theme'
ZIP = ROOT.parent / 'HIVOLT-theme.zip'

# flat authored file  ->  path inside the theme
MAP = {
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
    'theme/layout-theme.liquid':       'layout/theme.liquid',
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
     "theme_support_url": "https://hivolt-usa.com/pages/contact"},
    {"name": "Brand",
     "settings": [
         {"type": "image_picker", "id": "logo", "label": "Logo"},
         {"type": "text", "id": "support_email", "label": "Support email",
          "default": "support@hivolt-usa.com"},
     ]},
    {"name": "Announcements",
     "settings": [
         {"type": "checkbox", "id": "show_ticker", "label": "Show announcement ticker",
          "default": True},
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
                                "support_email": "support@hivolt-usa.com"}},
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
