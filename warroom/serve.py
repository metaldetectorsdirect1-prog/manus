#!/usr/bin/env python3
"""Run the War Room.

    python3 warroom/serve.py              # rebuild the brain, serve on :8787
    python3 warroom/serve.py --no-build   # serve what is already generated
    python3 warroom/serve.py --port 9000

Honours $PORT and binds 0.0.0.0 when it is set, so the same entrypoint works
unchanged on Railway, Render, Fly or any PaaS that injects a port.
"""
from __future__ import annotations

import argparse
import functools
import http.server
import os
import socketserver
import subprocess
import sys
import webbrowser
from pathlib import Path

HERE = Path(__file__).resolve().parent
APP = HERE / "app"


class Handler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Generated data must never be served from a stale cache.
        if self.path.startswith("/data/"):
            self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def log_message(self, fmt, *args):
        if "GET /data/" in (fmt % args) or " 404 " in (fmt % args):
            sys.stderr.write("  %s\n" % (fmt % args))


def rebuild() -> bool:
    ok = True
    for script in ("graphify.py", "extract_state.py"):
        r = subprocess.run([sys.executable, str(HERE / script)],
                           capture_output=True, text=True)
        sys.stdout.write(r.stdout)
        if r.returncode != 0:
            sys.stderr.write(r.stderr)
            ok = False
    return ok


def main() -> int:
    env_port = os.environ.get("PORT")
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--port", type=int, default=int(env_port or 8787))
    ap.add_argument("--host", default="0.0.0.0" if env_port else "127.0.0.1")
    ap.add_argument("--no-build", action="store_true")
    ap.add_argument("--open", action="store_true", help="open a browser")
    args = ap.parse_args()

    if not args.no_build and not rebuild():
        print("build failed — serving whatever is already generated", file=sys.stderr)

    for f in ("data/graph.json", "data/state.json"):
        if not (APP / f).exists():
            print(f"missing {f}; run without --no-build", file=sys.stderr)
            return 1

    socketserver.TCPServer.allow_reuse_address = True
    handler = functools.partial(Handler, directory=str(APP))
    with socketserver.TCPServer((args.host, args.port), handler) as httpd:
        url = f"http://{'localhost' if args.host == '0.0.0.0' else args.host}:{args.port}/"
        print(f"\n  War Room  {url}\n  ctrl-c to stop\n")
        if args.open:
            webbrowser.open(url)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nstopped")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
