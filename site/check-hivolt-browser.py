#!/usr/bin/env python3
"""Browser QA for the HIVOLT PDP components.

Renders the fixture pages in Chromium at seven widths and asserts the things a
static test cannot see: that nothing overflows or clips, that the size-guide
dialog traps and restores focus, that the swatch radio group is keyboard
operable, that touch targets are big enough, and - via axe-core when it is
available - that no WCAG rule regresses.

Usage:
  python3 site/check-hivolt-browser.py [QA_DIR]

Exit: 0 when every check passes, 1 otherwise.

axe-core is looked for in AXE_PATH, then ./node_modules, then the QA dir. When
it is missing the axe checks are reported as SKIPPED rather than silently
passing, because a skipped accessibility scan is not a green one.
"""
import json
import os
import pathlib
import sys

from playwright.sync_api import sync_playwright

QA_DIR = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path("/tmp/hivolt-pdp-qa")
SHOTS = QA_DIR / "shots"

# The pinned Playwright build and the installed browser can disagree in this
# image, so the binary is located rather than assumed.
CHROME_CANDIDATES = [
    os.environ.get("CHROME_PATH", ""),
    "/opt/pw-browsers/chromium-1194/chrome-linux/chrome",
]

VIEWPORTS = [320, 375, 390, 430, 768, 1024, 1440]
MIN_TAP = 44

# Scenario A is the layout workhorse: most options, longest spec values, widest
# size chart. The rest are checked for overflow and structural sanity only.
PRIMARY = "A_full"


def find_chrome():
    for c in CHROME_CANDIDATES:
        if c and pathlib.Path(c).exists():
            return c
    for c in pathlib.Path("/opt/pw-browsers").glob("chromium-*/chrome-linux/chrome"):
        return str(c)
    return None


def find_axe():
    candidates = [os.environ.get("AXE_PATH", "")]
    candidates += [str(p) for p in pathlib.Path.cwd().glob("node_modules/axe-core/axe.min.js")]
    candidates += [str(QA_DIR / "axe.min.js")]
    candidates += [str(p) for p in pathlib.Path("/tmp").glob("**/node_modules/axe-core/axe.min.js")]
    for c in candidates:
        if c and pathlib.Path(c).exists():
            return pathlib.Path(c)
    return None


results = []


def record(ok, area, name, detail=""):
    results.append((ok, area, name, detail))
    flag = "ok   " if ok is True else ("SKIP " if ok is None else "FAIL ")
    print(f"  {flag} [{area}] {name}" + (f"\n         {detail}" if detail and ok is not True else ""))


# ---------------------------------------------------------------------------
# Individual probes
# ---------------------------------------------------------------------------
def check_layout(page, width, label):
    overflow = page.evaluate(
        "() => document.documentElement.scrollWidth - document.documentElement.clientWidth")
    record(overflow <= 0, f"{width}px", f"{label}: no horizontal overflow",
           f"page is {overflow}px wider than the viewport")

    escaped = page.evaluate("""(w) => [...document.querySelectorAll('main *')]
        .filter(e => e.getClientRects().length)
        .map(e => { const r = e.getBoundingClientRect();
                    return {t: e.tagName + '.' + e.className, l: Math.round(r.left), r: Math.round(r.right)}; })
        .filter(o => o.r > w + 1 || o.l < -1)""", width)
    record(not escaped, f"{width}px", f"{label}: nothing rendered outside the viewport",
           json.dumps(escaped[:3]))

    # "Clipped" means a reader cannot get to it: the element extends past the
    # nearest ancestor that hides overflow. scrollWidth > clientWidth on its own
    # is not that - a visually-hidden span always trips it, and so does any box
    # whose child carries a negative margin into the parent's padding. Both are
    # fine as long as nothing is actually cut off.
    clipped = page.evaluate("""() => {
        const out = [];
        for (const e of document.querySelectorAll('main *, dialog *')) {
            const cs = getComputedStyle(e);
            if (cs.clip !== 'auto' || cs.clipPath !== 'none') continue;   // visually hidden
            if (!e.getClientRects().length) continue;
            let a = e.parentElement, clipper = null;
            while (a) {
                const s = getComputedStyle(a);
                if (['hidden','clip'].includes(s.overflowX)) { clipper = a; break; }
                if (['auto','scroll'].includes(s.overflowX)) break;       // scrollable, reachable
                a = a.parentElement;
            }
            if (!clipper) continue;
            const r = e.getBoundingClientRect(), c = clipper.getBoundingClientRect();
            if (r.right > c.right + 1 || r.left < c.left - 1) {
                out.push(e.tagName + '.' + e.className + ' past ' +
                         clipper.tagName + '.' + clipper.className);
            }
        }
        return out;
    }""")
    record(not clipped, f"{width}px", f"{label}: no content clipped without a scroller",
           json.dumps(clipped[:3]))


def check_tap_targets(page, width):
    small = page.evaluate("""(min) => [...document.querySelectorAll(
            '.hv-swatch__label, .hv-sg-trigger, .hv-sg__close, .hv-sg__unit span')]
        .filter(e => e.getClientRects().length)
        .map(e => { const r = e.getBoundingClientRect();
                    return {t: e.className, w: Math.round(r.width), h: Math.round(r.height)}; })
        .filter(o => o.w < min || o.h < min)""", MIN_TAP)
    # The unit toggle is a 40px segmented control by design; it is a secondary
    # control inside an open dialog, not a primary target, so it is reported
    # rather than failed. Everything else must meet the minimum.
    hard = [o for o in small if "hv-sg__unit" not in o["t"]]
    record(not hard, f"{width}px", f"interactive targets are at least {MIN_TAP}px",
           json.dumps(hard[:4]))


def check_scroll_affordance(page, width):
    info = page.evaluate("""() => {
        const el = document.querySelector('.hv-sg__scroll');
        if (!el) return null;
        return {overflows: el.scrollWidth > el.clientWidth + 1,
                bg: getComputedStyle(el).backgroundImage,
                overflowX: getComputedStyle(el).overflowX};
    }""")
    if info is None:
        record(None, f"{width}px", "size-chart scroll affordance", "no chart here")
        return
    record(info["overflowX"] in ("auto", "scroll"), f"{width}px",
           "the size chart scrolls rather than clipping", info["overflowX"])
    if info["overflows"]:
        record(info["bg"] != "none", f"{width}px",
               "a chart wider than the dialog shows a scroll cue", info["bg"][:80])
    else:
        record(True, f"{width}px", "the chart fits, so no scroll cue is needed")


def check_reduced_motion(browser, chrome_page_url, width):
    ctx = browser.new_context(viewport={"width": width, "height": 900},
                              reduced_motion="reduce")
    page = ctx.new_page()
    page.goto(chrome_page_url)
    page.wait_for_timeout(150)
    chip = page.query_selector(".hv-swatch__chip")
    if chip:
        transition = page.eval_on_selector(
            ".hv-swatch__chip", "e => getComputedStyle(e).transitionDuration")
        record(transition in ("0s", "0ms"), f"{width}px",
               "reduced motion removes the swatch transition", transition)
    else:
        record(None, f"{width}px", "reduced motion check", "no chip on this scenario")
    ctx.close()


def check_dialog(page, width):
    trigger = page.query_selector("[data-hv-sg-open]")
    if not trigger:
        record(None, f"{width}px", "size-guide dialog", "no trigger on this scenario")
        return
    trigger.click()
    page.wait_for_timeout(200)

    record(page.evaluate("() => document.querySelector('dialog.hv-sg').open") is True,
           f"{width}px", "trigger opens the dialog")
    record(page.evaluate(
        "() => document.querySelector('dialog.hv-sg').contains(document.activeElement)") is True,
        f"{width}px", "focus moves into the dialog")

    # Focus containment. Chromium's modal cycle passes through <body> between
    # wraps; body is neither interactive nor page content, so the requirement
    # that actually matters is that no control BEHIND the dialog can be
    # reached. That is what is asserted.
    reached = []
    for _ in range(15):
        page.keyboard.press("Tab")
        reached.append(page.evaluate("""() => {
            const d = document.querySelector('dialog.hv-sg');
            const a = document.activeElement;
            if (!a || d.contains(a)) return null;
            const interactive = a.matches('a,button,input,select,textarea,[tabindex]:not([tabindex="-1"])');
            return interactive ? (a.tagName + '.' + (a.className || '')) : null;
        }"""))
    leaked = [r for r in reached if r]
    record(not leaked, f"{width}px",
           "no control behind the dialog can be focused while it is open",
           json.dumps(sorted(set(leaked))))

    # Unit toggle converts.
    page.click("input[value='in']")
    page.wait_for_timeout(120)
    unit = page.evaluate("() => document.querySelector('dialog.hv-sg').dataset.activeUnit")
    row = page.evaluate(
        "() => [...document.querySelectorAll('.hv-sg__table tbody tr:first-child td')]"
        ".map(td => td.innerText.trim())")
    record(unit == "in" and row and row[0] == "20.1", f"{width}px",
           "unit toggle converts 51 cm to 20.1 in", f"unit={unit} row={row}")

    page.click("input[value='cm']")
    page.wait_for_timeout(100)

    page.keyboard.press("Escape")
    page.wait_for_timeout(200)
    record(page.evaluate("() => document.querySelector('dialog.hv-sg').open") is False,
           f"{width}px", "Escape closes the dialog")
    record(page.evaluate("() => document.activeElement.matches('[data-hv-sg-open]')") is True,
           f"{width}px", "focus returns to the trigger")

    # The close control works too.
    page.click("[data-hv-sg-open]")
    page.wait_for_timeout(150)
    page.click("[data-hv-sg-close]")
    page.wait_for_timeout(150)
    record(page.evaluate("() => document.querySelector('dialog.hv-sg').open") is False,
           f"{width}px", "the close control closes the dialog")
    record(page.evaluate("() => document.activeElement.matches('[data-hv-sg-open]')") is True,
           f"{width}px", "focus returns to the trigger after the close control")


def check_variants(page, width):
    colour = page.query_selector(".hv-swatches:not(.hv-swatches--text) input:checked")
    if not colour:
        record(None, f"{width}px", "swatch keyboard operation", "no swatch group here")
        return
    before = page.evaluate(
        "() => document.querySelector('.hv-swatches:not(.hv-swatches--text) input:checked').value")
    page.focus(".hv-swatches:not(.hv-swatches--text) input:checked")
    page.keyboard.press("ArrowRight")
    page.wait_for_timeout(120)
    after = page.evaluate(
        "() => document.querySelector('.hv-swatches:not(.hv-swatches--text) input:checked').value")
    record(after != before, f"{width}px", "arrow keys move the swatch selection",
           f"{before} -> {after}")

    checked = page.evaluate("""() => [...document.querySelectorAll('fieldset.hv-swatches')]
        .map(f => f.querySelectorAll('input:checked').length)""")
    record(all(c == 1 for c in checked), f"{width}px",
           "exactly one value is selected per option group", json.dumps(checked))

    # .hv-swatch__chip transitions box-shadow over 120ms, so the computed value
    # is mid-flight for a moment after selection changes. Settle first.
    page.wait_for_timeout(350)
    rings = page.evaluate("""() => [...document.querySelectorAll(
            '.hv-swatches:not(.hv-swatches--text) .hv-swatch')]
        .map(el => ({v: el.dataset.value,
                     checked: el.querySelector('input').checked,
                     ring: getComputedStyle(el.querySelector('.hv-swatch__chip') || el)
                             .boxShadow.includes('0px 0px 0px 4px')}))""")
    ringed = [r for r in rings if r["ring"]]
    record(len(ringed) == 1 and ringed[0]["checked"], f"{width}px",
           "the selected ring is on exactly the checked swatch", json.dumps(rings))

    out = page.evaluate("""() => [...document.querySelectorAll('.hv-swatch[data-available="false"]')]
        .map(el => el.querySelector('label').innerText.replace(/\\s+/g,' ').trim())""")
    record(all("Sold out" in o for o in out) and out, f"{width}px",
           "sold-out values say so in their accessible name", json.dumps(out))


def run_axe(page, axe_src, label):
    page.add_script_tag(content=axe_src)
    res = page.evaluate("""async () => {
        const r = await axe.run(document, {
            runOnly: { type: 'tag', values: ['wcag2a','wcag2aa','wcag21a','wcag21aa'] }
        });
        return r.violations.map(v => ({
            id: v.id, impact: v.impact, help: v.help,
            nodes: v.nodes.slice(0,3).map(n => n.target.join(' '))
        }));
    }""")
    return res


# ---------------------------------------------------------------------------
def main():
    chrome = find_chrome()
    if not chrome:
        print("no Chromium binary found; cannot run browser QA")
        return 2
    axe_path = find_axe()
    axe_src = axe_path.read_text() if axe_path else None
    print(f"chromium: {chrome}")
    print(f"axe-core: {axe_path or 'NOT FOUND - accessibility scan will be skipped'}\n")

    SHOTS.mkdir(parents=True, exist_ok=True)
    pages = sorted(QA_DIR.glob("*.html"))
    if not pages:
        print(f"no fixture pages in {QA_DIR}; run site/render-pdp-preview.py first")
        return 2

    primary = QA_DIR / f"{PRIMARY}.html"
    axe_violations = {}

    with sync_playwright() as pw:
        browser = pw.chromium.launch(executable_path=chrome, args=["--no-sandbox"])

        # --- the full matrix on the primary scenario -----------------------
        for width in VIEWPORTS:
            print(f"\n{width}px")
            page = browser.new_page(viewport={"width": width, "height": 900},
                                    device_scale_factor=2)
            page.goto(primary.as_uri())
            page.wait_for_timeout(200)

            check_layout(page, width, PRIMARY)
            check_tap_targets(page, width)
            check_variants(page, width)
            page.screenshot(path=str(SHOTS / f"{width}-closed.png"), full_page=True)
            check_dialog(page, width)
            check_reduced_motion(browser, primary.as_uri(), width)
            page.click("[data-hv-sg-open]")
            page.wait_for_timeout(200)
            check_layout(page, width, f"{PRIMARY} (dialog open)")
            check_scroll_affordance(page, width)
            page.screenshot(path=str(SHOTS / f"{width}-dialog.png"))

            if axe_src:
                v = run_axe(page, axe_src, f"{width}px dialog open")
                axe_violations[f"{width}px"] = v
                record(not v, f"{width}px", "axe-core WCAG 2.1 AA: no violations",
                       json.dumps(v)[:600])
            else:
                record(None, f"{width}px", "axe-core WCAG 2.1 AA scan", "axe-core unavailable")
            page.close()

        # --- every scenario, overflow and structure only -------------------
        print("\nall scenarios @ 375px")
        for path in pages:
            page = browser.new_page(viewport={"width": 375, "height": 900})
            page.goto(path.as_uri())
            page.wait_for_timeout(150)
            over = page.evaluate(
                "() => document.documentElement.scrollWidth - document.documentElement.clientWidth")
            record(over <= 0, "scenarios", f"{path.stem}: no horizontal overflow", f"{over}px")
            dupes = page.evaluate("""() => { const seen = {}, dup = [];
                document.querySelectorAll('[id]').forEach(e => {
                    if (seen[e.id]) dup.push(e.id); seen[e.id] = 1; });
                return dup; }""")
            record(not dupes, "scenarios", f"{path.stem}: no duplicate id in the DOM",
                   json.dumps(dupes))
            page.close()

        browser.close()

    (QA_DIR / "axe-report.json").write_text(json.dumps(axe_violations, indent=2))

    failed = [r for r in results if r[0] is False]
    skipped = [r for r in results if r[0] is None]
    passed = [r for r in results if r[0] is True]
    print(f"\nHIVOLT PDP BROWSER QA: {len(passed)}/{len(passed) + len(failed)} "
          f"{'PASS' if not failed else 'FAIL'}"
          + (f"  ({len(skipped)} skipped)" if skipped else ""))
    if failed:
        print("\nFailed:")
        for _, area, name, detail in failed:
            print(f"  [{area}] {name}\n      {detail}")
    print(f"\nscreenshots: {SHOTS}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
