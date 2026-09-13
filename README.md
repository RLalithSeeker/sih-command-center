# SIH Command Center – Hackathon Team & Deliverable Tracking (PBL 14)

Woxsen University | Full Stack Development (24TU05MJC1) | MERN

SPOC tracks SIH teams across sheets/emails and misses invalid teams,
unassigned mentors, pending deliverables. This app centralises it.

Features (per PBL): 6-member team validation (min 1 female), PS catalog
(software/hardware + org), mentor assignment, deliverable tracker
(GitHub/PPT/video/report), readiness %, reminders, export.

## Run (works without Mongo)
```
cd backend
npm install
npm start
```
Open `frontend/index.html` in browser. API at http://localhost:5000.
With Mongo: copy backend/.env.example to backend/.env and set MONGO_URI.

## Structure
backend/ – Express APIs + Mongoose models (falls back to in-memory + seed)
frontend/ – plain HTML/CSS/JS (student-style, no build step)
docs/ – Review-1 material, report/ – final report, ppt/ – slides outline

## Team
See TEAM.md.
