#!/usr/bin/env python3
"""Build the knowledge graph over this repository's markdown corpus.

Emits warroom/app/data/graph.json — nodes are documents, edges are the
references documents actually make to each other. Nothing is inferred from
similarity or embeddings; an edge exists only where one document names another.

    python3 warroom/graphify.py [--include-tooling] [--out PATH]
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DEFAULT_OUT = REPO / "warroom" / "app" / "data" / "graph.json"

# Reference forms that actually occur in this corpus, most specific first.
REF_PATTERNS = [
    ("wikilink", re.compile(r"\[\[([^\]|#]+?)(?:[|#][^\]]*)?\]\]")),
    ("link", re.compile(r"\]\(([^)\s]+?\.md)(?:#[^)]*)?\)")),
    ("code", re.compile(r"`([A-Za-z0-9._/-]+\.md)`")),
    # Lookbehind must exclude `-` and `.` too, or a bare match starts mid-filename
    # and turns HIVOLT-PDP-RELEASE-QA.md into a phantom PDP-RELEASE-QA.md.
    ("bare", re.compile(r"(?<![`(\[/\w.\-])([A-Za-z0-9._-]+(?:/[A-Za-z0-9._-]+)*\.md)\b")),
]

FENCE = re.compile(r"```.*?```", re.S)
H1 = re.compile(r"^#\s+(.+?)\s*$", re.M)
HEADINGS = re.compile(r"^(#{1,3})\s+(.+?)\s*$", re.M)

# Filename tokens worth filtering on in the UI.
TAG_TOKENS = {
    "AUDIT", "POLICY", "POLICIES", "PRODUCT", "SEO", "GMC", "THEME", "LAUNCH",
    "QA", "CATALOG", "BRAND", "REVIEW", "SOURCING", "SUPPLIER", "TRUST",
    "ANALYTICS", "CRO", "DESIGN", "IMAGE", "GLOBAL", "PUBLISH", "DATA",
    "STATE", "TASKS", "BLOCKERS", "MODEL", "FEED", "SHIPPING", "LEGAL",
}

EXCLUDE_DIRS = ("node_modules/", ".git/")
TOOLING_DIRS = (".claude/", ".agents/", ".claude-flow/")


def tracked_markdown(include_tooling: bool) -> list[str]:
    """Markdown files git knows about, so untracked scratch never enters the graph."""
    try:
        out = subprocess.run(
            ["git", "-C", str(REPO), "ls-files", "*.md"],
            capture_output=True, text=True, check=True,
        ).stdout
    except (subprocess.CalledProcessError, FileNotFoundError):
        out = "\n".join(
            str(p.relative_to(REPO)) for p in REPO.rglob("*.md")
        )
    paths = []
    for rel in out.splitlines():
        rel = rel.strip()
        if not rel or rel.startswith(EXCLUDE_DIRS):
            continue
        if not include_tooling and rel.startswith(TOOLING_DIRS):
            continue
        paths.append(rel)
    return sorted(paths)


def cluster_of(rel: str) -> str:
    parts = rel.split("/")
    if len(parts) == 1:
        return "<root>"
    if parts[0] in (".claude", ".agents", ".claude-flow"):
        return "tooling"
    return parts[0]


def tags_of(rel: str) -> list[str]:
    stem = Path(rel).stem.upper()
    found = [t for t in TAG_TOKENS if t in re.split(r"[^A-Z0-9]+", stem)]
    return sorted(found)


def git_last_commit(rel: str) -> str | None:
    try:
        out = subprocess.run(
            ["git", "-C", str(REPO), "log", "-1", "--format=%cI", "--", rel],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
        return out or None
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def first_prose(body: str) -> str:
    """The first real sentences of a document.

    Table rows, headings, rules and list bullets carry no meaning out of
    context, so they are skipped rather than truncated mid-pipe.
    """
    keep = []
    for line in body.splitlines():
        t = line.strip()
        if not t or t.startswith(("|", "#", "---", "***", "===")):
            continue
        if re.fullmatch(r"[-*+]\s+.*", t) and not keep:
            continue
        t = re.sub(r"^>\s*", "", t)
        if t:
            keep.append(t)
        if sum(len(k) for k in keep) > 300:
            break
    # Emphasis spans wrapped lines, so unwrap first and strip marks after.
    out = re.sub(r"\s+", " ", " ".join(keep))
    out = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", out)   # links -> text
    out = re.sub(r"\*\*([^*]+)\*\*", r"\1", out)          # bold
    out = re.sub(r"(?<!\w)[*_]([^*_\n]+)[*_](?!\w)", r"\1", out)
    return out.replace("`", "").strip()[:260]


def read_doc(rel: str) -> dict:
    text = (REPO / rel).read_text(encoding="utf-8", errors="replace")
    stripped = FENCE.sub(" ", text)

    m = H1.search(text)
    title = m.group(1).strip() if m else Path(rel).stem
    title = re.sub(r"\s*—\s*20\d\d-\d\d-\d\d\s*$", "", title)

    heads = [
        {"level": len(h), "text": t.strip()}
        for h, t in HEADINGS.findall(stripped)
    ][:40]

    excerpt = first_prose(H1.sub("", stripped, count=1))

    return {
        "id": rel,
        "title": title,
        "cluster": cluster_of(rel),
        "tags": tags_of(rel),
        "bytes": len(text.encode("utf-8")),
        "words": len(stripped.split()),
        "headings": heads,
        "excerpt": excerpt,
        "updated": git_last_commit(rel),
        "_raw": stripped,
    }


def build_index(nodes: dict[str, dict]) -> tuple[dict, dict]:
    by_path = {rel: rel for rel in nodes}
    by_base: dict[str, list[str]] = defaultdict(list)
    for rel in nodes:
        by_base[Path(rel).name.lower()].append(rel)
        by_base[Path(rel).stem.lower()].append(rel)
    return by_path, by_base


def resolve(ref: str, src: str, by_path: dict, by_base: dict) -> str | None:
    """Map a reference string onto a real document, or give up.

    Unresolvable references are dropped rather than turned into phantom nodes —
    a graph that invents documents is worse than one with holes.
    """
    ref = ref.strip().lstrip("./")
    if not ref:
        return None
    if not ref.lower().endswith(".md"):
        ref_md = ref + ".md"
    else:
        ref_md = ref

    if ref_md in by_path:
        return ref_md

    # Relative to the referring document's directory.
    joined = os.path.normpath(os.path.join(str(Path(src).parent), ref_md))
    if joined in by_path:
        return joined

    # Unique basename match anywhere in the corpus.
    cands = by_base.get(Path(ref_md).name.lower(), [])
    if len(cands) == 1:
        return cands[0]
    if len(cands) > 1:
        # Prefer a candidate in the same cluster as the source.
        same = [c for c in cands if cluster_of(c) == cluster_of(src)]
        if len(same) == 1:
            return same[0]
    return None


def extract_edges(nodes: dict[str, dict], by_path, by_base) -> tuple[list, Counter]:
    pair_kinds: dict[tuple[str, str], Counter] = defaultdict(Counter)
    unresolved: Counter = Counter()

    for src, node in nodes.items():
        raw = node["_raw"]
        for kind, pat in REF_PATTERNS:
            for m in pat.finditer(raw):
                ref = m.group(1)
                tgt = resolve(ref, src, by_path, by_base)
                if tgt is None:
                    if ref.lower().endswith(".md"):
                        unresolved[ref] += 1
                    continue
                if tgt == src:
                    continue
                pair_kinds[(src, tgt)][kind] += 1

    edges = []
    for (s, t), kinds in sorted(pair_kinds.items()):
        edges.append({
            "s": s,
            "t": t,
            "n": sum(kinds.values()),
            "kind": kinds.most_common(1)[0][0],
        })
    return edges, unresolved


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--include-tooling", action="store_true",
                    help="also graph .claude/ skill and command docs")
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = ap.parse_args()

    paths = tracked_markdown(args.include_tooling)
    if not paths:
        print("no markdown found", file=sys.stderr)
        return 1

    nodes = {rel: read_doc(rel) for rel in paths}
    by_path, by_base = build_index(nodes)
    edges, unresolved = extract_edges(nodes, by_path, by_base)

    indeg: Counter = Counter()
    outdeg: Counter = Counter()
    for e in edges:
        outdeg[e["s"]] += 1
        indeg[e["t"]] += 1

    for rel, node in nodes.items():
        node["inDeg"] = indeg.get(rel, 0)
        node["outDeg"] = outdeg.get(rel, 0)
        del node["_raw"]

    clusters = Counter(n["cluster"] for n in nodes.values())
    orphans = sorted(r for r, n in nodes.items() if not n["inDeg"] and not n["outDeg"])
    hubs = [r for r, _ in indeg.most_common(12)]

    graph = {
        "generated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "includesTooling": args.include_tooling,
        "stats": {
            "docs": len(nodes),
            "edges": len(edges),
            "clusters": len(clusters),
            "orphans": len(orphans),
            "words": sum(n["words"] for n in nodes.values()),
            "unresolvedRefs": sum(unresolved.values()),
        },
        "clusters": [
            {"id": c, "count": n} for c, n in sorted(clusters.items(), key=lambda kv: -kv[1])
        ],
        "hubs": hubs,
        "orphans": orphans,
        "unresolved": [{"ref": r, "n": c} for r, c in unresolved.most_common(25)],
        "nodes": list(nodes.values()),
        "edges": edges,
    }

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(graph, indent=1), encoding="utf-8")

    s = graph["stats"]
    print(f"graph  {s['docs']} docs  {s['edges']} edges  {s['clusters']} clusters  "
          f"{s['orphans']} orphans  {s['unresolvedRefs']} unresolved refs")
    print(f"wrote  {args.out.relative_to(REPO)}  "
          f"({args.out.stat().st_size / 1024:.0f} KB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
