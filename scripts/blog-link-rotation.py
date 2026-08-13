"""Why only half the offsets get used, and which Liquid expression fixes it."""
import json
import pathlib

ROOT = pathlib.Path("/tmp/claude-0/-home-user-manus/"
                    "f9f720c1-823b-5cd8-aec8-e4501793ee60/scratchpad/gs")

arts = []
for line in (ROOT / "articles.jsonl").read_text().splitlines():
    if not line.strip():
        continue
    d = json.loads(line)
    if "id" in d and "handle" in d:
        arts.append((int(d["id"].rsplit("/", 1)[-1]), d.get("title") or ""))

ids = [a for a, _ in arts]
print(f"{len(ids)} articles")
print(f"  all even?  {all(i % 2 == 0 for i in ids)}")
print(f"  all div 4? {all(i % 4 == 0 for i in ids)}")
srt = sorted(ids)
gaps = sorted({srt[i + 1] - srt[i] for i in range(min(60, len(srt) - 1))})
print(f"  smallest gaps between consecutive ids: {gaps[:8]}")

SPAN = 46


def coverage(offsets, size=50):
    reached = {p for o in offsets for p in range(o, o + 4) if p < size}
    return len(set(offsets)), len(reached)


cands = {
    "article.id                        ": [i % SPAN for i in ids],
    "article.id | divided_by: 2        ": [(i // 2) % SPAN for i in ids],
    "article.id | plus: title.size     ": [(i + len(t)) % SPAN for i, t in arts],
    "article.id | divided_by: 2 | plus: title.size":
        [((i // 2) + len(t)) % SPAN for i, t in arts],
}

print(f"\nagainst a 50-product pool (span {SPAN}):")
print(f"  {'expression':46s} {'offsets':>8s} {'reached':>8s}")
for name, offs in cands.items():
    used, reached = coverage(offs)
    print(f"  {name:46s} {used:3d}/{SPAN:<4d} {reached:3d}/50")
