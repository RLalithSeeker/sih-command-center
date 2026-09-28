# VIDEO BRIEF — SIH Command Center Demo Video

Use this file as the single source of truth for generating a project demo video
(presentation / submission). Everything an AI video generator or editor needs is here.

---

## 1. Project metadata

| Field | Value |
|---|---|
| Title | SIH Command Center — Hackathon Team & Deliverable Tracking |
| Subtitle | Centralised SPOC Operations & Deliverable Engine |
| Institution | Woxsen University, B.Tech CSE SEM 5 |
| Course | Full Stack Development (24TU05MJC1), MERN |
| Problem code | PBL 14 |
| Team | 4 members: Full-Stack Lead, Frontend Dev, Backend Dev, QA + Docs |
| GitHub | https://github.com/RLalithSeeker/sih-command-center |
| Live app | http://localhost:8080/index.html (API: http://localhost:5000) |
| Total length | ~90 seconds (6 scenes) |
| Tone | Technical, confident, fast-paced. No fluff. |
| Aesthetic | Cream paper (#F6F1E7), deep navy (#1E2A4A), brass accent (#A96B1B), Georgia serif headings |

---

## 2. Visual assets (record or screenshot these)

| Asset | Path |
|---|---|
| Dashboard desktop | `report/shots/index-1280.png` |
| Teams page | `report/shots/teams-1280.png` |
| Problem statements | `report/shots/ps-1280.png` |
| Mentors page | `report/shots/mentors-1280.png` |

---

## 3. Scene-by-scene script

### Scene 1 — Title (0:00–0:08)
**Visual:** Cream background. Navy/brass rule animates in. Title fades up:
"SIH COMMAND CENTER" (Georgia serif, navy) with brass eyebrow
"WOXSEN · SIH 2026 · SPOC REGISTER".
**Voiceover:** "SIH Command Center — a single register for every SIH team,
problem statement, mentor and deliverable."
**SFX:** subtle paper-slide in.

### Scene 2 — The problem (0:08–0:20)
**Visual:** Split screen — messy spreadsheet/WhatsApp on the left, our clean dashboard on the right.
Caption bullets fly in one at a time: invalid teams found late / same problem statement picked twice /
uneven mentor load / deliverables chased manually.
**Voiceover:** "SPOCs track hackathon teams across spreadsheets and email.
Invalid teams surface too late, problem statements get claimed twice, mentor load
is invisible, and deliverables are chased over WhatsApp. We replace all of that
with one scored, validated register."

### Scene 3 — The rule engine, enforced live (0:20–0:42)
**Visual:** Screen recording of `teams.html`. Action sequence with on-screen cursor:
1. Type team name + lead email → click "Next: members".
2. Fill only 5 members → Submit → red toast + inline error "Team must have exactly 6 members".
3. Fill 6 but all male → Submit → "At least 1 female member is mandatory (SIH rule)".
4. Fix gender dropdown → Submit → green toast "registered", wizard reaches Step 3, readiness dial appears in "All teams".
**Voiceover:** "Validation is server-side, not cosmetic. Five members — rejected.
No female member — rejected, per official SIH rules. A valid six-member team is
accepted atomically and gets four deliverable slots auto-created."
**Caption:** `400 Bad Request before persistence · hard block, per PBL spec`

### Scene 4 — Problem statements + duplicate guard (0:42–1:02)
**Visual:** `ps.html`.
1. Click "Fetch from sih.gov.in" → spinner → toast "Catalog already up to date (242)" (or "N new statements fetched").
2. Type `25001` in search → result table appears (max 20 rows) → click "Use".
3. Try assigning an already-taken PS to a second team → red toast "Already taken by Demo Spartans".
4. Tick "allow same PS as another team" → succeeds with brass toast.
**Voiceover:** "The official SIH catalog is one click — 242 statements scraped live
from sih.gov.in. Search by SIH number, claim a statement — duplicates are blocked
with a hard error, and the SPOC can explicitly override."

### Scene 5 — Mentor load + readiness + export (1:02–1:22)
**Visual:** rapid montage:
1. `mentors.html` — load table (mentor with `full` badge), click "Auto-assign free-est" → toast.
2. `deliverables.html` — set github → approved, ppt → approved → status chips update (green/amber).
3. `index.html` — the readiness dial animates 25 → 50 → 75%, reminders list shrinks, filter by Status = Ready.
4. Click "Export Excel (CSV)" → CSV opens; then "Open printable report" → print-ready HTML table.
**Voiceover:** "Mentors auto-assign to the freest desk under capacity limits.
Every approved artifact moves the readiness score — twenty-five percent per item,
minus penalties for an invalid team or missing mentor. One click exports the
consolidated register as CSV or a printable report."

### Scene 6 — Quality + close (1:22–1:30)
**Visual:** metrics cards animate in over the mobile screenshot:
`40/40 functional` · `27/27 stress (450 req/s)` · `38/38 headless Chrome` ·
`XSS + DoS hardened`. End card: repo URL + team roles.
**Voiceover:** "One hundred and five automated tests passing — functional,
concurrency and browser suites — with XSS and crash hardening built in.
SIH Command Center: ready for the nodal centre."
**SFX:** soft click on end card.

---

## 4. Narration (full, continuous — if using one voiceover track)

> SIH Command Center — a single register for every SIH team, problem statement,
> mentor and deliverable. SPOCs currently track hackathon teams across spreadsheets
> and email: invalid teams surface too late, statements get claimed twice, mentor
> load is invisible, and deliverables are chased over WhatsApp. We replace all of
> that with one scored, validated register. Validation is server-side, not cosmetic:
> five members — rejected; no female member — rejected, per official SIH rules.
> A valid six-member team is accepted atomically and gets four deliverable slots
> auto-created. The official SIH catalog is one click — 242 statements scraped live
> from sih.gov.in — search by SIH number, claim a statement, and duplicates are
> blocked with a hard error the SPOC can explicitly override. Mentors auto-assign
> to the freest desk under capacity limits. Every approved artifact moves the
> readiness score — twenty-five percent per item, minus penalties for an invalid
> team or missing mentor — and one click exports the consolidated register as CSV
> or a printable report. Behind it: one hundred and five automated tests passing —
> functional, concurrency and browser suites — with XSS and crash hardening built
> in. SIH Command Center: ready for the nodal centre.

---

## 5. Generation constraints

- Aspect ratio 16:9 (1920×1080); keep UI text legible — record at 100% zoom, no less.
- No stock footage of people/offices — only product UI, this repo's screenshots, and motion-graphic captions.
- Never show the test-junk rows (`<img src=x…>`, `bold-name`) — demo data must be: Demo Spartans, 3 seed milestones, 242 statements.
- Fonts: Georgia (headings), system sans (UI), monospace (data/captions).
- Captions must quote errors verbatim — exact wording is part of the spec evidence.
- Do not narrate or show: Mongo vs Postgres debates, internal test file names, Git commit hashes.
- Mobile shot (390px) may appear only in Scene 6 as "responsive" proof.


| Deliverables page | `report/shots/deliverables-1280.png` |
| Dashboard mobile 390px | `report/shots/index-390.png` |
| Deck | `ppt/SIH_Command_Center.pptx` (8 slides) |
| Report | `report/REPORT.docx` |

To start everything for live recording: double-click `run.bat`, then open `frontend/index.html`
(or serve frontend on 8080). Backend health check: `http://localhost:5000/api/health`.
