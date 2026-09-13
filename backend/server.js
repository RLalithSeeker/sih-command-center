// SIH Command Center backend - kept in one file on purpose (easy viva explanation)
// ponytail: single file, split into routes/ when teams > 10
const express = require('express');
const cors = require('cors');
const mongoose = require('mongoose');

const app = express();
app.use(cors());
app.use(express.json());
const PORT = process.env.PORT || 5000;

// ---------- schemas (used when MONGO_URI is set) ----------
const teamSchema = new mongoose.Schema({
  teamName: String, leadEmail: String,
  members: [{ name: String, gender: String, email: String }],
  psId: { type: String, default: null }, mentorId: { type: String, default: null },
  createdAt: { type: Date, default: Date.now }
});
const Team = mongoose.model('Team', teamSchema);

// ---------- in-memory store (default for demo) ----------
let useDb = false;
const db = { teams: [], ps: [], mentors: [], deliverables: [] };
let nextId = 100; // starts above seed ids (t1, ps1, m1) so new teams never collide
const nid = (p) => p + (nextId++);

function seed() {
  db.ps = [
    { id: 'ps1', code: 'SIH001', sihId: 'SIH25001', title: 'Campus grievance portal', category: 'software', org: 'AICTE' },
    { id: 'ps2', code: 'SIH002', sihId: 'SIH25002', title: 'Smart classroom attendance', category: 'software', org: 'MoE' },
    { id: 'ps3', code: 'SIH003', sihId: 'SIH25123', title: 'Low-cost soil sensor', category: 'hardware', org: 'MoA' }
  ];
  db.mentors = [
    { id: 'm1', name: 'Dr. Rao', dept: 'CSE', email: 'rao@woxsen.edu', maxTeams: 3 },
    { id: 'm2', name: 'Prof. Iyer', dept: 'ECE', email: 'iyer@woxsen.edu', maxTeams: 2 }
  ];
  db.teams = [{
    id: 't1', teamName: 'Demo Spartans', leadEmail: 'lead@woxsen.edu',
    psId: 'ps1', mentorId: 'm1',
    members: [
      { name: 'Asha', gender: 'female', email: 'a@woxsen.edu' },
      { name: 'Ravi', gender: 'male', email: 'b@woxsen.edu' },
      { name: 'Kiran', gender: 'male', email: 'c@woxsen.edu' },
      { name: 'Divya', gender: 'female', email: 'd@woxsen.edu' },
      { name: 'Arjun', gender: 'male', email: 'e@woxsen.edu' },
      { name: 'Meena', gender: 'female', email: 'f@woxsen.edu' }
    ]
  }];
  db.deliverables = [
    { teamId: 't1', type: 'github', link: 'https://github.com/demo/spartans', status: 'approved' },
    { teamId: 't1', type: 'ppt', link: 'https://drive/demo.pptx', status: 'submitted' },
    { teamId: 't1', type: 'video', link: '', status: 'not_submitted' },
    { teamId: 't1', type: 'report', link: '', status: 'not_submitted' }
  ];
}

// validation used by both stores
function checkComposition(members) {
  if (!members || members.length !== 6) return 'Team must have exactly 6 members';
  const hasFemale = members.some(m => (m.gender || '').toLowerCase() === 'female');
  if (!hasFemale) return 'At least 1 female member is mandatory (SIH rule)';
  return null;
}

function clean(s) { return (s || '').trim(); }

function mentorLoad(id) { return db.teams.filter(t => t.mentorId === id).length; }

function leastLoadedMentor() {
  const free = db.mentors.filter(m => mentorLoad(m.id) < m.maxTeams);
  free.sort((a, b) => mentorLoad(a.id) - mentorLoad(b.id));
  return free[0] || null;
}

function readiness(team) {
  const d = db.deliverables.filter(x => x.teamId === team.id);
  const approved = d.filter(x => x.status === 'approved').length;
  let score = Math.round(approved / 4 * 100);
  if (checkComposition(team.members)) score -= 25;
  if (!team.mentorId) score -= 25;
  return Math.max(score, 0);
}

function teamView(t) {
  const ps = db.ps.find(p => p.id === t.psId);
  const mentor = db.mentors.find(m => m.id === t.mentorId);
  const d = db.deliverables.filter(x => x.teamId === t.id);
  return {
    ...t, psTitle: ps ? (ps.sihId || ps.code) + ' - ' + ps.title : 'Not selected',
    mentorName: mentor ? mentor.name : 'Not assigned',
    compositionError: checkComposition(t.members),
    deliverables: d, readiness: readiness(t)
  };
}

// ---------- routes ----------
app.get('/api/health', (req, res) => res.json({ ok: true, mode: useDb ? 'mongo' : 'memory' }));

app.get('/api/ps', (req, res) => {
  const q = clean(req.query.q).toLowerCase();
  let list = db.ps.map(p => {
    const holder = db.teams.find(t => t.psId === p.id);
    return { ...p, takenBy: holder ? holder.teamName : null };
  });
  if (q) list = list.filter(p => ((p.sihId || '') + ' ' + p.code + ' ' + p.title + ' ' + p.org).toLowerCase().includes(q));
  res.json(list);
});
app.post('/api/ps', (req, res) => {
  const { code, title, category, org, sihId } = req.body;
  if (!code || !title) return res.status(400).json({ error: 'code and title required' });
  const ps = { id: nid('ps'), code: clean(code), sihId: clean(sihId), title: clean(title), category: clean(category).toLowerCase() || 'software', org: clean(org) || 'SIH' };
  db.ps.push(ps);
  mongoSave(); res.json(ps);
});
app.post('/api/ps/bulk', (req, res) => {
  // paste lines copied from sih.gov.in: SIHID | title | software/hardware | org
  const lines = (req.body.lines || '').split('\n').map(l => l.trim()).filter(Boolean);
  let added = 0;
  lines.forEach((l, i) => {
    const parts = l.split('|').map(s => s.trim());
    if (parts.length < 2) return;
    const [sihId, title, category, org] = parts;
    if (db.ps.find(p => (p.sihId || '').toLowerCase() === sihId.toLowerCase())) return;
    db.ps.push({ id: nid('ps'), code: 'SIH' + String(100 + db.ps.length + i), sihId, title, category: (category || 'software').toLowerCase(), org: org || 'SIH' });
    added++;
  });
  mongoSave(); res.json({ added, total: db.ps.length });
});

app.get('/api/mentors', (req, res) => {
  const out = db.mentors.map(m => ({
    ...m, load: db.teams.filter(t => t.mentorId === m.id).length
  }));
  res.json(out);
});
app.post('/api/mentors', (req, res) => {
  const { name, dept, email } = req.body;
  if (!name) return res.status(400).json({ error: 'name required' });
  const m = { id: nid('m'), name, dept: dept || 'CSE', email: email || '', maxTeams: 3 };
  db.mentors.push(m);
  mongoSave(); res.json(m);
});

app.get('/api/teams', (req, res) => res.json(db.teams.map(teamView)));

app.get('/api/teams/:id', (req, res) => {
  const t = db.teams.find(x => x.id === req.params.id);
  if (!t) return res.status(404).json({ error: 'team not found' });
  mongoSave(); res.json(teamView(t));
});

app.post('/api/teams', async (req, res) => {
  let { teamName, leadEmail, members } = req.body;
  teamName = clean(teamName); leadEmail = clean(leadEmail).toLowerCase();
  if (!teamName || !leadEmail) return res.status(400).json({ error: 'teamName and leadEmail required' });
  members = (members || []).map(m => ({ name: clean(m.name), gender: clean(m.gender).toLowerCase(), email: clean(m.email).toLowerCase() }));
  const err = checkComposition(members);
  if (err) return res.status(400).json({ error: err }); // hard block, per PBL spec
  const t = { id: nid('t'), teamName, leadEmail, members, psId: null, mentorId: null };
  db.teams.push(t);
  ['github', 'ppt', 'video', 'report'].forEach(type =>
    db.deliverables.push({ teamId: t.id, type, link: '', status: 'not_submitted' }));
  mongoSave(); res.json(teamView(t));
});

app.post('/api/teams/:id/select-ps', (req, res) => {
  const t = db.teams.find(x => x.id === req.params.id);
  if (!t) return res.status(404).json({ error: 'team not found' });
  const { psId, allowDuplicate } = req.body;
  if (!db.ps.find(p => p.id === psId)) return res.status(400).json({ error: 'invalid PS' });
  const taken = db.teams.find(x => x.psId === psId && x.id !== t.id);
  if (taken && !allowDuplicate) return res.status(400).json({ error: `Already taken by ${taken.teamName}. Tick allowDuplicate to override.` });
  t.psId = psId;
  mongoSave(); res.json(teamView(t));
});

app.post('/api/teams/:id/assign-mentor', (req, res) => {
  const t = db.teams.find(x => x.id === req.params.id);
  if (!t) return res.status(404).json({ error: 'team not found' });
  const m = db.mentors.find(x => x.id === req.body.mentorId);
  if (!m) return res.status(400).json({ error: 'invalid mentor' });
  const load = db.teams.filter(x => x.mentorId === m.id && x.id !== t.id).length;
  if (load >= m.maxTeams) return res.status(400).json({ error: `${m.name} already has ${load} teams (max ${m.maxTeams})` });
  t.mentorId = m.id;
  mongoSave(); res.json(teamView(t));
});

app.post('/api/teams/:id/auto-mentor', (req, res) => {
  const t = db.teams.find(x => x.id === req.params.id);
  if (!t) return res.status(404).json({ error: 'team not found' });
  if (t.mentorId) return res.json(teamView(t));
  const m = leastLoadedMentor();
  if (!m) return res.status(400).json({ error: 'All mentors are full' });
  t.mentorId = m.id;
  mongoSave(); res.json(teamView(t));
});

app.get('/api/deliverables/:teamId', (req, res) =>
  res.json(db.deliverables.filter(d => d.teamId === req.params.teamId)));

app.put('/api/deliverables/:teamId', (req, res) => {
  // body: { type, link, status }
  const { type, link, status } = req.body;
  const d = db.deliverables.find(x => x.teamId === req.params.teamId && x.type === type);
  if (!d) return res.status(404).json({ error: 'not found' });
  const ok = ['not_submitted', 'submitted', 'needs_revision', 'approved'];
  if (status && !ok.includes(status)) return res.status(400).json({ error: 'bad status' });
  if (link !== undefined) d.link = link;
  if (status) d.status = status;
  mongoSave(); res.json(d);
});

app.get('/api/dashboard', (req, res) => {
  const { mentor, category, status } = req.query;
  let teams = db.teams.map(teamView);
  if (mentor) teams = teams.filter(t => t.mentorId === mentor);
  if (category) teams = teams.filter(t => {
    const ps = db.ps.find(p => p.id === t.psId);
    return ps && ps.category === category;
  });
  if (status === 'pending') teams = teams.filter(t => t.readiness < 100);
  if (status === 'ready') teams = teams.filter(t => t.readiness === 100);
  const pendingReminders = teams
    .filter(t => t.readiness < 100)
    .map(t => ({ team: t.teamName, lead: t.leadEmail, missing: t.deliverables.filter(d => d.status !== 'approved').map(d => d.type) }));
  res.json({ teams, pendingReminders, total: teams.length });
});

app.get('/api/export.csv', (req, res) => {
  const rows = [['Team', 'PS', 'Mentor', 'Readiness', 'Composition', 'Pending deliverables']];
  db.teams.map(teamView).forEach(t => {
    rows.push([t.teamName, t.psTitle, t.mentorName, t.readiness + '%',
      t.compositionError || 'OK',
      t.deliverables.filter(d => d.status !== 'approved').map(d => d.type).join('|') || 'none']);
  });
  res.header('Content-Type', 'text/csv');
  res.send(rows.map(r => r.map(c => `"${c}"`).join(',')).join('\n'));
});

app.get('/api/report.html', (req, res) => {
  const rows = db.teams.map(teamView).map(t =>
    `<tr><td>${t.teamName}</td><td>${t.psTitle}</td><td>${t.mentorName}</td><td>${t.readiness}%</td><td>${t.compositionError || 'OK'}</td><td>${t.deliverables.map(d => d.type + ': ' + d.status).join('<br>')}</td></tr>`
  ).join('');
  res.header('Content-Type', 'text/html');
  res.send(`<!doctype html><html><head><meta charset="utf-8"><title>SIH Status Report</title>
<style>body{font-family:Arial;margin:24px}table{width:100%;border-collapse:collapse}th,td{border:1px solid #999;padding:6px;font-size:13px}@media print{button{display:none}}</style>
</head><body><h2>SIH Command Center – Consolidated Status (${new Date().toLocaleDateString('en-IN')})</h2>
<button onclick="window.print()">Print / Save as PDF</button><br><br>
<table><tr><th>Team</th><th>Problem Statement</th><th>Mentor</th><th>Ready</th><th>Team check</th><th>Deliverables</th></tr>${rows}</table>
<p>Generated for institute records / nodal centre.</p></body></html>`);
});

const Doc = mongoose.model('Doc', new mongoose.Schema({ key: String, data: mongoose.Schema.Types.Mixed }));

async function mongoLoad() {
  const docs = await Doc.find({});
  docs.forEach(d => { if (db[d.key]) db[d.key] = d.data; });
  if (!db.ps.length) seed();
  const maxNum = s => Math.max(0, ...['teams', 'ps', 'mentors'].flatMap(k => (db[k] || []).map(x => parseInt((x.id || '').replace(/\D/g, '')) || 0)));
  nextId = Math.max(nextId, maxNum() + 1);
}

function mongoSave() {
  if (!useDb) return;
  Object.keys(db).forEach(k => Doc.updateOne({ key: k }, { key: k, data: db[k] }, { upsert: true }).exec().catch(() => {}));
}

async function start() {
  seed();
  if (process.env.MONGO_URI) {
    try {
      await mongoose.connect(process.env.MONGO_URI);
      useDb = true;
      await mongoLoad();
      console.log('Mongo connected, data loaded');
    } catch (e) { console.log('Mongo failed, using memory:', e.message); }
  }
  app.listen(PORT, () => console.log(`SIH backend on http://localhost:${PORT} (${useDb ? 'mongo' : 'memory'})`));
}
start();
