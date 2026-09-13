// shared helper
const API = 'http://localhost:5000/api';
async function get(p) { const r = await fetch(API + p); return r.json(); }
async function post(p, body) {
  const r = await fetch(API + p, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) });
  const j = await r.json(); if (!r.ok) throw new Error(j.error || 'failed'); return j;
}
async function put(p, body) {
  const r = await fetch(API + p, { method: 'PUT', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) });
  const j = await r.json(); if (!r.ok) throw new Error(j.error || 'failed'); return j;
}
