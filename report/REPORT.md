# SIH Command Center – Project Report (PBL 14)

Course: Full Stack Development (24TU05MJC1), Woxsen University.
Team of 4: full-stack lead, frontend, backend, QA+docs. Stack: MongoDB
(optional), Express, plain HTML/CSS/JS frontend (React-equivalent UI without
build step for college PCs), Node, Git.

## 1. Problem + objectives
SPOC tracked SIH teams in sheets/emails; invalid teams and pending
deliverables surfaced too late. Objectives: (1) registration blocking
non-6 / no-female teams, (2) PS catalog with duplicate check, (3) mentor
assignment with load view, (4) deliverable tracker + readiness %, (5) filterable
dashboard + CSV export. (Detail: docs/01.)

## 2. Design + methodology
Express REST + Mongo-or-memory, 5 pages, one CSS. Entities: Team, PS, Mentor,
Deliverable. Readiness = approved/4*100 − penalties. Weekly plan: W1 req+design,
W2 backend, W3 frontend, W4 testing+report. (Detail: docs/02, per-person
choices: docs/03.)

## 3. Implementation (what we actually did, phase-wise)
- Phase 1: scaffold + docs, git root commit.
- Phase 2 (backend): server.js – 10 routes, checkComposition(), readiness(),
  seed (3 PS, 2 mentors, demo team), /export.csv. In-memory default so review
  demo runs offline; MONGO_URI switches to real DB.
- Phase 3 (frontend): index (dashboard+filters+reminders), teams (6-row form),
  ps, mentors, deliverables; shared app.js fetch helpers; navy theme for
  projector readability.
- Phase 4 (QA): 17 manual cases, 2 bugs fixed (04-test-plan.md).

## 4. Analysis / results
Demo data: 1 seed team + 2 we registered in testing. Readiness correctly shows
25% for team with 1/4 approved; invalid-team and mentor-less penalties verified.
CSV opens in Excel for nodal-centre record. Limitation: no real email (reminder
list shown instead), mentor view read-only, filters don't persist.

## 5. Conclusion + future work
Meets all 8 PBL features in working form. Next: real auth + email, mentor login,
PDF export. Each member can demo own part (see TEAM.md + 03-dev-notes.md).

## Screenshots (QA to paste before print)
1. Dashboard with readiness 2. Teams page valid/invalid message
3. PS duplicate error 4. Mentor load 5. CSV in Excel
