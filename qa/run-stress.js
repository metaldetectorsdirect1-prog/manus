// QA FIXTURE stress runner — local only. Renders grid-harness.html and the
// homepage-rhythm harness at 7 viewports, asserts layout invariants, and
// captures screenshots. Validates theme-design scalability, NOT Shopify
// runtime behavior (Impulse JS/liquid does not run here).
const { chromium } = require('playwright-core');
const path = require('path');
const fs = require('fs');

const WIDTHS = [320, 375, 390, 430, 768, 1024, 1440];
const SHOT_WIDTHS = [320, 390, 1440];

(async () => {
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  const results = [];
  for (const file of ['grid-harness.html', 'home-harness.html']) {
    const url = 'file://' + path.resolve(__dirname, file);
    for (const width of WIDTHS) {
      const page = await browser.newPage({ viewport: { width, height: 900 } });
      const errors = [];
      page.on('pageerror', e => errors.push(String(e)));
      page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
      await page.goto(url);
      await page.waitForTimeout(400);
      const metrics = await page.evaluate(() => {
        const out = { overflowX: document.documentElement.scrollWidth > window.innerWidth + 1,
                      scrollWidth: document.documentElement.scrollWidth,
                      innerWidth: window.innerWidth,
                      domNodes: document.querySelectorAll('*').length };
        const grid = document.getElementById('grid');
        if (grid) {
          const cards = [...grid.querySelectorAll('.card')];
          out.cards = cards.length;
          out.columns = getComputedStyle(grid).gridTemplateColumns.split(' ').length;
          // per-row height consistency + collision checks
          const rows = new Map();
          let collisions = 0, titleOverflow = 0;
          for (const c of cards) {
            const r = c.getBoundingClientRect();
            const key = Math.round(r.top);
            if (!rows.has(key)) rows.set(key, []);
            rows.get(key).push(r.height);
            const badge = c.querySelector('.card__badge');
            const title = c.querySelector('.card__title');
            if (badge && title) {
              const b = badge.getBoundingClientRect(), t = title.getBoundingClientRect();
              if (b.bottom > t.top && b.top < t.bottom && b.right > t.left && b.left < t.right) collisions++;
            }
            // Clamp SUCCESS = long text ellipsized into <=2 rendered lines
            // (scrollHeight > clientHeight is expected there). Failure = the
            // rendered box itself exceeds the 2-line budget (clamp not applied).
            if (title && title.clientHeight > 42) titleOverflow++;
          }
          let maxRowVariance = 0;
          for (const hs of rows.values()) {
            if (hs.length > 1) maxRowVariance = Math.max(maxRowVariance, Math.max(...hs) - Math.min(...hs));
          }
          out.maxRowHeightVariancePx = Math.round(maxRowVariance);
          out.badgeTitleCollisions = collisions;
          out.titleClampFailures = titleOverflow;
        }
        const firstShop = document.querySelector('[data-first-shopping-surface]');
        if (firstShop) out.firstShoppingSurfaceY = Math.round(firstShop.getBoundingClientRect().top + window.scrollY);
        return out;
      });
      results.push({ file, width, errors, ...metrics });
      if (SHOT_WIDTHS.includes(width)) {
        await page.screenshot({ path: path.join(__dirname, 'screenshots', `${file.replace('.html','')}-${width}.png`), fullPage: true });
      }
      await page.close();
    }
  }
  await browser.close();
  fs.writeFileSync(path.join(__dirname, 'stress-results.json'), JSON.stringify(results, null, 1));
  let fail = 0;
  for (const r of results) {
    const bad = r.overflowX || (r.errors && r.errors.length) || r.badgeTitleCollisions > 0 || (r.maxRowHeightVariancePx || 0) > 2 || (r.titleClampFailures || 0) > 0;
    if (bad) fail++;
    console.log(`${r.file}@${r.width}: cols=${r.columns ?? '-'} cards=${r.cards ?? '-'} overflowX=${r.overflowX} rowVar=${r.maxRowHeightVariancePx ?? '-'}px collisions=${r.badgeTitleCollisions ?? '-'} clampFail=${r.titleClampFailures ?? '-'} dom=${r.domNodes} err=${r.errors.length}${r.firstShoppingSurfaceY ? ' firstShopY=' + r.firstShoppingSurfaceY : ''}${bad ? '  <-- FAIL' : ''}`);
  }
  console.log(fail === 0 ? 'ALL PASS' : `${fail} viewport(s) FAILED`);
  process.exit(fail === 0 ? 0 : 1);
})();
