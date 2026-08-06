#!/usr/bin/env python3
"""Structural checks for the HIVOLT Liquid templates.

Not a Liquid parser — a guard against the specific ways these files break:
unbalanced blocks, colour literals that bypass the token system, banned
social-proof patterns, and images without dimensions.
"""
import re, sys, json, pathlib

BLOCKS = {'if':'endif','unless':'endunless','for':'endfor','case':'endcase',
          'capture':'endcapture','form':'endform','paginate':'endpaginate',
          'comment':'endcomment','tablerow':'endtablerow','raw':'endraw',
          'schema':'endschema','style':'endstyle','javascript':'endjavascript'}
OPEN = set(BLOCKS); CLOSE = {v:k for k,v in BLOCKS.items()}

BANNED = [
    (r'\b\d+\s*(people|customers|shoppers)\s+(are\s+)?(viewing|bought|watching)', 'fake live-viewer / social proof'),
    (r'\bcountdown\b|\bexpires? in\b|\bhurry\b|\bonly \d+ left\b', 'urgency / scarcity'),
    (r'★|⭐|\bstar rating\b|\breview_count\b|\brating_count\b', 'star rating / review count'),
    (r'\bcellulite\b|\bvaricose\b|\blipedema\b|\blymphatic\b|\bmedical[- ]grade\b', 'health / medical claim'),
    (r'\bbuttery\b|\bluxurious\b|\bsecond[- ]skin\b', 'banned marketing adjective'),
]
COLOUR = re.compile(r'#[0-9a-fA-F]{3,8}\b')

def check(path):
    src = pathlib.Path(path).read_text()
    errs, warns = [], []

    # 1. block balance
    stack = []
    for m in re.finditer(r'\{%-?\s*(\w+)', src):
        tag = m.group(1)
        line = src[:m.start()].count('\n') + 1
        if tag in OPEN:
            stack.append((tag, line))
        elif tag in CLOSE:
            want = CLOSE[tag]
            if not stack:
                errs.append(f'line {line}: {{% {tag} %}} with nothing open')
            elif stack[-1][0] != want:
                errs.append(f'line {line}: {{% {tag} %}} closes {{% {stack[-1][0]} %}} opened line {stack[-1][1]}')
                stack.pop()
            else:
                stack.pop()
    for tag, line in stack:
        errs.append(f'line {line}: {{% {tag} %}} never closed')

    # 2. colour literals outside a <style> block or a .css file
    if not path.endswith('.css'):
        stripped = re.sub(r'<style>.*?</style>', '', src, flags=re.S)
        stripped = re.sub(r'<script type="application/ld\+json">.*?</script>', '', stripped, flags=re.S)
        for m in COLOUR.finditer(stripped):
            warns.append(f'line {stripped[:m.start()].count(chr(10))+1}: colour literal {m.group(0)} — use var(--token)')

    # 3. banned content.
    # A naive match can't tell "we use countdowns" from "no countdowns" — the
    # HIVOLT copy deliberately names these tactics in order to disavow them.
    # Treat a match as clean when a negation cue precedes it in the same clause.
    NEG = re.compile(r"(\bno\b|\bnot\b|\bnever\b|\bwon't\b|\bdon't\b|\bwithout\b|"
                     r"\bthere are no\b|\bhiding (it )?behind\b|\bnothing\b|\brather than\b|"
                     r"\bfake\b|\bnot here\b|\bwe('ll)? (won't|refuse)\b)[^.;]{0,90}$")
    low = src.lower()
    for pat, why in BANNED:
        for m in re.finditer(pat, low):
            line = low[:m.start()].count(chr(10)) + 1
            before = low[max(0, m.start()-140):m.start()]
            after  = low[m.end():m.end()+140]
            # negation can sit either side: "no countdowns" / "sell them as
            # treatments for cellulite. We won't."
            if NEG.search(before) or re.search(r"\b(we won't|we don't|we do not|not here|never)\b", after):
                continue          # disavowal, not a claim
            # a term inside quotation marks is being cited, not claimed:
            #   'why "compression" and "buttery" answer nothing'
            if re.search(r'["\u201c\u2018\u2019\u201d]\s*$', src[:m.start()]) and \
               re.match(r'\s*["\u201c\u2018\u2019\u201d]', src[m.end():]):
                continue
            errs.append(f'line {line}: {why} — "{src[m.start():m.end()][:40]}"')

    # 4. shell duplication.
    # layout/theme.liquid owns <main>, the ticker, the masthead and the footer.
    # A page template that emits any of them produces nested landmarks. Agents
    # working in parallel wrote several templates before the layout existed, so
    # this is checked rather than trusted.
    if 'layout-theme' not in path and path.endswith('.liquid'):
        nocomment = re.sub(r'\{%-?\s*comment\s*-?%\}.*?\{%-?\s*endcomment\s*-?%\}',
                           '', src, flags=re.S)
        for pat, what in ((r'<main\b', '<main>'),
                          (r'<header class="mast"', 'masthead'),
                          (r'<footer class="foot"', 'footer'),
                          (r'<div class="ticker"', 'ticker')):
            for m in re.finditer(pat, nocomment):
                errs.append(f'line {nocomment[:m.start()].count(chr(10))+1}: '
                            f'{what} belongs to layout/theme.liquid — page templates are content-only')

    # 5. images need dimensions
    for m in re.finditer(r'<img\b[^>]*>', src, re.S):
        tag = m.group(0)
        line = src[:m.start()].count('\n') + 1
        if 'width=' not in tag or 'height=' not in tag:
            warns.append(f'line {line}: <img> missing width/height')
        if 'alt=' not in tag:
            errs.append(f'line {line}: <img> missing alt')

    # 6. JSON-LD validity
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', src, re.S):
        body = m.group(1)
        line = src[:m.start()].count('\n') + 1
        if '{{' in body or '{%' in body:
            continue  # Liquid-templated, can't parse statically
        try: json.loads(body)
        except Exception as e:
            errs.append(f'line {line}: invalid JSON-LD — {e}')

    return errs, warns

if __name__ == '__main__':
    bad = 0
    for p in sys.argv[1:]:
        e, w = check(p)
        status = 'FAIL' if e else ('warn' if w else 'ok')
        print(f'{status:>4}  {p}')
        for x in e: print(f'      ERROR  {x}'); 
        for x in w[:8]: print(f'      warn   {x}')
        if len(w) > 8: print(f'      warn   … {len(w)-8} more')
        if e: bad += 1
    sys.exit(1 if bad else 0)
