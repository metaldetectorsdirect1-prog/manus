#!/usr/bin/env python3
"""Finish a Kindle eBook draft on Amazon KDP (Content + Pricing pages) and publish it.

Drives a real, headed Chromium window with a persistent profile so you log in
once and later runs reuse the session. Every book-specific value lives in
CONFIG below; the next title is a config change only.

Run (after scripts/kdp/setup.sh):
    cd ~/kdp-bot && source .venv/bin/activate && python publish.py

The script prints "LOGIN NEEDED" and waits when KDP asks for a password / OTP.
Type them in the Chrome window; nothing else needs a click.
"""
import os
import re
import sys
import time
import traceback

from playwright.sync_api import TimeoutError as PWTimeout, sync_playwright

CONFIG = {
    "title_id": "A2T39BZUARUGEZ",
    "title_name": "The Wife He Scheduled Around",
    "manuscript": os.path.expanduser("~/Downloads/the-wife-he-scheduled-around_digital.epub"),
    "cover": os.path.expanduser("~/Downloads/the-wife-he-scheduled-around_cover.jpg"),
    "publisher": "ORGANILAND FZCO",
    "isbn": "",  # leave blank
    "drm": "No",
    "ai_used": True,
    "ai_text_option": r"Entire work.*extensive",  # fallback: any option containing "extensive"
    "ai_images_option": r"^None",
    "ai_translations_option": r"^None",
    "kdp_select": True,
    "territories": "All territories",
    "primary_marketplace": "Amazon.com",
    "royalty": "70%",
    "list_price_usd": "2.99",
    "login_email": "support@kitchenusadirect.com",
    "bot_dir": os.path.expanduser("~/kdp-bot"),
    "login_wait_max_s": 600,
    "upload_wait_s": 300,
    "step_timeout_ms": 60_000,
}

BASE = "https://kdp.amazon.com/en_US"
CONTENT_URL = f"{BASE}/title-setup/kindle/{CONFIG['title_id']}/content"
PRICING_URL = f"{BASE}/title-setup/kindle/{CONFIG['title_id']}/pricing"
BOOKSHELF_URL = f"{BASE}/bookshelf"
SHOTS = os.path.join(CONFIG["bot_dir"], "shots")

REPORT = {
    "STATUS": "unknown", "TITLE ID": CONFIG["title_id"], "MANUSCRIPT": "not attempted",
    "COVER": "not attempted", "AI DISCLOSURE": "not set", "KDP SELECT": "not set",
    "PRICE": "not set", "SCREENSHOTS": SHOTS + "/", "DEVIATIONS": [],
}
_step_no = 0
page = None


class StepFailed(Exception):
    pass


def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def deviate(msg):
    REPORT["DEVIATIONS"].append(msg)
    log(f"DEVIATION: {msg}")


def shot(name):
    global _step_no
    _step_no += 1
    path = os.path.join(SHOTS, f"{_step_no:02d}_{name}.png")
    try:
        page.screenshot(path=path, full_page=True)
    except Exception:
        page.screenshot(path=path)
    log(f"screenshot -> {path}")
    return path


def visible_errors():
    texts = []
    for sel in ("[class*=error]", "[role=alert]", "[class*=alert]"):
        for el in page.locator(sel).all():
            try:
                if el.is_visible():
                    t = el.inner_text().strip()
                    if t and t not in texts:
                        texts.append(t)
            except Exception:
                pass
    return texts


def dump_dom(step, label):
    """Selector defeated twice: dump DOM, show 20 nearest lines around label, stop."""
    path = os.path.join(SHOTS, f"dom_{step}.html")
    html = page.content()
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(html)
    lines = html.splitlines()
    hit = next((i for i, ln in enumerate(lines) if label.lower() in ln.lower()), None)
    print(f"DOM dumped to {path}")
    if hit is None:
        print(f'Label "{label}" not found in DOM at all.')
    else:
        for ln in lines[max(0, hit - 10): hit + 10]:
            print(ln[:300])
    raise StepFailed(f'QUESTION: KDP layout defeated the selector for "{label}" at step {step}. '
                     f"See {path}. Which element should be used?")


def step(name, fn):
    log(f"STEP {name}")
    try:
        result = fn()
        shot(name)
        return result
    except StepFailed:
        shot(name + "_FAILED")
        raise
    except Exception as exc:
        shot(name + "_FAILED")
        print(f"FAILED at step {name}: {exc!r}")
        print(f"URL: {page.url}")
        errs = visible_errors()
        if errs:
            print("Visible error text:")
            for t in errs:
                print("  " + t)
        traceback.print_exc()
        raise StepFailed(name)


def try_selectors(label, candidates, action, step_name):
    """Run action(locator) on the first candidate that works. Two misses -> DOM dump."""
    misses = 0
    for loc in candidates:
        try:
            loc.first.wait_for(state="attached", timeout=8_000)
            action(loc.first)
            return True
        except Exception as exc:
            misses += 1
            log(f'selector miss for "{label}": {exc.__class__.__name__}')
            if misses >= 2 and loc is candidates[-1]:
                break
    dump_dom(step_name, label)


def click_choice(label_regex, step_name):
    """Select a radio/checkbox whose label matches label_regex (KDP uses label-wrapped inputs)."""
    rx = re.compile(label_regex, re.I)

    def do(loc):
        loc.scroll_into_view_if_needed()
        loc.click(timeout=CONFIG["step_timeout_ms"])

    def do_check(loc):
        loc.scroll_into_view_if_needed()
        loc.check(timeout=CONFIG["step_timeout_ms"], force=True)

    candidates = [page.get_by_label(rx), page.locator("label").filter(has_text=rx)]
    misses = 0
    for loc, act in ((candidates[0], do_check), (candidates[1], do)):
        try:
            loc.first.wait_for(state="attached", timeout=8_000)
            act(loc.first)
            return
        except Exception as exc:
            misses += 1
            log(f'choice miss for /{label_regex}/: {exc.__class__.__name__}')
    dump_dom(step_name, label_regex)


def select_option_matching(control, option_regex, fallback_regex=None):
    """For a <select> or a radio group inside `control`, choose the option matching regex."""
    rx = re.compile(option_regex, re.I)
    if control.evaluate("el => el.tagName.toLowerCase()") == "select":
        labels = control.locator("option").all_inner_texts()
        for rxx in (rx, re.compile(fallback_regex, re.I) if fallback_regex else None):
            if rxx is None:
                continue
            match = next((t for t in labels if rxx.search(t.strip())), None)
            if match:
                control.select_option(label=match.strip())
                return match.strip()
        raise StepFailed(f"no option matching {option_regex} in {labels}")
    radios = control.locator("label")
    texts = radios.all_inner_texts()
    for rxx in (rx, re.compile(fallback_regex, re.I) if fallback_regex else None):
        if rxx is None:
            continue
        for i, t in enumerate(texts):
            if rxx.search(t.strip()):
                radios.nth(i).click()
                return t.strip()
    raise StepFailed(f"no radio matching {option_regex} in {texts}")


def file_input_near(section_regex):
    """Hidden <input type=file> inside the section whose text matches section_regex."""
    rx = re.compile(section_regex, re.I)
    section = page.locator("section, fieldset, div").filter(has_text=rx).filter(
        has=page.locator("input[type=file]"))
    if section.count():
        return section.last.locator("input[type=file]").first
    return None


def upload(path, section_regex, button_regex, success_regex, step_name):
    inp = file_input_near(section_regex)
    if inp is not None:
        inp.set_input_files(path)
        log(f"set_input_files on hidden input near /{section_regex}/")
    else:
        deviate(f"no <input type=file> found near /{section_regex}/; used file chooser on button /{button_regex}/")
        with page.expect_file_chooser(timeout=CONFIG["step_timeout_ms"]) as fc:
            page.get_by_role("button", name=re.compile(button_regex, re.I)).first.click()
        fc.value.set_files(path)
    page.get_by_text(re.compile(success_regex, re.I)).first.wait_for(
        state="visible", timeout=CONFIG["upload_wait_s"] * 1000)
    log(f"upload confirmed: /{success_regex}/")


# ----------------------------------------------------------------- steps
def s05_open_content():
    page.goto(CONTENT_URL, wait_until="domcontentloaded")
    page.wait_for_timeout(3000)
    if re.search(r"signin|ap/|login", page.url, re.I) or page.locator("input[type=password]").count():
        print("LOGIN NEEDED — type password/OTP in the Chrome window", flush=True)
        try:
            em = page.locator("input[type=email], #ap_email")
            if em.count() and em.first.is_visible() and not em.first.input_value():
                em.first.fill(CONFIG["login_email"])
        except Exception:
            pass
        deadline = time.time() + CONFIG["login_wait_max_s"]
        while time.time() < deadline:
            if "title-setup" in page.url or "bookshelf" in page.url:
                break
            time.sleep(3)
        else:
            raise StepFailed("login not completed within the wait window")
        page.goto(CONTENT_URL, wait_until="domcontentloaded")
    page.get_by_text(re.compile(r"Manuscript", re.I)).first.wait_for(timeout=CONFIG["step_timeout_ms"])


def s06_drm():
    drm = page.locator("section, fieldset, div").filter(has_text=re.compile(r"Digital Rights Management|DRM", re.I))
    target = drm.last if drm.count() else page
    rx = re.compile(rf"^\s*{CONFIG['drm']}\b", re.I)
    lab = target.locator("label").filter(has_text=rx)
    if lab.count():
        lab.first.click()
    else:
        click_choice(rf"^\s*{CONFIG['drm']}\b", "06_drm")


def s07_manuscript():
    upload(CONFIG["manuscript"], r"Upload (eBook )?manuscript", r"Upload (eBook )?manuscript",
           r"Manuscript uploaded successfully|uploaded successfully", "07_manuscript")
    REPORT["MANUSCRIPT"] = "uploaded OK"


def s08_cover():
    click_choice(r"Upload a cover you already have", "08_cover_radio")
    page.wait_for_timeout(1500)
    upload(CONFIG["cover"], r"Upload your cover file|cover file", r"Upload your cover file|Upload",
           r"Cover uploaded successfully", "08_cover")
    REPORT["COVER"] = "uploaded OK"


def s09_ai():
    sec = page.locator("section, fieldset, div").filter(has_text=re.compile(r"AI-?generated content", re.I)).last
    yes_no = "Yes" if CONFIG["ai_used"] else "No"
    lab = sec.locator("label").filter(has_text=re.compile(rf"^\s*{yes_no}\b", re.I))
    if not lab.count():
        dump_dom("09_ai", "AI-generated content")
    lab.first.click()
    page.wait_for_timeout(1500)
    chosen = {}
    for key, opt, fb in (("Text", CONFIG["ai_text_option"], "extensive"),
                         ("Images", CONFIG["ai_images_option"], None),
                         ("Translations", CONFIG["ai_translations_option"], None)):
        block = sec.locator("div, fieldset").filter(has_text=re.compile(rf"^\s*{key}\b", re.I)).last
        ctl = block.locator("select")
        if ctl.count():
            chosen[key] = select_option_matching(ctl.first, opt, fb)
        else:
            chosen[key] = select_option_matching(block, opt, fb)
        log(f"AI {key}: {chosen[key]}")
    REPORT["AI DISCLOSURE"] = f"Yes; Text={chosen['Text']}; Images={chosen['Images']}; Translations={chosen['Translations']}"
    if not re.search(CONFIG["ai_text_option"], chosen["Text"], re.I):
        deviate(f'AI text option wording differed; chose "{chosen["Text"]}"')


def s10_previewer():
    btn = page.get_by_role("button", name=re.compile(r"Launch Previewer", re.I))
    link = page.get_by_role("link", name=re.compile(r"Launch Previewer", re.I))
    target = btn if btn.count() else (link if link.count() else None)
    if target is None:
        deviate("Launch Previewer control not present; skipped previewer")
        return
    try:
        with page.context.expect_page(timeout=15_000) as popup:
            target.first.click()
        prev = popup.value
        prev.wait_for_timeout(20_000)
        prev.screenshot(path=os.path.join(SHOTS, "10_previewer_popup.png"))
        prev.close()
    except PWTimeout:
        page.wait_for_timeout(20_000)
        shot("10_previewer_inline")
        if "content" not in page.url:
            page.goto(CONTENT_URL, wait_until="domcontentloaded")
    except Exception as exc:
        deviate(f"previewer errored ({exc.__class__.__name__}); skipped, not required to publish")
        if "content" not in page.url:
            page.goto(CONTENT_URL, wait_until="domcontentloaded")


def s11_isbn_publisher():
    pub = page.get_by_label(re.compile(r"^Publisher", re.I))
    if not pub.count():
        pub = page.locator("input[id*=publisher i], input[name*=publisher i]")
    if not pub.count():
        dump_dom("11_publisher", "Publisher")
    pub.first.fill(CONFIG["publisher"])
    if CONFIG["isbn"]:
        page.get_by_label(re.compile(r"ISBN", re.I)).first.fill(CONFIG["isbn"])


def s12_save_continue():
    page.get_by_role("button", name=re.compile(r"Save and Continue", re.I)).first.click()
    try:
        page.wait_for_url(re.compile(r"/pricing"), timeout=CONFIG["step_timeout_ms"])
    except PWTimeout:
        errs = visible_errors()
        print("Validation errors (verbatim):")
        for t in errs:
            print("  " + t)
        raise StepFailed("content page did not advance to pricing")


def s13_kdp_select():
    if CONFIG["kdp_select"]:
        click_choice(r"Enroll my book in KDP Select", "13_kdp_select")
        REPORT["KDP SELECT"] = "enrolled"
    else:
        REPORT["KDP SELECT"] = "not enrolled"


def s14_territories():
    click_choice(CONFIG["territories"], "14_territories")


def s15_primary_marketplace():
    sel = page.get_by_label(re.compile(r"Primary marketplace", re.I))
    if not sel.count():
        sel = page.locator("select[id*=marketplace i]")
    if not sel.count():
        dump_dom("15_marketplace", "Primary marketplace")
    sel.first.select_option(label=CONFIG["primary_marketplace"])


def s16_royalty_price():
    click_choice(rf"^\s*{re.escape(CONFIG['royalty'])}", "16_royalty")
    page.wait_for_timeout(1000)
    row = page.locator("tr, div").filter(has_text=re.compile(r"Amazon\.com\b")).filter(
        has=page.locator("input[type=text], input[type=number]"))
    if not row.count():
        dump_dom("16_price", "Amazon.com")
    box = row.first.locator("input[type=text], input[type=number]").first
    box.fill("")
    box.fill(CONFIG["list_price_usd"])
    box.press("Tab")
    page.wait_for_timeout(2000)
    REPORT["PRICE"] = f"USD {box.input_value()} on Amazon.com, {CONFIG['royalty']} royalty, other marketplaces auto-converted"


def s17_terms():
    click_choice(r"terms and conditions", "17_terms")


def s18_publish():
    page.get_by_role("button", name=re.compile(r"Publish Your Kindle eBook", re.I)).first.click()
    page.wait_for_timeout(3000)
    modal_ok = page.get_by_role("button", name=re.compile(r"^(OK|Continue|Confirm|Publish)$", re.I))
    if modal_ok.count() and modal_ok.first.is_visible():
        deviate("a confirmation / price-band dialog appeared; accepted the default")
        modal_ok.first.click()
    page.get_by_text(re.compile(r"being published|in review|Publishing", re.I)).first.wait_for(
        timeout=CONFIG["step_timeout_ms"])


def s19_bookshelf():
    page.goto(BOOKSHELF_URL, wait_until="domcontentloaded")
    page.wait_for_timeout(5000)
    card = page.locator("div, tr, li").filter(has_text=re.compile(re.escape(CONFIG["title_name"]), re.I))
    text = card.last.inner_text() if card.count() else ""
    m = re.search(r"(In Review|Publishing|Live|Draft|Blocked|Live with unpublished changes)", text, re.I)
    REPORT["STATUS"] = m.group(1) if m else (text.strip()[:120] or "title not found on bookshelf")


def print_report():
    print("\n" + "=" * 60)
    for key in ("STATUS", "TITLE ID", "MANUSCRIPT", "COVER", "AI DISCLOSURE", "KDP SELECT", "PRICE", "SCREENSHOTS"):
        print(f"{key}: {REPORT[key]}")
    dev = REPORT["DEVIATIONS"]
    print("DEVIATIONS: " + ("none" if not dev else "; ".join(dev)))
    print("=" * 60)


def main():
    global page
    for key in ("manuscript", "cover"):
        p = CONFIG[key]
        if not os.path.isfile(p):
            print(f"STOP: {key} file not found: {p}")
            os.system(f'ls -la "{os.path.dirname(p)}"')
            return 2
        log(f"{key}: {p} ({os.path.getsize(p)} bytes)")
    os.makedirs(SHOTS, exist_ok=True)
    with sync_playwright() as pw:
        ctx = pw.chromium.launch_persistent_context(
            user_data_dir=os.path.join(CONFIG["bot_dir"], "profile"), headless=False,
            channel="chromium", viewport={"width": 1400, "height": 1000}, slow_mo=150)
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        page.set_default_timeout(CONFIG["step_timeout_ms"])
        try:
            for name, fn in (("05_open_content", s05_open_content), ("06_drm", s06_drm),
                             ("07_manuscript", s07_manuscript), ("08_cover", s08_cover),
                             ("09_ai_disclosure", s09_ai), ("10_previewer", s10_previewer),
                             ("11_isbn_publisher", s11_isbn_publisher), ("12_save_continue", s12_save_continue),
                             ("13_kdp_select", s13_kdp_select), ("14_territories", s14_territories),
                             ("15_primary_marketplace", s15_primary_marketplace),
                             ("16_royalty_price", s16_royalty_price), ("17_terms", s17_terms),
                             ("18_publish", s18_publish), ("19_bookshelf", s19_bookshelf)):
                step(name, fn)
        except StepFailed as exc:
            print(f"STOPPED: {exc}")
            print_report()
            return 1
        finally:
            ctx.close()
    print_report()
    return 0


if __name__ == "__main__":
    sys.exit(main())
