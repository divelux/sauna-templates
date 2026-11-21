// Checks the sauna club website template in one headless Chromium:
// widths 375/390/768/1280, no sideways scroll, no outside requests, one h1, alt texts, skip link, fonts, FAQ keyboard.
// Run: flock /tmp/freebies-chromium.lock env NODE_PATH=/opt/carmax/node_modules node w3s_check70.js <outdir>
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const out = process.argv[2] || '/tmp';
  const url = 'file://' + path.resolve(__dirname, '../sauna-club-website/index.html');
  const b = await chromium.launch({ args: ['--no-sandbox', '--disable-dev-shm-usage'] });
  const res = {};
  try {
    const p = await b.newPage({ viewport: { width: 375, height: 812 } });
    const reqs = [], errs = [];
    p.on('request', (r) => { if (!r.url().startsWith('file://') && !r.url().startsWith('data:')) reqs.push(r.url()); });
    p.on('pageerror', (e) => errs.push(e.message));
    p.on('console', (m) => { if (m.type() === 'error') errs.push(m.text()); });
    p.on('requestfailed', (r) => errs.push('failed ' + r.url()));
    await p.goto(url); await p.evaluate(() => document.fonts.ready);
    for (const w of [375, 390, 768, 1280]) {
      await p.setViewportSize({ width: w, height: w < 800 ? 844 : 900 });
      await p.waitForTimeout(150);
      const r = await p.evaluate(() => {
        const de = document.documentElement;
        const wide = [...document.querySelectorAll('body *')].filter((e) => {
          if (e.closest('.table-box,.nav')) return false;
          const b = e.getBoundingClientRect(); return b.right > innerWidth + 1 || b.left < -1;
        }).map((e) => e.tagName + '.' + e.className).slice(0, 5);
        const small = [...document.querySelectorAll('a,button,summary')].filter((e) => {
          const b = e.getBoundingClientRect(); return b.width && b.height < 24 && !e.closest('p,dd,td');
        }).map((e) => e.textContent.trim().slice(0, 20));
        return { sw: de.scrollWidth, iw: innerWidth, wide, small, h: de.scrollHeight };
      });
      res[w] = r;
      await p.screenshot({ path: `${out}/site-${w}.png`, fullPage: true });
    }
    await p.setViewportSize({ width: 1280, height: 900 });
    res.a11y = await p.evaluate(() => ({
      h1: document.querySelectorAll('h1').length,
      headings: [...document.querySelectorAll('h1,h2,h3')].map((h) => h.tagName).join(' '),
      imgNoAlt: [...document.querySelectorAll('img')].filter((i) => !i.hasAttribute('alt')).length,
      fonts: [...document.fonts].map((f) => f.family + ':' + f.status),
      landmarks: ['header', 'nav', 'main', 'footer'].map((t) => t + ':' + document.querySelectorAll(t).length).join(' '),
      lang: document.documentElement.lang,
    }));
    await p.keyboard.press('Tab');
    res.firstFocus = await p.evaluate(() => { const a = document.activeElement; const b = a.getBoundingClientRect(); return a.className + ' visible:' + (b.top >= 0); });
    await p.screenshot({ path: `${out}/site-skip.png`, clip: { x: 0, y: 0, width: 640, height: 160 } });
    await p.focus('.faq summary');
    await p.keyboard.press('Enter');
    res.faqOpen = await p.evaluate(() => document.querySelector('.faq details').open);
    res.reqs = reqs; res.errs = errs;
  } finally { await b.close(); }
  console.log(JSON.stringify(res, null, 1));
})();
