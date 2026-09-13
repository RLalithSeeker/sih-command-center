# Review 1 – Design & Methodology (5M)

## Architecture
Simple MERN, no build tools so anyone can run it:
Browser (HTML/CSS/JS fetch) → Express REST (port 5000) → MongoDB (or
in-memory fallback with same API). Seed file loads 3 PS + 2 mentors + 1 demo team.

## Data model
- Team: teamName, leadEmail, members[6]{name, gender, email}, psId, mentorId, createdAt
  rule: members.length == 6 AND at least one gender == 'female'
- ProblemStatement: code (e.g. SIH001), title, category (software/hardware), org
- Mentor: name, dept, email, maxTeams (default 3)
- Deliverable: teamId, type (github/ppt/video/report), link, status
  (not_submitted/submitted/needs_revision/approved), updatedAt

## Readiness %
readiness = approved/4 * 100 minus penalty: -25 if invalid composition,
-25 if no mentor. Simple enough to explain in viva.

## API list (10 routes, kept small on purpose)
POST /api/teams, GET /api/teams, GET /api/teams/:id
POST /api/teams/:id/select-ps, POST /api/teams/:id/assign-mentor
GET/POST /api/ps, GET /api/mentors, POST /api/mentors
GET/PUT /api/deliverables/:teamId, GET /api/dashboard, GET /api/export.csv

## Pages (5)
index (dashboard), teams (register + list), ps (catalog), mentors, deliverables.
One CSS file. Kept plain so it looks student-made.

## Methodology
Week 1 req + design, Week 2 backend, Week 3 frontend, Week 4 testing + report.
Git: one commit per phase-step, prefixed by role.
Testing: manual test table (docs/04-test-plan.md) + basic API checks.
