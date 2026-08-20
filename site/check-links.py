#!/usr/bin/env python3
"""
Validate every internal /pages/ and /collections/ target in the theme against
the handles that actually exist on the store.

Why this exists
───────────────
On 2026-08-08 a link-repair pass reported "none — all resolved" while six dead
targets were still live in the header and footer. The pass matched a target only
when it was followed by a quote, "#" or "?" — a deliberate guard so that
/pages/contact would not corrupt /pages/contact-us. But layout/theme.liquid
builds its navigation from comma-separated strings:

    {%- assign nav_urls = '/collections/womens,/collections/mens,...' | split: ',' -%}

There, a target is followed by a COMMA. The guard skipped every one of them, and
the check that "verified" the fix used the same guard, so it agreed. A checker
that shares its blind spot with the fix it is checking will always pass.

This script has no boundary rule at all. It extracts each handle with a greedy
character class and compares the WHOLE handle against a set — so /pages/contact
and /pages/contact-us are simply different strings and neither can mask the
other.

Keeping the handle lists current
────────────────────────────────
They are a snapshot of the live store. Refresh with:

    pages(first: 50)       { nodes { handle isPublished } }
    collections(first: 50) { nodes { handle } }

Unpublished pages are NOT valid targets — they return 404 to a shopper exactly
as a missing page does, which is what made /pages/about and /pages/contact
dangerous: they exist in the admin, so they look real in a link audit.
"""
import re
import sys
import glob

# Published pages only — snapshot 2026-08-08.
PAGES = {
    'data-sharing-opt-out', 'about-us', 'faq', 'shipping-delivery',
    '60-day-love-it-guarantee', 'contact-us', 'google-site-verification',
    'returns-refunds', 'size-guide', 'membership', 'drops', 'terms-of-service',
    'accessibility', 'track-order', 'materials-sustainability', 'ambassadors',
    'wholesale', 'voltcore',
}

COLLECTIONS = {
    'frontpage', 'all', 'mens-activewear', 'womens-activewear', 'tops',
    'bottoms', 'outerwear-hoodies', 'training', 'yoga-studio',
    'drop-04-voltcore', 'sports-bras', 'leggings', 'shorts', 'tennis-and-court',
    'football-soccer', 'basketball',
}

# Shopify serves these itself; they are not theme-authored handles.
POLICIES = {
    'privacy-policy', 'terms-of-service', 'refund-policy', 'shipping-policy',
    'legal-notice', 'terms-of-sale', 'contact-information',
}

VALID = {'pages': PAGES, 'collections': COLLECTIONS, 'policies': POLICIES}

# Greedy on the handle: capture it whole, then compare whole. No lookahead, no
# boundary assumption — that is the entire point.
TARGET = re.compile(r'/(pages|collections|policies)/([a-z0-9][a-z0-9\-]*)')


def main(argv):
    files = argv[1:] or sorted(glob.glob('*.liquid') + glob.glob('theme/*.liquid'))
    if not files:
        print('check-links: no templates given and none found', file=sys.stderr)
        return 2

    dead = {}
    checked = 0
    for path in files:
        try:
            src = open(path, encoding='utf-8').read()
        except OSError as exc:
            print('check-links: cannot read %s: %s' % (path, exc), file=sys.stderr)
            return 2
        for match in TARGET.finditer(src):
            kind, handle = match.group(1), match.group(2)
            checked += 1
            if handle not in VALID[kind]:
                line = src.count('\n', 0, match.start()) + 1
                dead.setdefault(path, []).append((line, '/%s/%s' % (kind, handle)))

    if not dead:
        print('  ok  %d internal targets, all resolve' % checked)
        return 0

    for path in sorted(dead):
        for line, target in dead[path]:
            print('  DEAD  %s:%d  %s' % (path, line, target))
    total = sum(len(v) for v in dead.values())
    print('\n%d dead target(s) across %d file(s), out of %d checked'
          % (total, len(dead), checked))
    return 1


if __name__ == '__main__':
    sys.exit(main(sys.argv))
