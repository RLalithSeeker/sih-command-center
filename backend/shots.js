// Clean phase-by-phase screenshots for the PPT (read-only, no data mutations)
const puppeteer = require('C:\\Users\\starl\\AppData\\Roaming\\npm\\node_modules\\@modelcontextprotocol\\server-puppeteer\\node_modules\\puppeteer');
const fs = require('fs');
const BASE = 'http://localhost:8080/';
const OUT = 'C:\\Users\\starl\\woxsen\\SEM 5\\Fullstack (notes)\\sih-command-center\\report\\shots\\';
const sleep = ms => new Promise(r => setTimeout(r, ms));

(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const browser = await puppeteer.launch({ headless: 'new', args: ['--no-sandbox'], executablePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe' });
  const shot = async (name, fn, w = 1280, h = 900) => {
    const p = await browser.newPage();
    await p.setViewport({ width: w, height: h });
    const errs = [];
    p.on('pageerror', e => errs.push(e.message));
    await p.goto(fn && fn.page && fn.page.startsWith('http') ? fn.page : BASE + (fn ? fn.page : ''), { waitUntil: 'networkidle0' });
    await sleep(800);
    if (fn && fn.act) await fn.act(p);
    await sleep(600);
    await p.screenshot({ path: OUT + name + '.png', fullPage: !!(fn && fn.full) });
    console.log((errs.length ? 'ERR ' + errs.join('|') : 'ok  ') + ' ' + name);
    await p.close();
  };

  // 1. Dashboard — deadlines + filter + team with readiness dial
  await shot('phase1-dashboard');

  // 2. Dashboard — filtered: Status = Ready (URL-persisted filters)
  await shot('phase2-dashboard-filtered', { page: 'index.html?status=ready' });

  // 3. Teams — registration wizard step 1
  await shot('phase3-team-step1', { page: 'teams.html' });

  // 4. Teams — step 2 members form (client-side only, no submit)
  await shot('phase4-team-step2', { page: 'teams.html', act: p => p.evaluate(() => go(2)) });

  // 5. PS page — search "25001" with result rows visible
  await shot('phase5-ps-search', {
    page: 'ps.html',
    act: async p => {
      await p.click('#q');
      await p.type('#q', '25001', { delay: 40 });
      // close any focused native select popup + leave focus neutral for the shot
      await p.keyboard.press('Escape');
      await p.evaluate(() => { if (document.activeElement && document.activeElement.blur) document.activeElement.blur(); });
      const sample = await p.evaluate(() => Array.from(document.getElementById('psSel').options).slice(0, 3).map(o => o.text));
      console.log('  picker sample: ' + JSON.stringify(sample));
    }
  });

  // 6. Mentors — load table + assignment card
  await shot('phase6-mentors', { page: 'mentors.html' });

  // 7. Deliverables — Demo Spartans 4-item table + status chips
  await shot('phase7-deliverables', { page: 'deliverables.html' });

  // 8. Printable report (backend export)
  await shot('phase8-printable-report', { page: 'http://localhost:5000/api/report.html', full: true });

  // 9. Mobile proof shot
  await shot('phase9-mobile-dashboard', { page: 'index.html' }, 390, 844);

  await browser.close();
})().catch(e => { console.error('FATAL', e); process.exit(1); });
