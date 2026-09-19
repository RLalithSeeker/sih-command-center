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
