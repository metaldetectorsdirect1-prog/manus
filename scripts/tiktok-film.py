"""Render a cinematic vertical brand film for HIVOLT, frame by frame, locally.

Why this exists rather than an AI video call: every Higgsfield CDN host is
blocked by this environment's egress proxy, so a generated clip can never be
opened and checked from here. Publishing an unverifiable moving picture of a
garment a customer can buy is not a trade worth making. Everything below is
rendered locally, which means any frame can be opened and looked at, and it
carries no AI-generated label — so it takes none of the distribution penalty
TikTok applies to disclosed AIGC.

The film is typographic because cdn.shopify.com is blocked too, so product
photography cannot be pulled in. That constraint suits the brand: the whole
proposition is a published number, and a number is what the film is about.

Animation is a pure function of time. Nothing uses CSS transitions or
requestAnimationFrame, because a screenshot has to be able to land on an exact
moment and get the same pixels every run.

    python3 scripts/tiktok-film.py            # 12s, 24fps, 1080x1920
"""
import math
import pathlib
import subprocess
import sys

import imageio_ffmpeg
from playwright.sync_api import sync_playwright

W, H, FPS, DUR = 1080, 1920, 24, 12.0
OUT = pathlib.Path("/tmp/claude-0/-home-user-manus/"
                   "f9f720c1-823b-5cd8-aec8-e4501793ee60/scratchpad/film")

# Real figures, from the live product page for the ankle-length leggings.
GSM, COMP, PRICE = 230, "89% polyester · 11% spandex", "$54"

HTML = r"""<!doctype html><meta charset="utf-8"><style>
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;background:#08090B;overflow:hidden}
body{font-family:"DejaVu Sans","Liberation Sans",Arial,sans-serif;color:#F2F4F7}
.stage{position:absolute;inset:0}
/* Every reveal is a slab of type sliding up inside a clipped box — one motion
   used consistently, so the film reads as designed rather than assembled. */
.mask{overflow:hidden;position:absolute;left:96px;right:150px}
.mask .in{display:block;will-change:transform}
.line{font-size:76px;line-height:1.14;letter-spacing:-.025em;font-weight:700}
.line.dim{color:#8A97AB;font-weight:400}
.accent{color:#6E9BFF}
.num{
  font-family:"DejaVu Sans Mono","Liberation Mono",monospace;
  font-size:340px;line-height:.92;letter-spacing:-.06em;font-weight:700;color:#6E9BFF;
}
.unit{
  font-family:"DejaVu Sans Mono","Liberation Mono",monospace;
  font-size:92px;letter-spacing:0;color:#F2F4F7;
}
.meta{
  font-family:"DejaVu Sans Mono","Liberation Mono",monospace;
  font-size:34px;letter-spacing:.05em;color:#9AA6B8;
}
.rule{position:absolute;height:3px;background:#1F4FD8;left:96px}
.wordmark{
  font-size:118px;letter-spacing:.16em;font-weight:700;
}
.url{
  font-family:"DejaVu Sans Mono","Liberation Mono",monospace;
  font-size:34px;letter-spacing:.18em;color:#6E9BFF;text-transform:uppercase;
}
.vig{position:absolute;inset:0;pointer-events:none;
  background:radial-gradient(120% 75% at 50% 45%,rgba(0,0,0,0) 40%,rgba(0,0,0,.55) 100%)}
</style>
<div class="stage" id="stage"></div>
<div class="vig"></div>
<script>
const W=1080,H=1920;
const clamp=(x,a,b)=>Math.max(a,Math.min(b,x));
// easeOutQuint — a fast departure settling slowly, which is what makes a type
// slab feel weighted rather than linear.
const eo=t=>1-Math.pow(1-clamp(t,0,1),5);
const eio=t=>{t=clamp(t,0,1);return t<.5?4*t*t*t:1-Math.pow(-2*t+2,3)/2};
// progress of a beat starting at `s`, lasting `d`
const p=(t,s,d)=>clamp((t-s)/d,0,1);

function slab(html,cls,top,prog,size){
  const h=(size||120);
  return `<div class="mask" style="top:${top}px;height:${h}px">
    <span class="in ${cls}" style="transform:translateY(${(1-eo(prog))*h}px)">${html}</span></div>`;
}

function render(t){
  let s="";
  // ── beat 1: the setup ────────────────────────────────────────────────
  const b1=p(t,0.25,0.9), b1o=1-p(t,3.3,0.5);
  if(b1o>0){
    s+=`<div style="opacity:${b1o}">`;
    s+=slab("Every activewear brand","line",620,b1,100);
    s+=slab("knows this number.","line",720,p(t,0.45,0.9),100);
    s+=`<div class="rule" style="top:880px;width:${eo(p(t,0.9,1.0))*(W-246)}px"></div>`;
    s+=`</div>`;
  }
  // ── beat 2: the turn ─────────────────────────────────────────────────
  const b2o=(1-p(t,6.0,0.45))*p(t,3.5,0.01);
  if(b2o>0){
    s+=`<div style="opacity:${b2o}">`;
    s+=slab("Almost none of them","line dim",640,p(t,3.6,0.9),100);
    s+=slab('<span class="accent">print it.</span>',"line",740,p(t,3.85,0.9),100);
    s+=`</div>`;
  }
  // ── beat 3: the number ───────────────────────────────────────────────
  const b3=p(t,6.15,1.5), b3o=p(t,6.15,0.35)*(1-p(t,10.6,0.5));
  if(b3o>0){
    const shown=Math.round(eio(b3)*230);
    s+=`<div style="opacity:${b3o}">`;
    s+=`<div class="mask" style="top:560px;height:360px">
          <span class="in num" style="transform:translateY(${(1-eo(p(t,6.15,0.8)))*360}px)">
          ${String(shown).padStart(3,'0')}</span></div>`;
    s+=slab("g/m&#178;","unit",930,p(t,7.5,0.7),120);
    s+=`<div class="rule" style="top:1090px;width:${eo(p(t,7.9,0.9))*(W-246)}px"></div>`;
    s+=slab("%COMP%","meta",1140,p(t,8.25,0.7),60);
    s+=slab("%PRICE% &#183; free US shipping","meta",1205,p(t,8.5,0.7),60);
    s+=`</div>`;
  }
  // ── beat 4: the sign-off ─────────────────────────────────────────────
  const b4o=p(t,10.7,0.4);
  if(b4o>0){
    s+=`<div style="opacity:${b4o}">`;
    s+=slab("HIVOLT","wordmark",760,p(t,10.75,0.8),150);
    s+=slab("Published, not claimed","meta",930,p(t,11.05,0.8),60);
    s+=slab("hivolt-usa.com/tiktok","url",1010,p(t,11.25,0.8),60);
    s+=`</div>`;
  }
  document.getElementById('stage').innerHTML=s;
}
</script>"""


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for f in OUT.glob("f_*.png"):
        f.unlink()

    html = HTML.replace("%COMP%", COMP).replace("%PRICE%", PRICE)
    page_file = OUT / "film.html"
    page_file.write_text(html)

    total = int(DUR * FPS)
    print(f"rendering {total} frames at {W}x{H}, {FPS}fps")

    # This image ships Chromium 1194; the installed Playwright pins a newer
    # build and would otherwise try to download one. Pointing at the binary
    # that is already here avoids that — `playwright install` must not run.
    chrome = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
    with sync_playwright() as pw:
        browser = pw.chromium.launch(
            executable_path=chrome, args=["--no-sandbox", "--disable-gpu"])
        page = browser.new_page(viewport={"width": W, "height": H})
        page.goto(f"file://{page_file}")
        for i in range(total):
            page.evaluate(f"render({i / FPS})")
            page.screenshot(path=str(OUT / f"f_{i:04d}.png"))
            if i % 48 == 0:
                print(f"  frame {i}/{total}")
        browser.close()

    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    mp4 = OUT / "hivolt-230.mp4"
    subprocess.run([
        ffmpeg, "-y", "-framerate", str(FPS),
        "-i", str(OUT / "f_%04d.png"),
        # yuv420p and even dimensions, or the file plays on desktop and fails
        # silently on a phone.
        "-c:v", "libx264", "-preset", "slow", "-crf", "18",
        "-pix_fmt", "yuv420p", "-movflags", "+faststart",
        str(mp4),
    ], check=True, capture_output=True)

    kb = mp4.stat().st_size // 1024
    print(f"\nwrote {mp4}  ({kb} KB, {DUR:.0f}s)")
    return mp4


if __name__ == "__main__":
    main()
