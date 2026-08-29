#!/usr/bin/env python3
"""Extract operational state from the repository's source-of-truth documents.

Emits warroom/app/data/state.json. Every panel carries the document it came
from and how old that document is, because this repository's own rules say the
state files are a convenience and not an authority — the War Room must show
that, not hide it.

    python3 warroom/extract_state.py [--out PATH]
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DEFAULT_OUT = REPO / "warroom" / "app" / "data" / "state.json"

BLOCKERS = "docs/HIVOLT-OPERATIONS-BLOCKERS.md"
TASKS = "docs/HIVOLT-MASTER-TASKS.md"
CURRENT = "docs/HIVOLT-CURRENT-STATE.md"
RULES = "CLAUDE.md"

# Blocker classes, ordered by who can actually clear them.
CLASS_ORDER = ["OWNER DECISION", "LEGAL REVIEW", "CONTENT", "OPERATIONAL"]


def git_date(rel: str) -> str | None:
    try:
        out = subprocess.run(
            ["git", "-C", str(REPO), "log", "-1", "--format=%cI", "--", rel],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
        return out or None
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def age_days(iso: str | None) -> int | None:
    if not iso:
        return None
    try:
        then = datetime.fromisoformat(iso)
    except ValueError:
        return None
    if then.tzinfo is None:
        then = then.replace(tzinfo=timezone.utc)
    return (datetime.now(timezone.utc) - then).days


def source(rel: str) -> dict:
    d = git_date(rel)
    return {"doc": rel, "updated": d, "ageDays": age_days(d)}


def read(rel: str) -> str:
    p = REPO / rel
    return p.read_text(encoding="utf-8", errors="replace") if p.exists() else ""


def split_row(line: str) -> list[str]:
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]
    return [c.strip() for c in line.split("|")]


def is_sep(line: str) -> bool:
    return bool(re.fullmatch(r"\|?[\s:|-]+\|?", line.strip())) and "-" in line


def parse_tables(text: str) -> list[list[dict]]:
    """Every markdown table in a block of text, as lists of header->cell dicts."""
    tables, lines, i = [], text.splitlines(), 0
    while i < len(lines):
        if lines[i].strip().startswith("|") and i + 1 < len(lines) and is_sep(lines[i + 1]):
            header = split_row(lines[i])
            i += 2
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                cells = split_row(lines[i])
                if len(cells) < len(header):
                    cells += [""] * (len(header) - len(cells))
                rows.append({h or f"c{n}": cells[n] for n, h in enumerate(header)})
                i += 1
            if rows:
                tables.append(rows)
        else:
            i += 1
    return tables


def section(text: str, heading: str) -> str:
    """Body of the first heading matching `heading`, up to the next same-or-higher one."""
    pat = re.compile(r"^(#{2,4})\s*" + heading + r".*$", re.M | re.I)
    m = pat.search(text)
    if not m:
        return ""
    level = len(m.group(1))
    rest = text[m.end():]
    nxt = re.search(r"^#{1," + str(level) + r"}\s", rest, re.M)
    return rest[: nxt.start()] if nxt else rest


def first_table(text: str, heading: str) -> list[dict]:
    tabs = parse_tables(section(text, heading))
    return tabs[0] if tabs else []


def clean(s: str) -> str:
    """Collapse whitespace; keep inline markdown for the UI to render."""
    return re.sub(r"\s+", " ", s).strip()


def norm_class(raw: str) -> str:
    up = re.sub(r"\*", "", raw).upper()
    for c in CLASS_ORDER:
        if c in up:
            return c
    if "OWNER" in up:
        return "OWNER DECISION"
    return "OPERATIONAL"


def extract_blockers(text: str) -> list[dict]:
    tabs = parse_tables(text)
    if not tabs:
        return []
    out = []
    for row in tabs[0]:
        vals = list(row.values())
        if len(vals) < 4:
            continue
        num, title, klass, detail = vals[0], vals[1], vals[2], vals[3]
        out.append({
            "id": clean(num).strip("*"),
            "title": clean(title),
            "class": norm_class(klass),
            "classRaw": clean(klass),
            "detail": clean(detail),
        })
    return out


def extract_rows(text: str, heading: str, keys: tuple[str, ...]) -> list[dict]:
    rows = first_table(text, heading)
    out = []
    for row in rows:
        vals = [clean(v) for v in row.values()]
        if not any(vals):
            continue
        item = {k: (vals[n] if n < len(vals) else "") for n, k in enumerate(keys)}
        out.append(item)
    return out


def extract_themes(text: str) -> list[dict]:
    rows = first_table(text, r"Shopify themes")
    out = []
    for row in rows:
        vals = [clean(v) for v in row.values()]
        if len(vals) < 3:
            continue
        role = re.sub(r"[`*]", "", vals[1]).strip()
        out.append({
            "id": re.sub(r"[`*]", "", vals[0]).strip(),
            "role": role,
            "name": vals[2],
            "isMain": role.upper() == "MAIN",
        })
    return out


def extract_kv(text: str, heading: str) -> list[dict]:
    rows = first_table(text, heading)
    out = []
    for row in rows:
        vals = [clean(v) for v in row.values()]
        if len(vals) >= 2 and (vals[0] or vals[1]):
            out.append({"k": vals[0], "v": vals[1]})
    return out


def extract_mutation_sequence(text: str) -> dict:
    body = section(text, r"The mutation sequence")
    steps = []
    for m in re.finditer(r"^(\d+)\.\s+(.+?)(?=\n\d+\.|\n\n|\Z)", body, re.M | re.S):
        steps.append({"n": int(m.group(1)), "text": clean(m.group(2))})
    phases = []
    for label in ("Before", "After"):
        pm = re.search(r"^\*\*" + label + r"\*\*", body, re.M)
        if pm:
            phases.append({"label": label, "at": pm.start()})
    return {"steps": steps, "phases": [p["label"] for p in phases]}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = ap.parse_args()

    t_block, t_tasks, t_cur, t_rules = (read(p) for p in (BLOCKERS, TASKS, CURRENT, RULES))

    blockers = extract_blockers(t_block)
    by_class = {c: [b for b in blockers if b["class"] == c] for c in CLASS_ORDER}

    themes = extract_themes(t_cur)
    catalog = extract_kv(t_cur, r"Catalog")
    issues = extract_rows(t_cur, r"Known unresolved issues", ("id", "issue", "state"))
    issues = [i for i in issues if not i["issue"].startswith("~~")]

    owner_blocked = extract_rows(t_tasks, r"Blocked on OWNER", ("id", "item", "why", "action"))
    tech_queue = extract_rows(t_tasks, r"TECH queue", ("id", "item", "why", "action"))
    carried = extract_rows(t_tasks, r"Open items carried forward", ("id", "item", "why", "action"))

    state = {
        "generated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "warning": (
            "Every panel below is parsed from a markdown document written by a "
            "past session. CLAUDE.md is explicit that these files are a "
            "convenience, not an authority. Re-query Shopify before any write."
        ),
        "panels": {
            "blockers": {
                "source": source(BLOCKERS),
                "total": len(blockers),
                "byClass": {c: len(v) for c, v in by_class.items()},
                "items": blockers,
            },
            "themes": {
                "source": source(CURRENT),
                "authoritative": False,
                "note": (
                    "Theme role must never be inferred from this table. IDs "
                    "survive role changes and names go stale; only Shopify's "
                    "live `role` field is authoritative."
                ),
                "items": themes,
            },
            "catalog": {"source": source(CURRENT), "items": catalog},
            "issues": {"source": source(CURRENT), "items": issues},
            "ownerBlocked": {"source": source(TASKS), "items": owner_blocked},
            "techQueue": {"source": source(TASKS), "items": tech_queue},
            "carried": {"source": source(TASKS), "items": carried},
            "safety": {"source": source(RULES), **extract_mutation_sequence(t_rules)},
        },
    }

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(state, indent=1), encoding="utf-8")

    p = state["panels"]
    print(f"state  {p['blockers']['total']} blockers  {len(themes)} themes  "
          f"{len(issues)} open issues  {len(owner_blocked)} owner-blocked  "
          f"{len(tech_queue)} tech-queue  {len(p['safety']['steps'])} safety steps")
    print(f"wrote  {args.out.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
