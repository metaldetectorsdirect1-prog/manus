from playwright.sync_api import sync_playwright
import sys
EXE="/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
shots=[("desktop",1440,1200,"light"),("desktop-dark",1440,1200,"dark"),("mobile",390,844,"light")]
with sync_playwright() as p:
    b=p.chromium.launch(executable_path=EXE,args=["--no-sandbox"])
    for name,w,h,scheme in shots:
        pg=b.new_page(viewport={"width":w,"height":h},color_scheme=scheme,device_scale_factor=2)
        pg.goto("file:///home/user/manus/site/index.html")
        pg.wait_for_timeout(700)
        pg.screenshot(path=f"shot-{name}.png",full_page=True)
        # measure horizontal overflow
        ov=pg.evaluate("()=>({doc:document.documentElement.scrollWidth,win:innerWidth})")
        print(name,ov,"OVERFLOW" if ov['doc']>ov['win']+1 else "ok")
        pg.close()
    b.close()
