const puppeteer = require('C:\\Users\\starl\\AppData\\Roaming\\npm\\node_modules\\@modelcontextprotocol\\server-puppeteer\\node_modules\\puppeteer');
const API = 'http://localhost:5000/api';

async function api(method, path, body) {
  const r = await fetch(API + path, { method, headers: { 'Content-Type': 'application/json' }, body: body ? JSON.stringify(body) : undefined });
  return r.json();
}

(async () => {
  const results = [];
  const check = (name, ok, detail) => { results.push((ok ? 'PASS ' : 'FAIL ') + name + (ok ? '' : ' :: ' + detail)); };

  // seed an XSS team + a milestone so we can verify escaping
  const members = Array.from({ length: 6 }, (_, i) => ({ name: 'M' + i, gender: i === 0 ? 'female' : 'male', email: 'm' + i + '@x.edu' }));
  const xss = await api('POST', '/teams', { teamName: '<img src=x onerror=window.__pwned=1>', leadEmail: 'xss@x.edu', members });
  check('xss team created', !!xss.id, JSON.stringify(xss).slice(0, 100));
  await api('POST', '/milestones', { name: '<b>bold-name</b>', date: '2026-12-25' });

  const browser = await puppeteer.launch({ headless: 'new', args: ['--no-sandbox'], executablePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe' });
  const pages = ['index.html', 'teams.html', 'ps.html', 'mentors.html', 'deliverables.html'];

  for (const width of [390, 1280]) {
    for (const page of pages) {
      const p = await browser.newPage();
      await p.setViewport({ width, height: width === 390 ? 844 : 900 });
      const errors = [];
      p.on('pageerror', e => errors.push('pageerror: ' + e.message));
      p.on('console', m => { if (m.type() === 'error') errors.push('console: ' + m.text()); });
      await p.evaluateOnNewDocument(() => { window.__pwned = 0; });
      await p.goto('file:///C:/Users/starl/woxsen/SEM%205/Fullstack%20(notes)/sih-command-center/frontend/' + page, { waitUntil: 'networkidle0', timeout: 20000 });
      await new Promise(r => setTimeout(r, 800));

      const tag = width + 'px ' + page;
      const pwned = await p.evaluate(() => window.__pwned);
      check(tag + ': no XSS executed', !pwned, 'onerror handler fired');
      check(tag + ': no JS errors', errors.length === 0, errors.join(' | ').slice(0, 200));
      const bodyText = await p.evaluate(() => document.body.innerText);
      check(tag + ': page has content', bodyText.length > 100, 'len=' + bodyText.length);
      const hscroll = await p.evaluate(() => document.documentElement.scrollWidth > window.innerWidth + 1);
      if (width === 390) check(tag + ': no horizontal scroll @390px', !hscroll, 'scrollWidth > innerWidth');
      await p.close();
    }
  }

  // interaction test: register team through the actual UI
  const p = await browser.newPage();
  await p.setViewport({ width: 1280, height: 900 });
  const errors = [];
  p.on('pageerror', e => errors.push(e.message));
  await p.goto('file:///C:/Users/starl/woxsen/SEM%205/Fullstack%20(notes)/sih-command-center/frontend/teams.html', { waitUntil: 'networkidle0' });
  await p.type('#tn', 'UI Bot Team');
  await p.type('#le', 'uibot@woxsen.edu');
  await p.click('#box1 button');
  await new Promise(r => setTimeout(r, 300));
  for (let i = 0; i < 6; i++) await p.type('#n' + i, 'Bot' + i);
  await p.select('#g0', 'female');
  for (let i = 0; i < 6; i++) await p.type('#e' + i, 'bot' + i + '@woxsen.edu');
  await p.click('#box2 button:last-of-type');
  await new Promise(r => setTimeout(r, 800));
  const doneText = await p.evaluate(() => document.getElementById('doneBody').textContent + ' ' + document.getElementById('m2').textContent);
  check('UI: team registered end-to-end', doneText.includes('is valid') || doneText.includes('composition'), doneText.slice(0, 120));
  check('UI: no page errors during flow', errors.length === 0, errors.join(' | ').slice(0, 150));
  await p.close();

  await browser.close();
  results.forEach(r => console.log(r));
  const fails = results.filter(r => r.startsWith('FAIL')).length;
  console.log('==== BROWSER RESULT: ' + (results.length - fails) + ' passed, ' + fails + ' failed ====');
  process.exit(0);
})().catch(e => { console.error('FATAL', e); process.exit(1); });
