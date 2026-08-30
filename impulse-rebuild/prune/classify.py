#!/usr/bin/env python3
"""
Deterministic prune classifier for the HIVOLT blog corpus.

METHOD (standing rule 1.3): this classifies by HANDLE KEYWORD ONLY.
It does NOT read article bodies. A handle is a strong but imperfect proxy for
subject; the rules below are stated so any disagreement is checkable, and the
output is a proposal for owner confirmation, not an executed decision.

Limits, stated up front:
  - An article whose handle does not signal its subject is misclassified.
  - No claim is made about article CONTENT quality, only topical category.
  - Traffic is measured (Shopify sessions, 90d) and is a floor: the analytics
    API caps at 250 rows per query and both the ASC and DESC windows truncated,
    so articles with 0 here may have had 1 session.
"""
import re, sys, json, os

BASE = os.path.dirname(os.path.abspath(__file__))
handles = [l.strip() for l in open(os.path.join(BASE, 'articles-501.txt')) if l.strip()]

# --- category-neutral: transferable to a general women's clothing store ---
CARE = (r'wash|dryer|air-drying|how-to-dry|detergent|softener|stain|pilling|smell|'
        r'odor|odour|storing-|repairing|care-label|fade|lint-on|static-cling|snag|shrink')
FABRIC = (r'fabric|gsm|polyester|nylon|polyamide|spandex|elastane|moisture-wicking|'
          r'thermal-regulation|breathab|four-way-stretch|seamless-vs-flatlock|flatlock|'
          r'bonded-hems|jacquard|compression-fabric|recycled-polyester|opacity|squat-proof|'
          r'stretch-recovery|brushed-vs-slick|anti-odor|anti-chafe|chafing')
SIZING = (r'sizing|size-chart|activewear-size|between-sizes|how-should-.*-fit|'
          r'-fit-guide|fit-rules|armhole-gap|waistband-rolling|leggings-falling-down|'
          r'shorts-riding-up|sports-bra-straps|when-to-replace-a-sports-bra|'
          r'how-long-do-leggings-last|the-squat-test|legging-length-guide|'
          r'petite-activewear-fit|tall-women-s-activewear|jacket-fit-for-training')

KEEP_RE = re.compile(f'({CARE})|({FABRIC})|({SIZING})')
ROUNDUP_RE = re.compile(r'^best-|^the-best-|^quality-activewear|gifts?-')

def classify(h):
    if KEEP_RE.search(h):
        # a round-up that merely mentions fabric is still a round-up
        if ROUNDUP_RE.search(h):
            return 'delete', 'product round-up (fabric keyword incidental)'
        return 'keep', 'category-neutral: care / fabric / sizing'
    if ROUNDUP_RE.search(h):
        return 'delete', 'product round-up for a catalog that does not exist'
    return 'delete', 'training / styling / off-category'

rows = [(h,) + classify(h) for h in handles]
keep = [r for r in rows if r[1] == 'keep']
dele = [r for r in rows if r[1] == 'delete']

print(f"corpus           : {len(handles)}")
print(f"KEEP  (survivors): {len(keep)}")
print(f"DELETE           : {len(dele)}")
print(f"round-ups deleted: {sum(1 for r in dele if 'round-up' in r[2])}")
print()
if '--list' in sys.argv:
    for h, c, why in sorted(keep):
        print(f"KEEP   {h}")
if '--json' in sys.argv:
    json.dump({'keep':[r[0] for r in keep], 'delete':[r[0] for r in dele]},
              open(os.path.join(BASE,'prune-map.json'),'w'), indent=1)
    print("wrote prune-map.json")
