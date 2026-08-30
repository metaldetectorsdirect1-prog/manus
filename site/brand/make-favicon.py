#!/usr/bin/env python3
"""HIVOLT favicon, derived from the authoritative badge.

Nothing is invented. Mark, volt accent and ground all come from
site/brand/hivolt-badge.png, supplied by the owner 2026-08-23; README.md
designates that badge for favicon use.

The badge cannot serve as-is: it carries the HIVOLT wordmark and a tagline,
both illegible below ~64px. So the volt swoosh is isolated and re-set on the
brand ground -- a favicon wants the icon, not the lockup.

Two things this has to get right:
  * the volt ring must not leak into the crop (mask to a circle well inside it)
  * the swoosh is ~2:1, so scale on WIDTH, not the longest edge, or the mark
    ends up marooned in vertical whitespace and dies at 16px
"""
from PIL import Image

SRC    = "site/brand/hivolt-badge.png"
GROUND = (9, 9, 9)          # #090909 per README
VOLT   = (218, 243, 5)      # #DAF305, sampled from the badge
RING_SAFE = 0.80            # fraction of radius kept; ring inner edge ~0.87
FILL      = 0.86            # swoosh width as fraction of canvas

def swoosh_bbox(im, tol=60):
    W, H = im.size
    cx, cy, rmax = W/2, H/2, (W/2)*RING_SAFE
    px = im.load()
    minx, miny, maxx, maxy = W, H, 0, 0
    for y in range(int(H*0.15), int(H*0.62)):        # above the wordmark
        for x in range(int(W*0.08), int(W*0.92)):
            if (x-cx)**2 + (y-cy)**2 > rmax*rmax:    # inside the ring only
                continue
            r, g, b = px[x, y][:3]
            if abs(r-VOLT[0]) < tol and abs(g-VOLT[1]) < tol and b < 90:
                minx, miny = min(minx, x), min(miny, y)
                maxx, maxy = max(maxx, x), max(maxy, y)
    return minx, miny, maxx, maxy

def main():
    badge = Image.open(SRC).convert("RGB")
    x0, y0, x1, y1 = swoosh_bbox(badge)
    sw, sh = x1-x0, y1-y0
    print(f"swoosh x{x0}-{x1} y{y0}-{y1}  {sw}x{sh}  ratio {sw/sh:.2f}")

    S = 512
    scale  = (S*FILL) / sw                      # scale on width
    nw, nh = int(sw*scale), int(sh*scale)
    mark   = badge.crop((x0, y0, x1+1, y1+1)).resize((nw, nh), Image.LANCZOS)

    out = Image.new("RGB", (S, S), GROUND)
    out.paste(mark, ((S-nw)//2, (S-nh)//2))
    out.save("site/brand/hivolt-favicon-512.png")
    for n in (16, 32, 48, 64, 180):
        out.resize((n, n), Image.LANCZOS).save(f"site/brand/hivolt-favicon-{n}.png")

    pad, sizes = 24, (512, 64, 48, 32, 16)
    sheet = Image.new("RGB", (sum(sizes)+pad*(len(sizes)+1), 512+pad*2), (255,255,255))
    x = pad
    for n in sizes:
        sheet.paste(out.resize((n, n), Image.LANCZOS), (x, (512+pad*2-n)//2))
        x += n + pad
    sheet.save("site/brand/hivolt-favicon-sizes.png")
    print(f"mark {nw}x{nh} in {S}px canvas")

if __name__ == "__main__":
    main()
