const { chromium, devices } = require('playwright');
const fs = require('fs');
const urls = fs.readFileSync(process.argv[2], 'utf8').trim().split('\n');
const outDir = process.argv[3];
(async () => {
  const browser = await chromium.launch();
  const results = [];
  const queue = [...urls];
  async function worker() {
    while (queue.length) {
      const url = queue.shift();
      const ctx = await browser.newContext({ ...devices['iPhone 13'], ignoreHTTPSErrors: true });
      const page = await ctx.newPage();
      let bytes = 0;
      page.on('response', async r => { const l = r.headers()['content-length']; if (l) bytes += +l; });
      const r = { url };
      try {
        const t0 = Date.now();
        const resp = await page.goto(url, { waitUntil: 'load', timeout: 30000 });
        r.loadMs = Date.now() - t0;
        r.status = resp && resp.status();
        r.finalUrl = page.url();
        await page.waitForTimeout(1500);
        Object.assign(r, await page.evaluate(() => {
          const txt = document.body ? document.body.innerText : '';
          const html = document.documentElement.outerHTML;
          const years = (txt.match(/(?:©|copyright|&copy;)\s*(?:\d{4}\s*[-–]\s*)?(\d{4})/gi) || []).map(s => +s.match(/(\d{4})(?!.*\d{4})/)[1]);
          const gen = document.querySelector('meta[name=generator]');
          return {
            title: document.title.slice(0, 80),
            viewport: !!document.querySelector('meta[name=viewport]'),
            overflowPx: document.documentElement.scrollWidth - window.innerWidth,
            copyright: years.length ? Math.max(...years) : null,
            telLink: !!document.querySelector('a[href^="tel:"]'),
            form: !!document.querySelector('form input[type=email], form textarea, form input[type=tel]'),
            reviews: /review|testimonial|★|stars?\b/i.test(txt),
            words: txt.split(/\s+/).length,
            tables: document.querySelectorAll('table').length,
            flash: /\.swf|shockwave/i.test(html),
            generator: gen ? gen.content.slice(0, 40) : '',
            smallText: [...document.querySelectorAll('p,li,td,span')].slice(0,200).filter(e => parseFloat(getComputedStyle(e).fontSize) < 12 && e.innerText.trim().length > 20).length,
          };
        }));
        r.kb = Math.round(bytes / 1024);
        const name = new URL(url).hostname.replace(/^www\./, '');
        await page.screenshot({ path: `${outDir}/${name}.png` });
      } catch (e) { r.error = e.message.split('\n')[0].slice(0, 100); }
      results.push(r); await ctx.close();
    }
  }
  await Promise.all(Array.from({ length: 6 }, worker));
  await browser.close();
  fs.writeFileSync(`${outDir}/../results.json`, JSON.stringify(results, null, 1));
})();
