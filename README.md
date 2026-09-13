# SIH Command Center – Hackathon Team & Deliverable Tracking (PBL 14)

Woxsen University | Full Stack Development (24TU05MJC1) | MERN

SPOC tracks SIH teams across sheets/emails and misses invalid teams,
unassigned mentors, pending deliverables. This app centralises it.

Features (per PBL): 6-member team validation (min 1 female), official SIH
catalog (one-click scrape from sih.gov.in + search by SIH number + duplicate
check), mentor assignment (load view + auto-assign), deliverable tracker
(GitHub/PPT/video/report), readiness %, milestone deadline countdowns,
pending reminders, CSV + printable PDF export.

## Run (works without Mongo – double-click run.bat on college PCs)
```
cd backend
npm install
npm start
```
Open `frontend/index.html` in browser. API at http://localhost:5000.
With Mongo: create backend/.env with `MONGO_URI=mongodb://…/sih`
(format in backend/config-example.txt). Empty = in-memory demo mode.

## Structure
backend/server.js – Express APIs (memory-first, Mongo persist if configured)
frontend/ – 5 guided pages, one CSS file, no build step
docs/ – Review-1 docs, test plan, viva Q&A
report/ – REPORT.md + REPORT.docx (generator: report/make_report.py)
ppt/ – SIH_Command_Center.pptx (generator: ppt/make_ppt.py)

## Team
See TEAM.md.
