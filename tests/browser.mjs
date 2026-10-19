import { chromium } from 'playwright';
import { spawn } from 'node:child_process';
import assert from 'node:assert/strict';
import { mkdir } from 'node:fs/promises';
const port = 18772,
  base = `http://127.0.0.1:${port}`,
  server = spawn(process.env.PYTHON || 'python3', ['-m', 'brain_breakers', 'serve', String(port)], {
    stdio: ['ignore', 'pipe', 'inherit'],
  });
let browser;
try {
  for (let i = 0; i < 100; i++) {
    try {
      if ((await fetch(base)).ok) break;
    } catch {}
    if (server.exitCode !== null) throw Error('server exited');
    if (i === 99) throw Error('server timeout');
    await new Promise((r) => setTimeout(r, 100));
  }
  browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 1400, height: 1100 } }),
    errors = [];
  page.on('pageerror', (e) => errors.push(e.message));
  for (const lang of ['fr', 'en', 'es']) {
    await page.goto(`${base}/?lang=${lang}`);
    await page.waitForFunction(() => document.getElementById('trials').textContent === '12');
    assert.equal(await page.locator('html').getAttribute('lang'), lang);
    assert.equal(await page.locator('#detected').textContent(), '12');
    assert.equal(await page.locator('#repaired').textContent(), '12');
    assert.equal(await page.locator('.trial').count(), 12);
    await page.locator('#filter').selectOption('same-answer-different-support');
    assert.equal(await page.locator('.trial').count(), 3);
    assert.ok(
      (await page.locator('.evidence.pass').first().textContent()).includes('independent-copy'),
    );
    await page.locator('#run').click();
    await page.waitForFunction(() => document.getElementById('trials').textContent === '4');
    assert.equal(await page.locator('.trial').count(), 1);
    assert.equal(await page.locator('#repaired').textContent(), '4');
    const event = page.waitForEvent('download');
    await page.locator('#download').click();
    assert.equal((await event).suggestedFilename(), 'brain-breakers-evidence.json');
  }
  await page.goto(`${base}/?lang=fr`);
  await page.waitForFunction(() => document.getElementById('trials').textContent === '12');
  await page.locator('#filter').selectOption('tenant-canary-leak');
  await mkdir('.local', { recursive: true });
  await page.screenshot({ path: '.local/preview-fr.png', fullPage: true });
  await page.setViewportSize({ width: 390, height: 844 });
  assert.equal(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), true);
  assert.deepEqual(errors, []);
  console.log(
    'FR/EN/ES: recorded three-engine proofs, live SQLite mutations, redundant support, filters, export and mobile verified.',
  );
} finally {
  if (browser) await browser.close();
  server.kill('SIGTERM');
}
