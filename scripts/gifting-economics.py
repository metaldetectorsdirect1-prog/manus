"""Does HIVOLT's margin support gifting product to creators?

Elliott Prendy's beginner method is influencers + Google Shopping. The
influencer half means sending real product to creators who already have the
audience. That only works if one resulting sale pays for the gift.

Gift cost  = unit cost + outbound shipping (the store ships free, so it eats it)
Sale value = price - unit cost - shipping - payment processing
Break-even = gift cost / contribution per sale
"""
import collections
import json
import pathlib

SHIP = 7.00
ROOT = pathlib.Path("/tmp/claude-0/-home-user-manus/"
                    "f9f720c1-823b-5cd8-aec8-e4501793ee60/scratchpad/gs")

products, variants = {}, collections.defaultdict(list)
for line in (ROOT / "econ3.jsonl").read_text().splitlines():
    if not line.strip():
        continue
    d = json.loads(line)
    if "handle" in d:
        if d.get("status") == "ACTIVE":
            products[d["id"]] = d
    elif "price" in d:
        variants[d["__parentId"]].append(d)

rows = []
for pid, p in products.items():
    vs = variants.get(pid, [])
    if not vs:
        continue
    v = vs[0]
    c = (v.get("inventoryItem") or {}).get("unitCost")
    if not c:
        continue
    price, cost = float(v["price"]), float(c["amount"])
    gift = cost + SHIP
    contribution = price - cost - SHIP - (0.029 * price + 0.30)
    rows.append((gift / contribution, p["handle"], price, cost, gift, contribution))

rows.sort()
print(f"{len(rows)} products with a unit cost\n")
print("Sales needed per gifted unit to break even, best first:")
print(f"  {'sales':>6}  {'gift$':>7} {'contrib$':>9}  {'price':>7} {'cost':>7}  handle")
for r in rows[:8]:
    print(f"  {r[0]:6.2f}  {r[4]:7.2f} {r[5]:9.2f}  {r[2]:7.2f} {r[3]:7.2f}  {r[1]}")
print("  ...")
for r in rows[-4:]:
    print(f"  {r[0]:6.2f}  {r[4]:7.2f} {r[5]:9.2f}  {r[2]:7.2f} {r[3]:7.2f}  {r[1]}")

med = rows[len(rows) // 2]
print(f"\nmedian: {med[0]:.2f} sales per gift ({med[1]})")

vc = [r for r in rows if r[1].startswith("voltcore")]
if vc:
    r = vc[0]
    print(f"\nVoltcore hero: gift costs ${r[4]:.2f}, each sale contributes "
          f"${r[5]:.2f}\n  -> break-even at {r[0]:.2f} sales per creator gifted")

print("\nWhat a 25-creator seeding round costs, using the hero:")
if vc:
    g = vc[0][4]
    contribution = vc[0][5]
    for n in (10, 25, 50):
        print(f"  {n:3d} creators  ${n * g:8.2f} outlay   "
              f"break-even at {n * g / contribution:5.1f} total sales "
              f"({n * g / contribution / n:.2f} per creator)")
