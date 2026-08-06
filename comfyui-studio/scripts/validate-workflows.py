#!/usr/bin/env python3
"""Validate ComfyUI API-format workflows against a running ComfyUI server.

Two independent passes:

  1. STRUCTURAL - every class_type exists; every required input is supplied;
     no unknown inputs; every link points at a real node/output slot; and the
     linked output type matches the declared input type.

  2. LIVE - POST each workflow to ComfyUI's own /prompt validator. Errors that
     are purely "this model file isn't downloaded yet" are reported as PENDING
     rather than FAIL, so the graph can be validated before a 24 GB download.

Usage:
    python validate-workflows.py [--url http://127.0.0.1:8188] [--dir ../workflows]

Exit code 0 = all graphs structurally valid.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys
import urllib.error
import urllib.request

# Inputs ComfyUI injects at runtime; never supplied in a saved workflow.
HIDDEN = {"prompt", "extra_pnginfo", "unique_id", "dynprompt", "auth_token_comfy_org", "api_key_comfy_org"}

# Wildcard-ish types that we do not hard-type-check.
ANY = {"*", "COMBO"}


def fetch(url: str, timeout: int = 120):
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode())


def post(url: str, payload: dict, timeout: int = 120):
    data = json.dumps(payload).encode()
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        try:
            return e.code, json.loads(body)
        except Exception:
            return e.code, {"error": body}


def input_specs(node_def: dict) -> dict:
    """Flatten required+optional inputs -> {name: (type, is_required)}."""
    out = {}
    inp = node_def.get("input", {}) or {}
    for name, spec in (inp.get("required", {}) or {}).items():
        out[name] = (spec[0] if spec else "*", True)
    for name, spec in (inp.get("optional", {}) or {}).items():
        out[name] = (spec[0] if spec else "*", False)
    return out


def type_of(spec_type) -> str:
    # A list in object_info means a COMBO of literal choices.
    return "COMBO" if isinstance(spec_type, list) else str(spec_type)


def structural(wf: dict, oi: dict) -> list[str]:
    errs: list[str] = []
    for nid, node in wf.items():
        ct = node.get("class_type")
        if not ct:
            errs.append(f"node {nid}: missing class_type")
            continue
        if ct not in oi:
            errs.append(f"node {nid}: unknown node type '{ct}'")
            continue

        defn = oi[ct]
        specs = input_specs(defn)
        given = node.get("inputs", {}) or {}

        for name, (stype, required) in specs.items():
            if required and name not in given and name not in HIDDEN:
                errs.append(f"node {nid} ({ct}): missing required input '{name}'")

        for name, val in given.items():
            if name not in specs:
                errs.append(f"node {nid} ({ct}): unknown input '{name}'")
                continue
            declared = type_of(specs[name][0])

            # A link is [source_node_id, output_index].
            if isinstance(val, list) and len(val) == 2 and isinstance(val[1], int):
                src, slot = str(val[0]), val[1]
                if src not in wf:
                    errs.append(f"node {nid} ({ct}).{name}: links to missing node '{src}'")
                    continue
                src_ct = wf[src].get("class_type")
                if src_ct not in oi:
                    continue
                outs = oi[src_ct].get("output", []) or []
                if slot >= len(outs):
                    errs.append(
                        f"node {nid} ({ct}).{name}: node {src} ({src_ct}) has "
                        f"{len(outs)} outputs, wanted slot {slot}")
                    continue
                produced = type_of(outs[slot])
                if declared not in ANY and produced not in ANY and produced != declared:
                    errs.append(
                        f"node {nid} ({ct}).{name}: type mismatch - "
                        f"{src} ({src_ct}) outputs {produced}, expected {declared}")
    return errs


def is_missing_model(msg: dict) -> bool:
    """True when a /prompt error is only 'that model file isn't installed yet'."""
    if msg.get("type") in {"value_not_in_list", "invalid_combo_value"}:
        return True
    text = json.dumps(msg).lower()
    return "not in list" in text or "not in the list" in text


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", default="http://127.0.0.1:8188")
    ap.add_argument("--dir", default=str(pathlib.Path(__file__).resolve().parent.parent / "workflows"))
    ap.add_argument("--skip-live", action="store_true", help="structural checks only")
    args = ap.parse_args()

    wdir = pathlib.Path(args.dir)
    files = sorted(wdir.glob("*.json"))
    if not files:
        print(f"no workflows found in {wdir}")
        return 1

    try:
        oi = fetch(f"{args.url}/object_info")
    except Exception as e:
        print(f"ERROR: cannot reach ComfyUI at {args.url}: {e}")
        print("Start ComfyUI first (scripts/start-comfyui.sh), then re-run.")
        return 1

    print(f"ComfyUI at {args.url} exposes {len(oi)} node types\n")

    failed = 0
    for f in files:
        wf = json.loads(f.read_text())
        errs = structural(wf, oi)
        if errs:
            failed += 1
            print(f"FAIL  {f.name}")
            for e in errs:
                print(f"        {e}")
            continue

        line = f"OK    {f.name:38} {len(wf):2d} nodes  structural"
        if args.skip_live:
            print(line)
            continue

        status, body = post(f"{args.url}/prompt",
                            {"prompt": wf, "client_id": "validate-workflows"})
        if status == 200:
            print(f"{line} + live-accepted (QUEUED)")
            continue

        node_errors = (body.get("node_errors") or {})
        blocking, pending = [], []
        for nid, ne in node_errors.items():
            for msg in ne.get("errors", []):
                (pending if is_missing_model(msg) else blocking).append(
                    f"{nid}: {msg.get('message')} ({msg.get('details')})")
        top = body.get("error") or {}
        if top and not node_errors and not is_missing_model(top):
            blocking.append(f"{top.get('message')} ({top.get('details')})")

        if blocking:
            failed += 1
            print(f"FAIL  {f.name}   live validation")
            for b in blocking:
                print(f"        {b}")
        else:
            print(f"{line} + live-validated (PENDING model download: {len(pending)})")

    print()
    if failed:
        print(f"{failed}/{len(files)} workflows FAILED")
        return 1
    print(f"all {len(files)} workflows valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
