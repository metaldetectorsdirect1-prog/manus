"""Render a TikTok photo carousel from HIVOLT's real published specs.

Nothing here is AI-generated imagery: the slides are typeset HTML built from
figures that already sit on the product pages, screenshotted with Chromium and
converted to JPEG because TikTok rejects PNG.

Rendering locally rather than generating video matters for one reason: the
frames can be opened and checked before they are published. An AI clip of a
real garment cannot be verified from this environment, and an unverifiable
picture of a product someone can buy is not worth the reach.
"""
import base64, pathlib, subprocess, sys
from PIL import Image

OUT = pathlib.Path(__file__).parent
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
W, H = 1080, 1920

CSS = """
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px}
/* Content is pulled above centre and kept out of the right rail for the same
   reason as the footer — the middle of a TikTok frame is the only region no
   platform chrome sits on top of. */
body{
  background:#0E1013;color:#F2F4F7;
  font-family:"DejaVu Sans","Liberation Sans",Arial,sans-serif;
  display:flex;flex-direction:column;justify-content:center;
  padding:120px 150px 460px 96px;position:relative;overflow:hidden;
}
.rule{position:absolute;left:0;right:0;height:6px;background:#1F4FD8}
.rule.top{top:0}.rule.bot{bottom:0}
.eyebrow{
  font-family:"DejaVu Sans Mono","Liberation Mono",monospace;
  font-size:30px;letter-spacing:.28em;text-transform:uppercase;
  color:#7C90B8;margin-bottom:56px;
}
h1{font-size:94px;line-height:1.06;letter-spacing:-.035em;font-weight:700}
h1 em{font-style:normal;color:#6E9BFF}
p.sub{font-size:44px;line-height:1.45;color:#AEB8C7;margin-top:48px;max-width:20ch}
.big{
  font-family:"DejaVu Sans Mono","Liberation Mono",monospace;
  font-size:230px;line-height:1;letter-spacing:-.05em;color:#6E9BFF;font-weight:700;
}
.big small{font-size:78px;letter-spacing:0;color:#F2F4F7;display:block;margin-top:24px}
.rows{margin-top:72px;border-top:2px solid #262C36}
.row{
  display:flex;justify-content:space-between;align-items:baseline;
  padding:34px 0;border-bottom:2px solid #262C36;
  font-family:"DejaVu Sans Mono","Liberation Mono",monospace;font-size:38px;
}
.row span:first-child{color:#7C90B8}
.row span:last-child{color:#F2F4F7}
/* Raised well clear of the bottom of the frame: TikTok lays its caption,
   handle and music ticker over roughly the lower fifth, and its action rail
   over the right edge. A footer at bottom:104px was sitting underneath both.
   nowrap because the URL was breaking mid-word into "HIVOLT-" / "USA.COM". */
.foot{
  position:absolute;left:96px;right:220px;bottom:300px;
  font-family:"DejaVu Sans Mono","Liberation Mono",monospace;
  font-size:28px;letter-spacing:.12em;text-transform:uppercase;color:#7C90B8;
  display:flex;justify-content:space-between;gap:40px;white-space:nowrap;
}
.foot b{color:#6E9BFF;font-weight:400}
"""

SLIDES = [
    # 1 — hook
    """<p class="eyebrow">Fabric weight</p>
       <h1>Your leggings<br>have a number<br>on them.<br><em>Nobody prints it.</em></h1>""",
    # 2 — what it means
    """<p class="eyebrow">What GSM means</p>
       <h1>Grams per<br>square metre.</h1>
       <p class="sub">How much fabric is actually there. Thin knit stretched over a
       curve is what goes see-through.</p>""",
    # 3 — the number
    """<p class="eyebrow">This pair</p>
       <div class="big">230<small>g/m&#178;</small></div>
       <div class="rows">
         <div class="row"><span>Composition</span><span>89% polyester</span></div>
         <div class="row"><span></span><span>11% spandex</span></div>
         <div class="row"><span>Price</span><span>$59</span></div>
       </div>""",
    # 4 — the challenge
    """<p class="eyebrow">Try it yourself</p>
       <h1>Go find this<br>number on any<br>big brand's site.<br><em>We'll wait.</em></h1>""",
    # 5 — cta
    """<p class="eyebrow">HIVOLT</p>
       <h1>Every fabric<br>weight we sell<br>is <em>published.</em></h1>
       <p class="sub">All 110 products. Taken from the mill spec sheet, unedited.</p>""",
]

FOOT = ('<div class="foot"><span>hivolt-usa.com/tiktok</span>'
        '<span><b>Published, not claimed</b></span></div>')


def build():
    files = []
    for i, body in enumerate(SLIDES, 1):
        html = (f"<!doctype html><meta charset='utf-8'><style>{CSS}</style>"
                f"<body><div class='rule top'></div>{body}{FOOT}"
                f"<div class='rule bot'></div></body>")
        h = OUT / f"slide{i}.html"
        h.write_text(html)
        png = OUT / f"slide{i}.png"
        subprocess.run([
            CHROME, "--headless", "--disable-gpu", "--no-sandbox",
            "--hide-scrollbars", f"--window-size={W},{H}",
            f"--screenshot={png}", f"file://{h}",
        ], check=True, capture_output=True, timeout=120)
        jpg = OUT / f"slide{i}.jpg"
        Image.open(png).convert("RGB").save(jpg, "JPEG", quality=92)
        kb = jpg.stat().st_size // 1024
        im = Image.open(jpg)
        print(f"  slide{i}.jpg  {im.size[0]}x{im.size[1]}  {kb} KB")
        files.append(jpg)
    return files


if __name__ == "__main__":
    print(f"chromium: {'ok' if pathlib.Path(CHROME).exists() else 'MISSING'}")
    build()
    print("done")
