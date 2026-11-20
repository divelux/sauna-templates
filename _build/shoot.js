// Photographs the #shot element of each HTML file. One Chromium for the whole batch, closed right away.
// Run only under the shared lock:
//   NODE_PATH=/opt/carmax/node_modules flock /tmp/freebies-chromium.lock node shoot.js jobs.json
const { chromium } = require('playwright');
const fs = require('fs');

(async () => {
  const jobs = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
  const browser = await chromium.launch();
  try {
    const page = await browser.newPage({ viewport: { width: 2600, height: 1400 }, deviceScaleFactor: 1 });
    for (const j of jobs) {
      await page.goto('file://' + j.html, { waitUntil: 'load' });
      await page.evaluate(() => document.fonts.ready);
      await page.locator('#shot').screenshot({ path: j.png });
    }
  } finally {
    await browser.close();
  }
})().catch((e) => { console.error(e); process.exit(1); });
