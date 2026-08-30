#!/usr/bin/env python3
"""Bundle the War Room into one self-contained HTML file.

Inlines the stylesheet, both scripts and both generated data payloads, so the
result runs from a file:// path, an email attachment or any static host with
no server and no fetches. Fonts still come from Google Fonts; everything else
ships in the file.

    python3 warroom/bundle.py [--out PATH] [--fragment]

--fragment omits the <!doctype>/<html>/<head> wrapper, for hosts that supply
their own document shell.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
APP = HERE / "app"
DEFAULT_OUT = HERE / "dist" / "warroom.html"

# Google Fonts is imported by the stylesheet; a bundled file keeps that link
# rather than embedding several hundred KB of font binary.
FONTS = ("https://fonts.googleapis.com/css2?"
         "family=IBM+Plex+Mono:wght@400;500&"
         "family=IBM+Plex+Sans:wght@400;500;600&display=swap")


def read(name: str) -> str:
    return (APP / name).read_text(encoding="utf-8")


def body_of(html: str) -> str:
    """The page content between <body> and </body>, minus the script tags we re-inline."""
    m = re.search(r"<body[^>]*>(.*)</body>", html, re.S | re.I)
    inner = m.group(1) if m else html
    return re.sub(r'\s*<script src="[^"]+"></script>', "", inner).strip()


def title_of(html: str) -> str:
    m = re.search(r"<title>(.*?)</title>", html, re.S | re.I)
    return m.group(1).strip() if m else "War Room"


def payload(name: str) -> str:
    """JSON safe to embed in a <script> block."""
    data = json.loads((APP / "data" / name).read_text(encoding="utf-8"))
    return (json.dumps(data, separators=(",", ":"))
            .replace("</", "<\\/")          # cannot close the script element
            .replace(" ", "\\u2028")   # JS line terminators
            .replace(" ", "\\u2029"))


def build(fragment: bool) -> str:
    index = read("index.html")
    css = read("app.css")
    # The @import must lead a stylesheet; as an inline <style> it would be
    # dropped, so the font request becomes a real <link> instead.
    css = re.sub(r"@import url\([^)]*\);\s*", "", css, count=1)

    parts = [
        f"<title>{title_of(index)}</title>",
        f'<link rel="stylesheet" href="{FONTS}">',
        f"<style>\n{css}\n</style>",
        body_of(index),
        "<script>\n"
        f"window.__GRAPH__={payload('graph.json')};\n"
        f"window.__STATE__={payload('state.json')};\n"
        "</script>",
        f"<script>\n{read('graph.js')}\n</script>",
        f"<script>\n{read('app.js')}\n</script>",
    ]
    inner = "\n".join(parts)

    if fragment:
        return inner + "\n"
    return (
        '<!doctype html>\n<html lang="en" data-view="command">\n<head>\n'
        '<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        "</head>\n<body>\n" + inner + "\n</body>\n</html>\n"
    )


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    ap.add_argument("--fragment", action="store_true")
    args = ap.parse_args()

    html = build(args.fragment)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(html, encoding="utf-8")
    print(f"bundled {args.out}  ({len(html.encode('utf-8')) / 1024:.0f} KB, "
          f"{'fragment' if args.fragment else 'full document'})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
