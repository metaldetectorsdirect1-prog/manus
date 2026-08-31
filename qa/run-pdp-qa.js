// QA FIXTURE — PDP sticky-ATC behavior QA + axe-core accessibility scan (local only)
// node qa/run-pdp-qa.js
const { chromium } = require('playwright-core');
const path = require('path');
const fs = require('fs');

const OUT = path.join(__dirname, 'screenshots', 'master');
fs.mkdirSync(OUT, { recursive: true });
const AXE = fs.readFileSync(path.join(__dirname, 'node_modules', 'axe-core', 'axe.min.js'), 'utf8');

const results = { stickyAtc: [], axe: [] };
let failures = 0;
const check = (arr, name, ok, detail) => {
  arr.push({ name, ok, detail: detail || '' });
  if (!ok) failures++;
};

(async () => {
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  const pdpUrl = 'file://' + path.join(__dirname, 'pdp-harness.html');

  // ---- Sticky ATC behavioral QA at 4 mobile widths ----
  for (const w of [320, 375, 390, 430]) {
    const page = await browser.newPage({ viewport: { width: w, height: 720 } });
    const errors = [];
    page.on('pageerror', (e) => errors.push(String(e)));
    await page.goto(pdpUrl);
    await page.waitForTimeout(150);
    const t = (name, ok, detail) => check(results.stickyAtc, `${w}px ${name}`, ok, detail);

    const bar = page.locator('#StickyAtc-qa');
    t('hidden initially', (await bar.getAttribute('aria-hidden')) === 'true' && !(await bar.isVisible()));

    const docH0 = await page.evaluate(() => document.documentElement.scrollHeight);

    // Scroll until ATC button is above viewport
    await page.evaluate(() => {
      const btn = document.querySelector('[name="add"]');
      window.scrollTo(0, btn.getBoundingClientRect().bottom + window.scrollY + 40);
    });
    await page.waitForTimeout(350);
    t('appears after ATC above viewport', (await bar.getAttribute('aria-hidden')) === 'false' && (await bar.isVisible()));
    t('no layout shift (fixed bar)', (await page.evaluate(() => document.documentElement.scrollHeight)) === docH0);
    t('single form on page', (await page.locator('form[id^="AddToCartForm"]').count()) === 1);
    t('bar price mirrors PDP', (await page.locator('[data-sticky-price]').textContent()).trim() === '$68.00');
    t('bar compare mirrors PDP', (await page.locator('[data-sticky-compare]').textContent()).trim() === '$88.00');
    t('bar button >=44px target', (await bar.locator('[data-sticky-submit]').boundingBox()).height >= 44);
    if (w === 390) await page.screenshot({ path: path.join(OUT, 'sticky-atc-390.png') });
    if (w === 320) await page.screenshot({ path: path.join(OUT, 'sticky-atc-320.png') });

    // Variant change -> price sync (MutationObserver path)
    await page.locator('.vbtn[data-variant]', { hasText: 'Charcoal' }).click();
    await page.waitForTimeout(80);
    t('price syncs on variant change', (await page.locator('[data-sticky-price]').textContent()).trim() === '$74.00');
    t('compare hides when none', await page.locator('[data-sticky-compare]').evaluate((el) => el.hidden === true));

    // Sold-out variant -> disabled + label sync
    await page.locator('.vbtn[data-variant]', { hasText: 'Ivory' }).click();
    await page.waitForTimeout(80);
    t('sold-out disables bar button', await bar.locator('[data-sticky-submit]').isDisabled());
    t('sold-out label syncs', (await bar.locator('[data-sticky-submit]').textContent()).trim() === 'Sold out');
    if (w === 390) await page.screenshot({ path: path.join(OUT, 'sticky-atc-soldout-390.png') });
    t('disabled bar click does not submit', await page.evaluate(() => { document.querySelector('[data-sticky-submit]').click(); return window.__submits === 0; }));

    // Back to available -> submit via bar, exactly once, main form only.
    // (Variant clicks auto-scroll the ATC back into view, correctly hiding the
    // bar — re-scroll past the ATC first, as a real shopper would be.)
    await page.locator('.vbtn[data-variant]', { hasText: 'Oat' }).click();
    await page.waitForTimeout(80);
    await page.evaluate(() => {
      const btn = document.querySelector('[name="add"]');
      window.scrollTo(0, btn.getBoundingClientRect().bottom + window.scrollY + 40);
    });
    await page.waitForTimeout(350);
    await bar.locator('[data-sticky-submit]').click();
    t('bar submits main form exactly once', (await page.evaluate(() => window.__submits)) === 1);

    // Scroll back to top -> hides again
    await page.evaluate(() => window.scrollTo(0, 0));
    await page.waitForTimeout(350);
    t('hides when ATC back in view', (await bar.getAttribute('aria-hidden')) === 'true');
    t('no JS errors', errors.length === 0, errors.join('; '));
    await page.close();
  }

  // Desktop: bar must not display; meta column sticky
  {
    const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
    await page.goto(pdpUrl);
    await page.waitForTimeout(150);
    check(results.stickyAtc, '1440px bar display:none', await page.locator('#StickyAtc-qa').evaluate((el) => getComputedStyle(el).display === 'none'));
    check(results.stickyAtc, '1440px meta column sticky', await page.locator('.product-single__meta').evaluate((el) => getComputedStyle(el).position === 'sticky'));
    await page.screenshot({ path: path.join(OUT, 'pdp-1440.png'), fullPage: true });
    await page.close();
  }
  {
    const page = await browser.newPage({ viewport: { width: 390, height: 844 } });
    await page.goto(pdpUrl);
    await page.screenshot({ path: path.join(OUT, 'pdp-390.png'), fullPage: true });
    await page.close();
  }

  // ---- axe-core scans ----
  for (const [name, file] of [
    ['pdp-harness', 'pdp-harness.html'],
    ['home-harness-v4', 'home-harness-v4.html'],
    ['grid-harness-100', 'grid-harness-100.html'],
  ]) {
    for (const w of [390, 1440]) {
      const page = await browser.newPage({ viewport: { width: w, height: 900 } });
      await page.goto('file://' + path.join(__dirname, file));
      await page.waitForTimeout(300);
      await page.evaluate(AXE);
      const r = await page.evaluate(async () => {
        const res = await axe.run(document, { resultTypes: ['violations'] });
        return res.violations.map((v) => ({ id: v.id, impact: v.impact, nodes: v.nodes.length, help: v.help }));
      });
      results.axe.push({ page: name, width: w, violations: r });
      const critical = r.filter((v) => v.impact === 'critical' || v.impact === 'serious');
      check(results.stickyAtc, `axe ${name}@${w} no critical/serious`, critical.length === 0, JSON.stringify(critical));
      await page.close();
    }
  }

  await browser.close();
  fs.writeFileSync(path.join(__dirname, 'pdp-qa-results.json'), JSON.stringify(results, null, 2));
  const total = results.stickyAtc.length;
  const passed = results.stickyAtc.filter((x) => x.ok).length;
  console.log(`PASS ${passed}/${total}`);
  for (const x of results.stickyAtc.filter((x) => !x.ok)) console.log('FAIL:', x.name, x.detail);
  for (const a of results.axe) console.log(`axe ${a.page}@${a.width}: ${a.violations.length} violations`, a.violations.map((v) => `${v.id}(${v.impact})`).join(', ') || '-');
  process.exit(failures ? 1 : 0);
})();
