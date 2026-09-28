# PPT BRIEF — SIH Command Center (general audience version)

Source of truth for generating the presentation deck. Audience: faculty examiners
and SPOC stakeholders — explain WHAT and WHY in plain language, not implementation
detail. Output: 8 slides, 16:9.

## 1. Tone rules (most important)

- Write for a smart non-programmer. If a term needs a CS degree, replace it with plain words.
- Good: "The app rejects a team of 5 — the rule is enforced before anything is saved."
- Bad: "Array.isArray guard + global Express error interceptor."
- One idea per bullet, max 14 words. No acronyms without a one-word gloss.
- Numbers are fine and impressive: 242 statements, 105 tests, 450 requests/sec.
- Never show code, file names, framework internals, or Git history.

## 2. Design system

| Token | Value |
|---|---|
| Paper / card background | `#F6F1E7` paper, `#FFFDF8` cards |
| Headings | deep navy `#1E2A4A`, Georgia serif |
| Accent | brass `#A96B1B` (eyebrow labels, thin rules) |
| Body text | `#334155`, system sans, sentence case |
| Green `#2F7D4F` | guarantees, passing results |
| Red `#B3352B` | problems, blocked actions |
| Data (numbers, IDs) | monospace |
| Title slide | navy `#0F172A` full-bleed, white text |
| Layout | max 4 cards per slide, max 5 short bullets per card, 10pt floor |
| Imagery | only the app screenshots listed below — no clip-art, no stock photos, no emoji |

## 3. Screenshots to embed (ready in `report/shots/`)

| # | File | Shows |
|---|---|---|
| 1 | `phase1-dashboard.png` | Dashboard: deadlines with countdowns + team readiness dials |
| 2 | `phase2-dashboard-filtered.png` | Dashboard filtered to "Ready" teams |
| 3 | `phase3-team-step1.png` | Team registration, step 1 |
| 4 | `phase4-team-step2.png` | Member entry form (6 members, gender dropdowns) |
| 5 | `phase5-ps-search.png` | Problem-statement search with results for one SIH number |
| 6 | `phase6-mentors.png` | Mentor load table + assign / auto-assign |
| 7 | `phase7-deliverables.png` | Four deliverables with link + status chips |
| 8 | `phase8-printable-report.png` | Printable status report (for institute records) |
| 9 | `phase9-mobile-dashboard.png` | Dashboard on a phone screen |


## 4. The 8 slides

### Slide 1 — Title
- Eyebrow: `WOXSEN · SMART INDIA HACKATHON 2026`
- Title: **SIH Command Center** — one place to track every hackathon team
- Sub: Team register · Problem statements · Mentors · Deliverable deadlines
- Footer: Woxsen University | B.Tech CSE SEM 5 | Full Stack Development | Team of 4

### Slide 2 — Why this was needed
Left card — **Today's mess** (red bullets):
- Teams tracked in spreadsheets + WhatsApp — errors found too late
- Two teams can pick the same problem statement
- No clear view of which mentor is overloaded
- Nobody knows a team's real progress until it's too late

Right card — **What we built** (green bullets):
- The app checks every team rule the moment it's entered
- A problem statement can be held by only one team at a time
- Each mentor's workload is visible, with a one-click auto-assign
- Every team gets a live "readiness score" out of 100

Embed: `phase1-dashboard.png`

### Slide 3 — How it helps (the rules)
- Exactly 6 members — a team of 5 is rejected instantly
- At least 1 female member — mandatory SIH rule, also rejected if missing
- A valid team is saved in one go and automatically gets its 4 deliverable slots
- Screenshots show the actual error messages an SPOC would see

Embed: `phase3-team-step1.png` + `phase4-team-step2.png`
Caption: "The rule is checked before anything is saved — nothing invalid can slip through."

### Slide 4 — Finding the right problem statement
- One click pulls the official list from sih.gov.in — 242 statements, no manual typing
- Search by the SIH number or a keyword — results show in seconds
- Claim a statement; if it's already taken, the app says who holds it
- The SPOC can deliberately allow a shared statement if needed

Embed: `phase5-ps-search.png`

### Slide 5 — Mentors without the guesswork
- Load table shows each mentor's current teams vs. their limit
- A full mentor is marked — the app refuses to overload them
- One click assigns a team to whoever is currently freest
- Changes appear immediately in the dashboard

Embed: `phase6-mentors.png`

### Slide 6 — Progress you can actually see
- Four deliverables per team: GitHub repo, presentation, demo video, report
- Each has a link + status: submitted, needs revision, approved
- Every approval adds 25% to the team's readiness score
- One click exports everything as an Excel file or a printable report

Embed: `phase7-deliverables.png` (+ small `phase8-printable-report.png`)

### Slide 7 — How we proved it works
- 105 automated checks — every rule, screen and export tested
- Fast and stable: about 450 requests handled per second
- Tested on phone and desktop screens — no layout breaks
- Security checked and hardened — fake data can't harm the app
- Works offline on any college PC — no database needed for a demo

Embed: `phase9-mobile-dashboard.png`
Metric strip (mono font): `105 tests` · `450 req/s` · `390px → desktop` · `242 statements`

### Slide 8 — What's next + who did what
Left — **Next steps**:
- Sign-in for SPOC / mentors / students (everyone sees only their own)
- Automatic email + WhatsApp deadline reminders
- Long-term: real database and online hosting for the whole campus

Right — **Team of 4**:
- Lead / Integration — architecture, wiring, demo
- Frontend — the 5 screens and forms
- Backend — the rules, list import, exports
- QA — 105 tests, security checks, this presentation

Close line: **"SIH Command Center — register it right, track it till the finale."**

---

## 5. Speaker notes (one line each)
1. One sentence: what the app is and who it's for.
2. Name the 4 everyday pains — examiners recognise them instantly.
3. Demo hook: "watch me try to break it" — the two rejections land here.
4. Emphasise no manual typing: the official list arrives in one click.
5. Point at the load numbers: fairness for mentors, visible in one glance.
6. The readiness score is the headline feature — SPOC never opens Drive again.
7. Lead with 105 — testing is the credibility slide.
8. Invite the live demo now; keep the backend visible on screen.

## 6. Constraints for the generator
- Keep exact numbers: 105 tests · 242 statements · 450 req/s · 25% per deliverable.
- Plain language only — no code, no framework names, no file paths on slides.
- Embed only screenshots from `report/shots/` (list in section 3).
- Trim bullets rather than shrink text below 10pt; never overflow a card.
- Do not invent features, names, metrics, or dates not listed here.
- Navy / brass / cream palette only; no clip-art, emoji, or stock imagery.

