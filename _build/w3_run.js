// Wave 3 design templates: renders jobs from a JSON list with ONE Chromium, closed at the end.
// Per job: PDF (preferCSSPageSize), PNG of each .page, a Figma-friendly SVG made from the laid-out page,
// layout checks (overflow), and optionally an editing test (type into fields, reload, check localStorage, Reset).
// Run only under the shared lock:
//   NODE_PATH=/opt/carmax/node_modules flock /tmp/freebies-chromium.lock nice -n 10 node w3_run.js jobs.json report.json
const { chromium } = require('playwright');
const fs = require('fs');

// ---- DOM -> SVG (runs inside the page) ----
function toSVG({ pageSel, index, title }) {
  const page = [...document.querySelectorAll(pageSel)].filter((p) => p.getClientRects().length)[index];
  const P = page.getBoundingClientRect();
  const W = P.width, H = P.height;
  const out = [];
  const r2 = (v) => Math.round(v * 100) / 100;
  const escx = (s) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  const color = (c) => {
    const m = c.match(/rgba?\(([^)]+)\)/); if (!m) return null;
    const p = m[1].split(/[ ,/]+/).filter(Boolean).map(Number);
    if (p.length > 3 && p[3] === 0) return null;
    const hex = '#' + p.slice(0, 3).map((v) => Math.round(v).toString(16).padStart(2, '0')).join('');
    return p.length > 3 && p[3] < 1 ? { hex, a: p[3] } : { hex, a: 1 };
  };
  const fillAttr = (c, k = 'fill') => c.a < 1 ? `${k}="${c.hex}" ${k}-opacity="${r2(c.a)}"` : `${k}="${c.hex}"`;
  const probes = {};
  const used = {};
  let clipN = 0;
  function baseline(cs) {
    const key = [cs.fontFamily, cs.fontSize, cs.fontWeight, cs.fontStretch, cs.fontStyle].join('|');
    if (key in probes) return probes[key];
    const s = document.createElement('span');
    s.style.cssText = `position:absolute;left:0;top:0;white-space:nowrap;line-height:normal;font-family:${cs.fontFamily};font-size:${cs.fontSize};font-weight:${cs.fontWeight};font-stretch:${cs.fontStretch};font-style:${cs.fontStyle}`;
    s.textContent = 'Hxg';
    const b = document.createElement('span');
    b.style.cssText = 'display:inline-block;width:0;height:0;vertical-align:baseline';
    s.appendChild(b); document.body.appendChild(s);
    const rg = document.createRange(); rg.selectNodeContents(s.firstChild);
    const off = b.getBoundingClientRect().bottom - rg.getBoundingClientRect().top;
    s.remove();
    return (probes[key] = off);
  }
  const fam = (f) => f.split(',')[0].replace(/["']/g, '').trim();
  function box(el, cs) {
    const r = el.getBoundingClientRect();
    if (!r.width || !r.height) return;
    const x = r.left - P.left, y = r.top - P.top;
    const rad = parseFloat(cs.borderTopLeftRadius) || 0;
    const bg = color(cs.backgroundColor);
    if (bg) out.push(`<rect x="${r2(x)}" y="${r2(y)}" width="${r2(r.width)}" height="${r2(r.height)}"${rad ? ` rx="${r2(Math.min(rad, r.width / 2, r.height / 2))}"` : ''} ${fillAttr(bg)}/>`);
    const sides = ['Top', 'Right', 'Bottom', 'Left'].map((s) => ({ s, w: parseFloat(cs['border' + s + 'Width']) || 0,
      st: cs['border' + s + 'Style'], c: color(cs['border' + s + 'Color']) })).filter((b) => b.w > 0 && b.st !== 'none' && b.c);
    if (!sides.length) return;
    const dash = (b) => b.st === 'dashed' ? ` stroke-dasharray="${r2(b.w * 3)} ${r2(b.w * 2)}"` : b.st === 'dotted' ? ` stroke-dasharray="0 ${r2(b.w * 2)}" stroke-linecap="round"` : '';
    const all = sides.length === 4 && sides.every((b) => b.w === sides[0].w && b.st === sides[0].st && b.c.hex === sides[0].c.hex);
    if (all) {
      const b = sides[0], h = b.w / 2;
      out.push(`<rect x="${r2(x + h)}" y="${r2(y + h)}" width="${r2(r.width - b.w)}" height="${r2(r.height - b.w)}"${rad ? ` rx="${r2(Math.max(0, rad - h))}"` : ''} fill="none" ${fillAttr(b.c, 'stroke')} stroke-width="${r2(b.w)}"${dash(b)}/>`);
      return;
    }
    for (const b of sides) {
      const h = b.w / 2;
      const L = { Top: [x, y + h, x + r.width, y + h], Bottom: [x, y + r.height - h, x + r.width, y + r.height - h],
        Left: [x + h, y, x + h, y + r.height], Right: [x + r.width - h, y, x + r.width - h, y + r.height] }[b.s];
      out.push(`<line x1="${r2(L[0])}" y1="${r2(L[1])}" x2="${r2(L[2])}" y2="${r2(L[3])}" ${fillAttr(b.c, 'stroke')} stroke-width="${r2(b.w)}"${dash(b)}/>`);
    }
  }
  function text(node) {
    const el = node.parentElement, cs = getComputedStyle(el);
    if (cs.visibility === 'hidden') return;
    const c = color(cs.color); if (!c) return;
    const t = node.data, words = [];
    const re = /\S+/g; let m;
    const rg = document.createRange();
    while ((m = re.exec(t))) {
      rg.setStart(node, m.index); rg.setEnd(node, m.index + m[0].length);
      const rs = [...rg.getClientRects()].filter((q) => q.width > 0);
      if (!rs.length) continue;
      if (rs.length === 1) { words.push({ s: m[0], r: rs[0] }); continue; }
      for (let i = 0; i < m[0].length; i++) { // a word split over lines: place it letter by letter
        rg.setStart(node, m.index + i); rg.setEnd(node, m.index + i + 1);
        const q = rg.getBoundingClientRect(); if (q.width) words.push({ s: m[0][i], r: q, glue: i > 0 });
      }
    }
    if (!words.length) return;
    const lines = [];
    for (const w of words) {
      const L = lines[lines.length - 1];
      if (L && Math.abs(L.top - w.r.top) < 2) { L.parts.push(w); } else lines.push({ top: w.r.top, parts: [w] });
    }
    const off = baseline(cs);
    const ls = cs.letterSpacing === 'normal' ? 0 : parseFloat(cs.letterSpacing) || 0;
    const up = cs.textTransform === 'uppercase';
    const wt = cs.fontWeight;
    const anchorRight = cs.textAlign === 'right' || cs.textAlign === 'end';
    for (const L of lines) {
      let s = '';
      L.parts.forEach((p, i) => { s += (i && !p.glue ? ' ' : '') + p.s; });
      if (up) s = s.toUpperCase();
      const x0 = L.parts[0].r.left - P.left, x1 = L.parts[L.parts.length - 1].r.right - P.left;
      const y = L.top - P.top + off;
      const ax = anchorRight ? ` text-anchor="end"` : '';
      out.push(`<text x="${r2(anchorRight ? x1 - ls : x0)}" y="${r2(y)}"${ax} font-family="${fam(cs.fontFamily)}" font-size="${r2(parseFloat(cs.fontSize))}" font-weight="${wt}"${ls ? ` letter-spacing="${r2(ls)}"` : ''} ${fillAttr(c)} xml:space="preserve">${escx(s)}</text>`);
    }
  }
  function walk(el) {
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || el.classList.contains('ctl') || el.classList.contains('screen-only')) return;
    if (parseFloat(cs.opacity) === 0) return;
    let name = el.dataset ? el.dataset.name : null;
    if (name) { used[name] = (used[name] || 0) + 1; if (used[name] > 1) name += '-' + used[name]; out.push(`<g id="${escx(name)}">`); }
    if (el.tagName.toLowerCase() === 'svg') {
      const r = el.getBoundingClientRect();
      const cl = el.cloneNode(true);
      ['class', 'aria-hidden', 'data-name', 'style'].forEach((a) => cl.removeAttribute(a));
      cl.setAttribute('x', r2(r.left - P.left)); cl.setAttribute('y', r2(r.top - P.top));
      cl.setAttribute('width', r2(r.width)); cl.setAttribute('height', r2(r.height));
      let s = new XMLSerializer().serializeToString(cl).replace(/currentColor/g, color(cs.color).hex);
      s = s.replace(/ xmlns="http:\/\/www\.w3\.org\/2000\/svg"/, '');
      out.push(s);
    } else if (el.tagName.toLowerCase() === 'img') {
      const r = el.getBoundingClientRect();
      out.push(`<image href="${el.src}" x="${r2(r.left - P.left)}" y="${r2(r.top - P.top)}" width="${r2(r.width)}" height="${r2(r.height)}"/>`);
    } else {
      if (cs.visibility !== 'hidden') box(el, cs);
      const clip = /hidden|clip/.test(cs.overflow);
      if (clip) {
        const r = el.getBoundingClientRect(); clipN++;
        out.push(`<clipPath id="clip${clipN}"><rect x="${r2(r.left - P.left)}" y="${r2(r.top - P.top)}" width="${r2(r.width)}" height="${r2(r.height)}"/></clipPath><g clip-path="url(#clip${clipN})">`);
      }
      for (const n of el.childNodes) {
        if (n.nodeType === 3) text(n);
        else if (n.nodeType === 1) walk(n);
      }
      if (clip) out.push('</g>');
    }
    if (name) out.push('</g>');
  }
  const pcs = getComputedStyle(page);
  const pbg = color(pcs.backgroundColor);
  const body = [];
  out.length = 0;
  for (const n of page.childNodes) { if (n.nodeType === 1) walk(n); else if (n.nodeType === 3) text(n); }
  return `<svg xmlns="http://www.w3.org/2000/svg" width="${r2(W)}" height="${r2(H)}" viewBox="0 0 ${r2(W)} ${r2(H)}">\n` +
    `<title>${escx(title)}</title>\n<desc>Editable template by DIVELUX, https://diveluxsaunahat.com. CC BY 4.0. Fonts: Bricolage Grotesque and Inter (Google Fonts, SIL OFL 1.1). Text layers are live text; groups are named after the fields.</desc>\n` +
    (pbg ? `<rect id="background" width="${r2(W)}" height="${r2(H)}" ${fillAttr(pbg)}/>\n` : '') +
    out.join('\n') + '\n</svg>\n';
}

function checks(pageSel) {
  const res = [];
  [...document.querySelectorAll(pageSel)].filter((p) => p.getClientRects().length).forEach((p, i) => {
    const P = p.getBoundingClientRect();
    p.querySelectorAll('*').forEach((el) => {
      if (el.closest('svg') && el.tagName.toLowerCase() !== 'svg') return;
      if (el.closest('[data-bleed]')) return;
      const r = el.getBoundingClientRect();
      if (!r.width && !r.height) return;
      const d = Math.max(r.right - P.right, r.bottom - P.bottom, P.left - r.left, P.top - r.top);
      if (d > 1) res.push(`page ${i + 1}: ${el.tagName}.${el.className.baseVal ?? el.className} "${(el.textContent || '').trim().slice(0, 20)}" sticks out ${Math.round(d)}px`);
    });
    p.querySelectorAll('[data-name],.fit').forEach((el) => {
      if (el.tagName.toLowerCase() === 'svg' || el.closest('svg')) return;
      if (el.scrollWidth > el.clientWidth + 1 || el.scrollHeight > el.clientHeight + 1) {
        const cs = getComputedStyle(el);
        if (cs.overflow === 'visible' && !el.classList.contains('fit')) {
          // only flag a visible-overflow box if a child really leaves it
          const r = el.getBoundingClientRect(); let worst = 0;
          el.querySelectorAll('*').forEach((c) => { const b = c.getBoundingClientRect(); worst = Math.max(worst, b.right - r.right, b.bottom - r.bottom); });
          if (worst <= 2) return;
        }
        res.push(`page ${i + 1}: [${el.dataset.name || el.className}] content ${el.scrollWidth}x${el.scrollHeight} > box ${el.clientWidth}x${el.clientHeight}`);
      }
    });
  });
  return res;
}

(async () => {
  const jobs = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
  const report = [];
  const browser = await chromium.launch({ args: ['--no-sandbox', '--disable-dev-shm-usage'] });
  try {
    for (const j of jobs) {
      const rep = { id: j.id, problems: [], errors: [] };
      const ctx = await browser.newContext({ viewport: { width: Math.ceil(j.vw), height: Math.ceil(j.vh) }, deviceScaleFactor: j.scale || 1 });
      const page = await ctx.newPage();
      page.on('pageerror', (e) => rep.errors.push('pageerror: ' + e.message));
      page.on('console', (m) => { if (m.type() === 'error') rep.errors.push('console: ' + m.text()); });
      page.on('requestfailed', (r) => rep.errors.push('failed: ' + r.url()));
      page.on('dialog', (d) => d.accept());
      const url = 'file://' + j.html + (j.query ? '?' + j.query : '');
      if (j.kind === 'svgview') {
        await page.goto('file://' + j.html, { waitUntil: 'load' });
        await page.evaluate(() => document.fonts.ready);
        await page.waitForTimeout(150);
        await page.locator('svg').first().screenshot({ path: j.png });
        report.push(rep); await ctx.close(); continue;
      }
      await page.goto(url, { waitUntil: 'load' });
      await page.evaluate(() => document.fonts.ready);
      if (j.kind === 'edit') {
        // type into the first few fields, reload, and check that the text is still there; then Reset
        const fields = page.locator('#doc [contenteditable="true"]:visible');
        const n = await fields.count();
        rep.fields = n;
        const pick = [0, Math.floor(n / 2), n - 1];
        const orig0 = await fields.nth(0).textContent();
        for (const k of pick) {
          const f = fields.nth(k);
          await f.click();
          await page.keyboard.press('Control+A');
          await page.keyboard.type('Edited ' + k);
        }
        await page.waitForTimeout(800);
        const ok1 = await Promise.all(pick.map((k) => fields.nth(k).textContent()));
        const store = await page.evaluate(() => JSON.stringify(localStorage).length);
        await page.reload({ waitUntil: 'load' });
        const ok2 = await Promise.all(pick.map((k) => page.locator('#doc [contenteditable="true"]:visible').nth(k).textContent()));
        rep.edit = { typed: ok1, afterReload: ok2, storageBytes: store };
        pick.forEach((k, i) => { if (!/Edited/.test(ok1[i] || '') || !/Edited/.test(ok2[i] || '')) rep.problems.push(`edit field ${k} not kept: ${ok1[i]} / ${ok2[i]}`); });
        // add-line button, if any
        const add = page.locator('.ctl.add:visible').first();
        if (await add.count()) {
          const before = await page.locator('[data-item]:visible').count();
          await add.click();
          const after = await page.locator('[data-item]:visible').count();
          rep.edit.addLine = [before, after];
          if (after !== before + 1) rep.problems.push('add line failed');
        }
        // sync fields (same data-sync on several cards)
        if (j.sync) {
          const s = page.locator(`[data-sync="${j.sync}"]:visible`);
          const cnt = await s.count();
          await s.first().click(); await page.keyboard.press('Control+A'); await page.keyboard.type('Sync Test Club');
          await page.waitForTimeout(300);
          const all = await s.allTextContents();
          rep.edit.sync = [cnt, all.filter((t) => t === 'Sync Test Club').length];
          if (all.some((t) => t !== 'Sync Test Club')) rep.problems.push('sync failed');
        }
        await page.locator('#b-reset').click();
        await page.waitForLoadState('load');
        await page.waitForTimeout(300);
        const after = await page.locator('#doc [contenteditable="true"]:visible').nth(pick[0]).textContent();
        rep.edit.afterReset = after;
        const syncLeft = j.sync ? (await page.locator(`[data-sync="${j.sync}"]:visible`).allTextContents()).filter((t) => t === 'Sync Test Club').length : 0;
        if (after !== orig0 || syncLeft) rep.problems.push(`reset failed: ${after} / ${orig0}, sync left ${syncLeft}`);
        report.push(rep); await ctx.close(); continue;
      }
      await page.emulateMedia({ media: 'print' });
      await page.waitForTimeout(100);
      rep.problems.push(...await page.evaluate(checks, '.page'));
      const nPages = await page.locator('.page:visible').count();
      rep.pages = nPages;
      for (let i = 0; i < nPages; i++) {
        if (j.png && j.png[i]) {
          // show this page alone, so a fractional page height never lets the page above bleed into the image
          await page.evaluate((k) => { [...document.querySelectorAll('.page')].filter((p) => p.getClientRects().length || p.dataset.solo)
            .forEach((p, n) => { p.dataset.solo = '1'; p.style.display = n === k ? '' : 'none'; }); }, i);
          await page.locator('.page:visible').first().screenshot({ path: j.png[i] });
          await page.evaluate(() => document.querySelectorAll('[data-solo]').forEach((p) => { p.style.display = ''; delete p.dataset.solo; }));
        }
        if (j.svg && j.svg[i]) fs.writeFileSync(j.svg[i], await page.evaluate(toSVG, { pageSel: '.page', index: i, title: j.title || '' }));
      }
      if (j.pdf) {
        await page.goto(url + '&pdfpad=1', { waitUntil: 'load' });
        await page.evaluate(() => document.fonts.ready);
        await page.pdf({ path: j.pdf, preferCSSPageSize: true, printBackground: true });
      }
      report.push(rep);
      await ctx.close();
    }
  } finally {
    await browser.close();
  }
  fs.writeFileSync(process.argv[3], JSON.stringify(report, null, 1));
})().catch((e) => { console.error(e); process.exit(1); });
