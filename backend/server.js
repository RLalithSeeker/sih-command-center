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
let nextId = 1;
const nid = (p) => p + (nextId++);

function seed() {
  db.ps = [
    { id: 'ps1', code: 'SIH001', title: 'Campus grievance portal', category: 'software', org: 'AICTE' },
    { id: 'ps2', code: 'SIH002', title: 'Smart classroom attendance', category: 'software', org: 'MoE' },
    { id: 'ps3', code: 'SIH003', title: 'Low-cost soil sensor', category: 'hardware', org: 'MoA' }
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
    ...t, psTitle: ps ? ps.code + ' - ' + ps.title : 'Not selected',
    mentorName: mentor ? mentor.name : 'Not assigned',
    compositionError: checkComposition(t.members),
    deliverables: d, readiness: readiness(t)
  };
}

// ---------- routes ----------
app.get('/api/health', (req, res) => res.json({ ok: true, mode: useDb ? 'mongo' : 'memory' }));

app.get('/api/ps', (req, res) => res.json(db.ps));
app.post('/api/ps', (req, res) => {
  const { code, title, category, org } = req.body;
  if (!code || !title) return res.status(400).json({ error: 'code and title required' });
  const ps = { id: nid('ps'), code, title, category: category || 'software', org: org || 'SIH' };
  db.ps.push(ps);
  res.json(ps);
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
  res.json(m);
});

app.get('/api/teams', (req, res) => res.json(db.teams.map(teamView)));

app.post('/api/teams', async (req, res) => {
  const { teamName, leadEmail, members } = req.body;
  if (!teamName || !leadEmail) return res.status(400).json({ error: 'teamName and leadEmail required' });
  const err = checkComposition(members);
  if (err) return res.status(400).json({ error: err }); // hard block, per PBL spec
  const t = { id: nid('t'), teamName, leadEmail, members, psId: null, mentorId: null };
  db.teams.push(t);
  ['github', 'ppt', 'video', 'report'].forEach(type =>
    db.deliverables.push({ teamId: t.id, type, link: '', status: 'not_submitted' }));
  if (useDb) await Team.create({ ...t, _id: undefined });
  res.json(teamView(t));
});

app.post('/api/teams/:id/select-ps', (req, res) => {
  const t = db.teams.find(x => x.id === req.params.id);
  if (!t) return res.status(404).json({ error: 'team not found' });
  const { psId, allowDuplicate } = req.body;
  if (!db.ps.find(p => p.id === psId)) return res.status(400).json({ error: 'invalid PS' });
  const taken = db.teams.find(x => x.psId === psId && x.id !== t.id);
  if (taken && !allowDuplicate) return res.status(400).json({ error: `Already taken by ${taken.teamName}. Tick allowDuplicate to override.` });
  t.psId = psId;
  res.json(teamView(t));
});

app.post('/api/teams/:id/assign-mentor', (req, res) => {
  const t = db.teams.find(x => x.id === req.params.id);
  if (!t) return res.status(404).json({ error: 'team not found' });
  const m = db.mentors.find(x => x.id === req.body.mentorId);
  if (!m) return res.status(400).json({ error: 'invalid mentor' });
  const load = db.teams.filter(x => x.mentorId === m.id && x.id !== t.id).length;
  if (load >= m.maxTeams) return res.status(400).json({ error: `${m.name} already has ${load} teams (max ${m.maxTeams})` });
  t.mentorId = m.id;
  res.json(teamView(t));
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
  res.json(d);
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

async function start() {
  seed();
  if (process.env.MONGO_URI) {
    try { await mongoose.connect(process.env.MONGO_URI); useDb = true; console.log('Mongo connected'); }
    catch (e) { console.log('Mongo failed, using memory:', e.message); }
  }
  app.listen(PORT, () => console.log(`SIH backend on http://localhost:${PORT} (${useDb ? 'mongo' : 'memory'})`));
}
start();
