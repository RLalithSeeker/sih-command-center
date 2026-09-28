// shared helper
const API = 'http://localhost:5000/api';
// escape user-supplied text before it goes into innerHTML (prevents stored XSS)
function esc(s) {
  return String(s == null ? '' : s).replace(/[&<>"']/g, c =>
    ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
}
async function get(p) {
  const r = await fetch(API + p);
  const j = await r.json();
  if (!r.ok) throw new Error(j.error || 'request failed');
  return j;
}
async function post(p, body) {
  const r = await fetch(API + p, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) });
  const j = await r.json(); if (!r.ok) throw new Error(j.error || 'failed'); return j;
}
async function put(p, body) {
  const r = await fetch(API + p, { method: 'PUT', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) });
  const j = await r.json(); if (!r.ok) throw new Error(j.error || 'failed'); return j;
}
// show a friendly message when the backend is unreachable or a load fails
function loadFailed(id, e) {
  const el = document.getElementById(id);
  if (el) el.innerHTML = '<p class="hint">Could not reach the backend at localhost:5000. Start it with run.bat, then refresh. <br><small>' + esc(e.message) + '</small></p>';
}
// readiness ring: dial(pct) -> inline SVG gauge. Colour follows score.
function dial(pct) {
  const p = Math.max(0, Math.min(100, +pct || 0));
  const col = p === 100 ? '#2F7D4F' : p >= 50 ? '#A96B1B' : '#B3352B';
  const C = 2 * Math.PI * 26;
  const off = C * (1 - p / 100);
  return `<span class="dial" role="img" aria-label="readiness ${p} percent">` +
    `<svg width="64" height="64" viewBox="0 0 64 64"><circle class="dial-track" cx="32" cy="32" r="26" fill="none" stroke-width="7"/>` +
    `<circle class="dial-fill" cx="32" cy="32" r="26" fill="none" stroke="${col}" stroke-width="7" stroke-dasharray="${C.toFixed(1)}" stroke-dashoffset="${off.toFixed(1)}"/></svg>` +
    `<span class="dial-num num">${p}</span></span>`;
}
// friendly empty table row
function emptyRow(cols, msg) { return `<tr><td colspan="${cols}"><p class="mutes" style="margin:4px 0">${esc(msg)}</p></td></tr>`; }
// toast: showFlash('Team saved') -> transient notice top of page
function showFlash(msg, kind) {
  let box = document.getElementById('flash');
  if (!box) {
    box = document.createElement('div');
    box.id = 'flash';
    box.style.cssText = 'position:fixed;top:14px;left:50%;transform:translateX(-50%);z-index:200;max-width:min(92vw,480px)';
    document.body.appendChild(box);
  }
  const el = document.createElement('div');
  el.style.cssText = 'background:#1E2A4A;color:#fff;padding:10px 16px;border-radius:10px;border-left:4px solid ' + (kind === 'bad' ? '#E0665E' : '#A96B1B') + ';box-shadow:0 4px 16px rgba(0,0,0,.2);margin-bottom:8px;font-size:14px';
  el.textContent = msg;
  box.appendChild(el);
  setTimeout(() => el.remove(), 3200);
}
