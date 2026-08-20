#!/usr/bin/env python3
"""Write the PDP fixture components to standalone HTML for browser QA.

The storefront cannot be reached from this environment, so viewport and
accessibility checks run against the real snippets and the real stylesheet
rendered into a local page. It is the components in isolation, not a replica of
the Shopify PDP - which is exactly what the layout, dialog and focus checks
need to look at.

Usage:
  python3 site/render-pdp-preview.py [OUT_DIR] [SCENARIO ...]

With no scenario names, every scenario in the fixture module is written.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import hivolt_pdp_fixtures as fx          # noqa: E402
import hivolt_pdp_render as R             # noqa: E402

DEFAULT_OUT = pathlib.Path("/tmp/hivolt-pdp-qa")


def main(argv):
    out = pathlib.Path(argv[0]) if argv else DEFAULT_OUT
    names = argv[1:] or list(fx.SCENARIOS)
    out.mkdir(parents=True, exist_ok=True)

    env = R.make_env()
    written = []
    for name in names:
        build = fx.SCENARIOS[name]
        html = R.preview_html(env, build(), title=f"HIVOLT PDP fixture - {name}")
        path = out / f"{name}.html"
        path.write_text(html)
        written.append(path)
        print(f"  {path}  {len(html):>6} bytes")

    print(f"\n{len(written)} scenario page(s) in {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
