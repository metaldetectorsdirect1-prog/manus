// QA FIXTURE — V4 master-reference render + 100-card pagination test (local only)
// node qa/run-v4-context.js
const { chromium } = require('playwright-core');
const path = require('path');
const fs = require('fs');

const OUT = path.join(__dirname, 'screenshots', 'v4');
fs.mkdirSync(OUT, { recursive: true });

(async () => {
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  const results = { home: [], grid100: [] };

  for (const vp of [{ w: 390, h: 844 }, { w: 1440, h: 900 }]) {
    const page = await browser.newPage({ viewport: { width: vp.w, height: vp.h } });
    const errors = [];
    page.on('pageerror', (e) => errors.push(String(e)));
    await page.goto('file://' + path.join(__dirname, 'home-harness-v4.html'));
    await page.waitForLoadState('networkidle');
    await page.waitForTimeout(250);
    const m = await page.evaluate(() => ({
      overflowX: document.documentElement.scrollWidth > window.innerWidth,
      pageHeight: Math.round(document.documentElement.scrollHeight),
      firstShoppingSurfaceY: (() => { const el = document.querySelector('[data-first-shopping-surface]'); return el ? Math.round(el.getBoundingClientRect().top + window.scrollY) : null; })(),
      brokenImages: [...document.images].filter((i) => !i.complete || i.naturalWidth === 0).length,
      stickyHeader: getComputedStyle(document.querySelector('.hdr')).position === 'sticky',
    }));
    await page.screenshot({ path: path.join(OUT, `v4-full-${vp.w}.png`), fullPage: true });
    for (const el of await page.$$('[data-shot]')) {
      const name = await el.getAttribute('data-shot');
      await el.scrollIntoViewIfNeeded();
      await page.waitForTimeout(50);
      await el.screenshot({ path: path.join(OUT, `v4-${name}-${vp.w}.png`) });
    }
    results.home.push({ viewport: vp.w, jsErrors: errors.length, ...m });
    await page.close();
  }

  // 100-card pagination-scale grid
  for (const vp of [{ w: 390, h: 844 }, { w: 768, h: 1024 }, { w: 1440, h: 900 }]) {
    const page = await browser.newPage({ viewport: { width: vp.w, height: vp.h } });
    const errors = [];
    page.on('pageerror', (e) => errors.push(String(e)));
    await page.goto('file://' + path.join(__dirname, 'grid-harness-100.html'));
    await page.waitForLoadState('networkidle');
    await page.waitForTimeout(250);
    const m = await page.evaluate(() => {
      const cards = [...document.querySelectorAll('.card')];
      const rows = new Map();
      for (const c of cards) {
        const top = Math.round(c.getBoundingClientRect().top + window.scrollY);
        rows.set(top, (rows.get(top) || 0) + 1);
      }
      const heights = cards.map((c) => Math.round(c.getBoundingClientRect().height));
      const rowTops = [...rows.keys()].sort((a, b) => a - b);
      let cols = rows.get(rowTops[0]) || 0;
      let titleOverflow = 0;
      for (const c of cards) {
        const t = c.querySelector('.card__title');
        if (t && t.clientHeight > 42) titleOverflow++;
      }
      return {
        cards: cards.length,
        cols,
        overflowX: document.documentElement.scrollWidth > window.innerWidth,
        titleOverflow,
        pagerLinks: document.querySelectorAll('nav[aria-label="Pagination"] a').length,
        minCardH: Math.min(...heights), maxCardH: Math.max(...heights),
      };
    });
    await page.screenshot({ path: path.join(OUT, `grid100-${vp.w}.png`), fullPage: vp.w !== 390 });
    results.grid100.push({ viewport: vp.w, jsErrors: errors.length, ...m });
    await page.close();
  }

  await browser.close();
  fs.writeFileSync(path.join(OUT, 'v4-results.json'), JSON.stringify(results, null, 2));
  console.log(JSON.stringify(results, null, 2));
})().catch((e) => { console.error(e); process.exit(1); });
