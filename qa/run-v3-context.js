// QA FIXTURE — V3 in-context render runner (local only)
// node qa/run-v3-context.js
const { chromium } = require('playwright-core');
const path = require('path');
const fs = require('fs');

const OUT = path.join(__dirname, 'screenshots', 'v3');
fs.mkdirSync(OUT, { recursive: true });

const VIEWPORTS = [
  { w: 390, h: 844 },
  { w: 1440, h: 900 },
];

(async () => {
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  const results = [];
  for (const vp of VIEWPORTS) {
    const page = await browser.newPage({ viewport: { width: vp.w, height: vp.h } });
    const errors = [];
    page.on('pageerror', (e) => errors.push(String(e)));
    await page.goto('file://' + path.join(__dirname, 'home-harness-v3.html'));
    await page.waitForLoadState('networkidle');
    await page.waitForTimeout(250);

    const metrics = await page.evaluate(() => {
      const fss = document.querySelector('[data-first-shopping-surface]');
      const shots = [...document.querySelectorAll('[data-shot]')].map((el) => ({
        name: el.getAttribute('data-shot'),
        top: Math.round(el.getBoundingClientRect().top + window.scrollY),
        height: Math.round(el.getBoundingClientRect().height),
      }));
      return {
        overflowX: document.documentElement.scrollWidth > window.innerWidth,
        pageHeight: Math.round(document.documentElement.scrollHeight),
        firstShoppingSurfaceY: fss ? Math.round(fss.getBoundingClientRect().top + window.scrollY) : null,
        brokenImages: [...document.images].filter((i) => !i.complete || i.naturalWidth === 0).length,
        shots,
      };
    });

    await page.screenshot({ path: path.join(OUT, `v3-full-${vp.w}.png`), fullPage: true });
    for (const el of await page.$$('[data-shot]')) {
      const name = await el.getAttribute('data-shot');
      await el.scrollIntoViewIfNeeded();
      await page.waitForTimeout(60);
      await el.screenshot({ path: path.join(OUT, `v3-${name}-${vp.w}.png`) });
    }
    results.push({ viewport: vp.w, jsErrors: errors.length, ...metrics });
    await page.close();
  }
  await browser.close();
  fs.writeFileSync(path.join(OUT, 'v3-context-results.json'), JSON.stringify(results, null, 2));
  console.log(JSON.stringify(results, null, 2));
})().catch((e) => { console.error(e); process.exit(1); });
