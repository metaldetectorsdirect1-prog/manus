#!/usr/bin/env python3
"""Rewrite workflows/*.json so they reference the weights the detected profile installs.

Safetensors profiles only need filenames + weight_dtype changed. The 'gguf' profile
additionally swaps the two loader node types, because ComfyUI-GGUF supplies its own:

    UNETLoader      -> UnetLoaderGGUF      (drops 'weight_dtype')
    DualCLIPLoader  -> DualCLIPLoaderGGUF  (drops 'device')

Usage:
    python apply-profile.py --profile balanced
    python apply-profile.py --profile gguf --dir ../workflows
    python apply-profile.py --profile high --dry-run
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
DEFAULT_CFG = HERE.parent / "config" / "model-profiles.json"
DEFAULT_WF = HERE.parent / "workflows"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--profile", required=True)
    ap.add_argument("--config", default=str(DEFAULT_CFG))
    ap.add_argument("--dir", default=str(DEFAULT_WF))
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    cfg = json.loads(pathlib.Path(args.config).read_text())
    profiles = cfg["profiles"]
    if args.profile not in profiles:
        print(f"unknown profile '{args.profile}'. choices: {', '.join(profiles)}")
        return 2
    p = profiles[args.profile]

    unet_name = p["unet_name"]
    t5_name = p["t5_name"]
    weight_dtype = p.get("weight_dtype")
    use_gguf = bool(p.get("gguf"))

    wdir = pathlib.Path(args.dir)
    changed_files = 0

    for f in sorted(wdir.glob("*.json")):
        wf = json.loads(f.read_text())
        edits: list[str] = []

        for nid, node in wf.items():
            ct = node.get("class_type")
            ins = node.setdefault("inputs", {})

            if ct in ("UNETLoader", "UnetLoaderGGUF"):
                if ins.get("unet_name") != unet_name:
                    ins["unet_name"] = unet_name
                    edits.append(f"{nid}.unet_name={unet_name}")
                if use_gguf:
                    if ct != "UnetLoaderGGUF":
                        node["class_type"] = "UnetLoaderGGUF"
                        edits.append(f"{nid}: UNETLoader -> UnetLoaderGGUF")
                    if ins.pop("weight_dtype", None) is not None:
                        edits.append(f"{nid}: dropped weight_dtype (GGUF)")
                else:
                    if ct != "UNETLoader":
                        node["class_type"] = "UNETLoader"
                        edits.append(f"{nid}: UnetLoaderGGUF -> UNETLoader")
                    if ins.get("weight_dtype") != weight_dtype:
                        ins["weight_dtype"] = weight_dtype
                        edits.append(f"{nid}.weight_dtype={weight_dtype}")

            elif ct in ("DualCLIPLoader", "DualCLIPLoaderGGUF"):
                # clip_name2 is the T5 slot (clip_name1 stays clip_l).
                if ins.get("clip_name2") != t5_name:
                    ins["clip_name2"] = t5_name
                    edits.append(f"{nid}.clip_name2={t5_name}")
                if use_gguf:
                    if ct != "DualCLIPLoaderGGUF":
                        node["class_type"] = "DualCLIPLoaderGGUF"
                        edits.append(f"{nid}: DualCLIPLoader -> DualCLIPLoaderGGUF")
                    if ins.pop("device", None) is not None:
                        edits.append(f"{nid}: dropped device (GGUF loader has no such input)")
                else:
                    if ct != "DualCLIPLoader":
                        node["class_type"] = "DualCLIPLoader"
                        edits.append(f"{nid}: DualCLIPLoaderGGUF -> DualCLIPLoader")
                    ins.setdefault("device", "default")

        if edits:
            changed_files += 1
            print(f"{f.name}")
            for e in edits:
                print(f"    {e}")
            if not args.dry_run:
                f.write_text(json.dumps(wf, indent=2) + "\n")

    verb = "would change" if args.dry_run else "updated"
    print(f"\nprofile '{args.profile}': {verb} {changed_files} workflow(s)")
    if use_gguf:
        print("note: the gguf profile requires the ComfyUI-GGUF custom node "
              "(scripts/04-install-custom-nodes.sh installs it).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
