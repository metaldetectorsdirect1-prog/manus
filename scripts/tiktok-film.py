"""Render cinematic vertical brand films for HIVOLT, frame by frame, locally.

Why local rather than an AI video call: every Higgsfield CDN host is blocked by
this environment's egress proxy, so a generated clip can never be opened and
checked from here. Publishing an unverifiable moving picture of a garment a
customer can buy is not a trade worth making. Everything below renders locally,
so any frame can be opened and looked at, and it carries no AI-generated label —
avoiding the distribution penalty TikTok applies to disclosed AIGC.

The films are typographic because cdn.shopify.com is blocked too, so product
photography cannot be pulled in. That constraint suits the brand: the whole
proposition is a published number.

Timing follows the aesthetic rules in .claude/skills/video-shotcraft:
  R1  key information holds still >=1s after it lands; the wordmark holds a
      full second, settled, before the film ends.
  R2  speed comes from acceleration, never constant velocity; grouped elements
      stagger and tighten, then rest.
  R3  slower is better — a first cut is almost always too fast, so main arcs
      run >=3s and every beat carries a deliberate hold.
  Q3  the camera stays steady. A slow scale push, no handheld shake.

Animation is a pure function of time. Nothing uses CSS transitions or
requestAnimationFrame, because a screenshot has to land on an exact moment and
produce identical pixels on a re-run.

    python3 scripts/tiktok-film.py            # renders every film
    python3 scripts/tiktok-film.py spec       # renders one
"""
import json
import pathlib
import subprocess
import sys

import imageio_ffmpeg
from playwright.sync_api import sync_playwright

W, H, FPS = 1080, 1920, 24
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
OUT = pathlib.Path("/tmp/claude-0/-home-user-manus/"
                   "f9f720c1-823b-5cd8-aec8-e4501793ee60/scratchpad/film")

# ── films ────────────────────────────────────────────────────────────────
# Every figure below is published on the corresponding HIVOLT product page.
# A beat is (start, end); elements inside it carry their own offset from the
# beat start. Beats overlap by design — the outgoing one fades while the next
# is already rising.

SIGNOFF = [
    {"k": "slab", "at": 0.00, "cls": "wordmark", "h": 160, "t": "HIVOLT"},
    {"k": "slab", "at": 0.35, "cls": "meta", "h": 62, "top": 170,
     "t": "Published, not claimed"},
    {"k": "slab", "at": 0.55, "cls": "url", "h": 62, "top": 250,
     "t": "hivolt-usa.com/tiktok"},
]

# Every line below is written to sit on ONE line at 72px inside an 834px
# column — roughly 20 characters. Longer copy is not a style choice here, it
# is the bug that clipped "So are most of the ones" down to "the".
FILMS = {
    # ── the number nobody prints ────────────────────────────────────────
    "spec": {
        "dur": 15.5,
        "beats": [
            {"in": 0.3, "out": 4.4, "top": 620, "els": [
                {"k": "slab", "at": 0.0, "cls": "line", "h": 100,
                 "t": "Every brand knows"},
                {"k": "slab", "at": 0.3, "cls": "line", "h": 100, "top": 100,
                 "t": "this number."},
                {"k": "rule", "at": 0.9, "top": 226, "d": 1.1},
            ]},
            {"in": 4.6, "out": 7.9, "top": 640, "els": [
                {"k": "slab", "at": 0.0, "cls": "line dim", "h": 100,
                 "t": "Almost none"},
                {"k": "slab", "at": 0.3, "cls": "line", "h": 100, "top": 100,
                 "t": '<span class="accent">of them print it.</span>'},
            ]},
            {"in": 8.1, "out": 13.3, "top": 520, "els": [
                {"k": "count", "at": 0.0, "to": 230, "d": 2.0, "h": 370},
                {"k": "slab", "at": 1.9, "cls": "unit", "h": 126, "top": 372,
                 "t": "g/m&#178;"},
                {"k": "rule", "at": 2.4, "top": 530, "d": 0.9},
                {"k": "slab", "at": 2.75, "cls": "meta", "h": 62, "top": 580,
                 "t": "89% polyester &#183; 11% spandex"},
                {"k": "slab", "at": 2.95, "cls": "meta", "h": 62, "top": 650,
                 "t": "$59 &#183; free US shipping"},
            ]},
            {"in": 13.4, "out": 15.5, "top": 760, "els": SIGNOFF},
        ],
    },

    # ── three weights, one price ────────────────────────────────────────
    "weights": {
        "dur": 16.0,
        "beats": [
            {"in": 0.3, "out": 4.2, "top": 640, "els": [
                {"k": "slab", "at": 0.0, "cls": "line", "h": 100,
                 "t": "Three pairs."},
                {"k": "slab", "at": 0.35, "cls": "line dim", "h": 100,
                 "top": 100, "t": "Three prices."},
                {"k": "rule", "at": 0.95, "top": 226, "d": 1.1},
            ]},
            # R2: the three weights land in a tightening rhythm, then rest.
            # 170px apart — at 140 they read as one block, not three choices.
            {"in": 4.4, "out": 11.6, "top": 450, "els": [
                {"k": "slab", "at": 0.0, "cls": "meta", "h": 60,
                 "t": "WEIGHT &#183; PRICE"},
                {"k": "row", "at": 0.5, "top": 120, "l": "220 g/m&#178;",
                 "r": "$54 &#183; lightest, breathes"},
                {"k": "row", "at": 1.35, "top": 290, "l": "250 g/m&#178;",
                 "r": "$64 &#183; middle"},
                {"k": "row", "at": 2.0, "top": 460, "l": "270 g/m&#178;",
                 "r": "$69 &#183; most opaque"},
                {"k": "slab", "at": 3.4, "cls": "line", "h": 100, "top": 640,
                 "t": "The number"},
                {"k": "slab", "at": 3.6, "cls": "line", "h": 100, "top": 740,
                 "t": '<span class="accent">sets the price.</span>'},
            ]},
            {"in": 11.8, "out": 13.8, "top": 640, "els": [
                {"k": "slab", "at": 0.0, "cls": "line dim", "h": 100,
                 "t": "Nobody else"},
                {"k": "slab", "at": 0.3, "cls": "line", "h": 100, "top": 100,
                 "t": "prints it."},
            ]},
            {"in": 13.9, "out": 16.0, "top": 760, "els": SIGNOFF},
        ],
    },

    # ── the honest teardown ─────────────────────────────────────────────
    "factory": {
        "dur": 16.5,
        "beats": [
            {"in": 0.3, "out": 4.0, "top": 660, "els": [
                {"k": "slab", "at": 0.0, "cls": "line", "h": 100,
                 "t": "We don't own"},
                {"k": "slab", "at": 0.3, "cls": "line", "h": 100, "top": 100,
                 "t": "a factory."},
                {"k": "rule", "at": 0.95, "top": 226, "d": 1.1},
            ]},
            {"in": 4.2, "out": 7.8, "top": 580, "els": [
                {"k": "slab", "at": 0.0, "cls": "line dim", "h": 100,
                 "t": "These are blanks."},
                {"k": "slab", "at": 1.5, "cls": "line", "h": 100, "top": 160,
                 "t": "So are most of"},
                {"k": "slab", "at": 1.7, "cls": "line", "h": 100, "top": 260,
                 "t": '<span class="accent">the ones you own.</span>'},
            ]},
            {"in": 8.0, "out": 11.6, "top": 600, "els": [
                {"k": "slab", "at": 0.0, "cls": "line", "h": 100,
                 "t": "We just publish"},
                {"k": "slab", "at": 0.3, "cls": "line", "h": 100, "top": 100,
                 "t": '<span class="accent">the spec.</span>'},
                {"k": "rule", "at": 1.1, "top": 236, "d": 0.9},
                {"k": "slab", "at": 1.5, "cls": "meta", "h": 62, "top": 286,
                 "t": "Composition &#183; weight &#183; every product"},
            ]},
            {"in": 11.8, "out": 14.6, "top": 620, "els": [
                {"k": "slab", "at": 0.0, "cls": "line dim", "h": 100,
                 "t": "No logo on it."},
                {"k": "slab", "at": 0.4, "cls": "line", "h": 100, "top": 130,
                 "t": "You're buying"},
                {"k": "slab", "at": 0.6, "cls": "line", "h": 100, "top": 230,
                 "t": '<span class="accent">the fabric.</span>'},
            ]},
            {"in": 14.8, "out": 16.5, "top": 760, "els": SIGNOFF},
        ],
    },

    # ── the return policy as a claim about the product ──────────────────
    "returns": {
        "dur": 15.5,
        "beats": [
            {"in": 0.3, "out": 4.0, "top": 660, "els": [
                {"k": "slab", "at": 0.0, "cls": "line", "h": 100,
                 "t": "Sixty days."},
                {"k": "slab", "at": 0.35, "cls": "line dim", "h": 100,
                 "top": 100, "t": "Worn and washed."},
                {"k": "rule", "at": 0.95, "top": 226, "d": 1.1},
            ]},
            {"in": 4.2, "out": 8.0, "top": 580, "els": [
                {"k": "slab", "at": 0.0, "cls": "line dim", "h": 100,
                 "t": "Train in them."},
                {"k": "slab", "at": 0.3, "cls": "line dim", "h": 100,
                 "top": 100, "t": "Wash them."},
                {"k": "slab", "at": 1.4, "cls": "line", "h": 100, "top": 240,
                 "t": '<span class="accent">Send them back.</span>'},
                {"k": "rule", "at": 2.1, "top": 372, "d": 0.9},
                {"k": "slab", "at": 2.5, "cls": "meta", "h": 62, "top": 420,
                 "t": "Free prepaid US label"},
                {"k": "slab", "at": 2.7, "cls": "meta", "h": 62, "top": 480,
                 "t": "No restocking fee"},
            ]},
            {"in": 8.2, "out": 11.6, "top": 600, "els": [
                {"k": "slab", "at": 0.0, "cls": "line dim", "h": 100,
                 "t": "You can't judge"},
                {"k": "slab", "at": 0.3, "cls": "line dim", "h": 100,
                 "top": 100, "t": "leggings in a shop."},
                {"k": "slab", "at": 1.5, "cls": "line", "h": 100, "top": 240,
                 "t": "You judge them"},
                {"k": "slab", "at": 1.7, "cls": "line", "h": 100, "top": 340,
                 "t": '<span class="accent">in a squat.</span>'},
            ]},
            {"in": 11.8, "out": 13.6, "top": 660, "els": [
                {"k": "slab", "at": 0.0, "cls": "line dim", "h": 100,
                 "t": "Not generosity."},
                {"k": "slab", "at": 0.35, "cls": "line", "h": 100, "top": 100,
                 "t": "Just confidence."},
            ]},
            {"in": 13.8, "out": 15.5, "top": 760, "els": SIGNOFF},
        ],
    },

    # ── the set: matched fabric is the whole point ──────────────────────
    "sets": {
        "dur": 15.5,
        "beats": [
            {"in": 0.3, "out": 4.0, "top": 660, "els": [
                {"k": "slab", "at": 0.0, "cls": "line", "h": 100,
                 "t": "Two pieces."},
                {"k": "slab", "at": 0.35, "cls": "line dim", "h": 100,
                 "top": 100, "t": "One fabric."},
                {"k": "rule", "at": 0.95, "top": 226, "d": 1.1},
            ]},
            {"in": 4.2, "out": 9.2, "top": 540, "els": [
                {"k": "count", "at": 0.0, "to": 230, "d": 1.8, "h": 370},
                {"k": "slab", "at": 1.7, "cls": "unit", "h": 126, "top": 372,
                 "t": "g/m&#178;"},
                {"k": "rule", "at": 2.2, "top": 530, "d": 0.9},
                {"k": "slab", "at": 2.6, "cls": "meta", "h": 62, "top": 578,
                 "t": "Bra and leggings &#183; the same knit"},
                {"k": "slab", "at": 2.8, "cls": "meta", "h": 62, "top": 646,
                 "t": "89% polyester &#183; 11% spandex"},
            ]},
            {"in": 9.4, "out": 13.4, "top": 560, "els": [
                {"k": "row", "at": 0.0, "top": 0, "l": "$92",
                 "r": "bought separately"},
                {"k": "row", "at": 0.7, "top": 170, "l": "$79",
                 "r": "as a set"},
                {"k": "slab", "at": 1.9, "cls": "line", "h": 100, "top": 360,
                 "t": "Matched fabric"},
                {"k": "slab", "at": 2.1, "cls": "line", "h": 100, "top": 460,
                 "t": '<span class="accent">wears the same.</span>'},
            ]},
            {"in": 13.6, "out": 15.5, "top": 760, "els": SIGNOFF},
        ],
    },

    # ── shipping, said before checkout instead of after ─────────────────
    "shipping": {
        "dur": 14.5,
        "beats": [
            {"in": 0.3, "out": 4.0, "top": 660, "els": [
                {"k": "slab", "at": 0.0, "cls": "line", "h": 100,
                 "t": "Eight to fourteen"},
                {"k": "slab", "at": 0.3, "cls": "line", "h": 100, "top": 100,
                 "t": "business days."},
                {"k": "rule", "at": 0.95, "top": 226, "d": 1.1},
            ]},
            {"in": 4.2, "out": 7.6, "top": 640, "els": [
                {"k": "slab", "at": 0.0, "cls": "line dim", "h": 100,
                 "t": "We say that here,"},
                {"k": "slab", "at": 0.35, "cls": "line", "h": 100, "top": 100,
                 "t": '<span class="accent">not at checkout.</span>'},
            ]},
            {"in": 7.8, "out": 11.0, "top": 600, "els": [
                {"k": "slab", "at": 0.0, "cls": "line dim", "h": 100,
                 "t": "It ships from a"},
                {"k": "slab", "at": 0.3, "cls": "line dim", "h": 100,
                 "top": 100, "t": "partner facility."},
                {"k": "rule", "at": 1.1, "top": 236, "d": 0.9},
                {"k": "slab", "at": 1.5, "cls": "meta", "h": 62, "top": 286,
                 "t": "Free, no minimum &#183; tracked"},
            ]},
            {"in": 11.2, "out": 12.8, "top": 660, "els": [
                {"k": "slab", "at": 0.0, "cls": "line dim", "h": 100,
                 "t": "Not two-day."},
                {"k": "slab", "at": 0.35, "cls": "line", "h": 100, "top": 100,
                 "t": "Not pretending to be."},
            ]},
            {"in": 13.0, "out": 14.5, "top": 760, "els": SIGNOFF},
        ],
    },
}

HTML = r"""<!doctype html><meta charset="utf-8"><style>
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;background:#08090B;overflow:hidden}
body{font-family:"DejaVu Sans","Liberation Sans",Arial,sans-serif;color:#F2F4F7}
/* Q3: a steady scale push, no handheld shake. The whole frame drifts, which
   reads as a camera rather than as elements moving independently. */
#cam{position:absolute;inset:0;transform-origin:50% 45%}
.mask{overflow:hidden;position:absolute;left:96px;right:150px}
/* nowrap belongs here, on every slab, not on .line alone. A mask is a
   single-line window with overflow hidden; anything that wraps loses its
   second line and the next slab overlaps the remains. Worse, a wrapped line
   never overflows horizontally, so fit() below cannot see it — putting the
   rule on .line only left .meta silently clipping "no restocking fee". */
.mask .in{display:block;will-change:transform;white-space:nowrap}
/* nowrap is load-bearing, not cosmetic. A slab is a fixed-height window with
   overflow hidden; if a line wraps, the second line is silently clipped and
   the next slab overlaps the remains. That shipped once and looked like
   corruption. With nowrap the text can only ever overflow horizontally, which
   fit() below detects and corrects. */
.line{font-size:72px;line-height:1.12;letter-spacing:-.025em;font-weight:700}
.line.dim{color:#8A97AB;font-weight:400}
.accent{color:#6E9BFF}
.num{font-family:"DejaVu Sans Mono","Liberation Mono",monospace;
  font-size:340px;line-height:.92;letter-spacing:-.06em;font-weight:700;color:#6E9BFF}
.unit{font-family:"DejaVu Sans Mono","Liberation Mono",monospace;
  font-size:92px;letter-spacing:0;color:#F2F4F7}
.meta{font-family:"DejaVu Sans Mono","Liberation Mono",monospace;
  font-size:34px;letter-spacing:.05em;color:#9AA6B8}
.rowl{font-family:"DejaVu Sans Mono","Liberation Mono",monospace;
  font-size:72px;letter-spacing:-.02em;color:#6E9BFF;font-weight:700}
.rowr{font-family:"DejaVu Sans Mono","Liberation Mono",monospace;
  font-size:32px;letter-spacing:.04em;color:#8A97AB}
.rule{position:absolute;height:3px;background:#1F4FD8;left:96px}
.wordmark{font-size:118px;letter-spacing:.16em;font-weight:700}
.url{font-family:"DejaVu Sans Mono","Liberation Mono",monospace;
  font-size:34px;letter-spacing:.18em;color:#6E9BFF;text-transform:uppercase}
.vig{position:absolute;inset:0;pointer-events:none;
  background:radial-gradient(120% 75% at 50% 45%,rgba(0,0,0,0) 40%,rgba(0,0,0,.55) 100%)}
</style>
<div id="cam"><div id="stage"></div></div><div class="vig"></div>
<script>
const W=1080,SPEC=%SPEC%;
const clamp=(x,a,b)=>Math.max(a,Math.min(b,x));
// easeOutQuint: fast departure settling slowly. R2 — acceleration is what
// reads as speed; constant velocity reads as a slideshow.
const eo=t=>1-Math.pow(1-clamp(t,0,1),5);
const eio=t=>{t=clamp(t,0,1);return t<.5?4*t*t*t:1-Math.pow(-2*t+2,3)/2};
const p=(t,s,d)=>clamp((t-s)/d,0,1);

function slab(html,cls,top,prog,h){
  return `<div class="mask" style="top:${top}px;height:${h}px">
    <span class="in ${cls}" style="transform:translateY(${(1-eo(prog))*h}px)">${html}</span></div>`;
}

// Safety net for the clipping bug above: any line that still overruns its
// column is stepped down until it fits. Deterministic — the same text always
// resolves to the same size — so frames stay reproducible. It should almost
// never fire; the copy is written to fit. If it does fire the line will look
// slightly small, which is a visible cue that the copy is too long.
function fit(){
  document.querySelectorAll(".mask .in").forEach(el=>{
    const box=el.parentNode.clientWidth;
    let size=parseFloat(getComputedStyle(el).fontSize);
    let guard=0;
    while(el.scrollWidth>box && size>22 && guard++<40){
      size-=2; el.style.fontSize=size+"px";
    }
  });
}

function render(t){
  let s="";
  for(const b of SPEC.beats){
    // Fade in fast, hold, fade out slower. The hold is the point (R1).
    const fin=p(t,b.in,0.28), fout=1-p(t,b.out-0.45,0.45);
    const o=Math.min(fin,fout);
    if(o<=0) continue;
    const lt=t-b.in;
    s+=`<div style="opacity:${o}">`;
    for(const e of b.els){
      const top=b.top+(e.top||0);
      if(e.k==="slab"){
        s+=slab(e.t,e.cls,top,p(lt,e.at,0.85),e.h);
      } else if(e.k==="rule"){
        s+=`<div class="rule" style="top:${top}px;width:${eo(p(lt,e.at,e.d))*(W-246)}px"></div>`;
      } else if(e.k==="count"){
        const v=Math.round(eio(p(lt,e.at,e.d))*e.to);
        s+=slab(String(v).padStart(3,"0"),"num",top,p(lt,e.at,0.8),e.h);
      } else if(e.k==="row"){
        s+=slab(e.l,"rowl",top,p(lt,e.at,0.8),92);
        s+=slab(e.r,"rowr",top+96,p(lt,e.at+0.12,0.8),44);
      }
    }
    s+=`</div>`;
  }
  document.getElementById("stage").innerHTML=s;
  fit();
  // 1.00 -> 1.035 across the whole film.
  const z=1+0.035*(t/SPEC.dur);
  document.getElementById("cam").style.transform=`scale(${z})`;
}
</script>"""


def render_film(name, spec, pw):
    d = OUT / name
    d.mkdir(parents=True, exist_ok=True)
    for f in d.glob("f_*.png"):
        f.unlink()

    page_file = d / "film.html"
    page_file.write_text(HTML.replace("%SPEC%", json.dumps(spec)))

    total = int(spec["dur"] * FPS)
    print(f"[{name}] {total} frames, {spec['dur']}s")

    browser = pw.chromium.launch(executable_path=CHROME,
                                 args=["--no-sandbox", "--disable-gpu"])
    page = browser.new_page(viewport={"width": W, "height": H})
    page.goto(f"file://{page_file}")
    for i in range(total):
        page.evaluate(f"render({i / FPS})")
        page.screenshot(path=str(d / f"f_{i:04d}.png"))
    browser.close()

    mp4 = OUT / f"hivolt-{name}.mp4"
    subprocess.run([
        imageio_ffmpeg.get_ffmpeg_exe(), "-y", "-framerate", str(FPS),
        "-i", str(d / "f_%04d.png"),
        # yuv420p and even dimensions, or it plays on desktop and fails
        # silently on a phone.
        "-c:v", "libx264", "-preset", "slow", "-crf", "18",
        "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(mp4),
    ], check=True, capture_output=True)
    print(f"[{name}] wrote {mp4.name}  {mp4.stat().st_size // 1024} KB")
    return mp4


def main():
    want = sys.argv[1:] or list(FILMS)
    OUT.mkdir(parents=True, exist_ok=True)
    made = []
    with sync_playwright() as pw:
        for n in want:
            if n not in FILMS:
                print(f"unknown film: {n}", file=sys.stderr)
                return 1
            made.append(render_film(n, FILMS[n], pw))
    print("\n" + "\n".join(str(m) for m in made))
    return 0


if __name__ == "__main__":
    sys.exit(main())
