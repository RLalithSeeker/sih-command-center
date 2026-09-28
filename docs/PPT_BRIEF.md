# PPT BRIEF — SIH Command Center (general audience version)

Source of truth for generating the presentation deck. Audience: faculty examiners
and SPOC stakeholders — explain WHAT and WHY in plain language, not implementation
detail. Output: 8 slides, 16:9.

## 1. Writing rules (the part that matters most)

- Write for a smart non-programmer. If a term needs a CS degree, say it in plain words.
- Good: "The app rejects a team of 5 — the rule is enforced before anything is saved."
- Bad: "Array.isArray guard + global Express error interceptor."
- One idea per bullet, max 14 words, sentence case, start the bullet with "- ".
- Bullets state outcomes, never mechanisms: "one click assigns the freest mentor", not "least-loaded heuristic".
- Numbers stay, because they are the evidence: 105 checks · 242 statements · 450 req/sec · 25% per deliverable.
- Ban on slides: code, file names, framework names, database names, Git history, acronyms without a plain gloss.
- Read every bullet aloud once. If you stumble, cut it.
- Each slide must survive being read from the back of the room: 5 bullets max, 6 on the overview slide only.

## 2. Design system (exact values — copy these)

Slide size 13.333 × 7.5 in (16:9).

| Token | Value |
|---|---|
| Slide paper | `#F6F1E7` |
| Card fill / border | `#FFFDF8` / `#E3DCCB` |
| Heading navy | `#1E2A4A` |
| Brass accent | `#A96B1B` |
| Body text | `#334155` |
| Muted text | `#78808F` |
| Title-slide background | `#0F172A`; title `#FFFFFF`; subtitle `#C8D2E6`; meta lines `#96A5C3` |
| Metric strip | `#1E2A4A` fill, white mono text |
| Green / red | `#2F7D4F` / `#B3352B` (results and warnings only) |

Type (fonts must exist on any Windows PC — no web fonts to install):
- Slide title: Georgia bold, 25pt, navy
- Eyebrow above title: Consolas, 10.5pt, UPPERCASE, brass
- Bullets: Arial 14pt (13pt in side-by-side cards), line spacing 1.15, 9pt after each bullet
- Emphasis / body in cards: Arial 12–13pt
- Numbers, IDs, metrics: Consolas bold (13.5–15pt)
- Title slide: eyebrow 13pt brass · title 46pt Georgia bold white · subtitle 18pt · meta 13pt
- Closing line: Georgia bold 15pt brass
- Smallest size allowed anywhere: 12pt

Geometry grid (inches from the top-left):
- Side margins 0.75; content width 11.85; vertical safe band 0.35 → 7.20
- Eyebrow at y=0.35, title at y=0.68, brass rule at y=1.42 (11.85 wide, 2.5pt thick)
- Content slides: bullets column starts x=0.75, y=1.75, width = 12.0 − image width − 0.4
- Images: right-aligned at x = 12.6 − image width, starting y=1.75, with a 1pt `#E3DCCB` border
- Standard image width 5.65 (a 4:3 screenshot becomes 3.97 tall)
- Two stacked images: crop each to ≈66% height, keep a 0.12 gap, verify y_end = y + width × aspect before saving
- Phone screenshot: width 1.95, portrait, no crop
- Metric strip: rounded rectangle 4.4 × 0.95 at (8.15, 6.20)
- Closing line: x=0.75, y=6.45
- Slide 8: two equal cards 5.9 and 5.75 wide × 4.5 tall at y=1.75

Image treatment rules:
- Never stretch an image — set width only, let height follow the aspect ratio, then check the bottom edge fits the safe band.
- Never let an image end mid-element: pick the crop height, then snap the cut to the flattest (blank) row within ±18% of it.
- Max 2 images per slide; they must never overlap each other or the bullets.
- Only real screenshots from `report/shots/` — no mockups, clip-art, stock photos, icons or emoji.


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

### Slide 2 — What we built (overview)
- One web app for the SPOC: five screens, no installation, works offline
- Register a team → the rules check themselves, instantly
- Pick a problem statement from the official list, held by one team only
- See every mentor's load and assign in one click
- Track 4 deliverables per team and get a live readiness score (0–100)
- Export the whole register as Excel or a printable report in one click

Embed: `phase1-dashboard.png`
(If space allows, small second image: `phase2-dashboard-filtered.png`)

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
2. Walk the overview top-to-bottom — this is the map of the four deep-dive slides that follow.
3. Demo hook: "watch me try to break it" — the two rejections land here.
4. Emphasise no manual typing: the official list arrives in one click.
5. Point at the load numbers: fairness for mentors, visible in one glance.
6. The readiness score is the headline feature — SPOC never opens Drive again.
7. Lead with 105 — testing is the credibility slide.
8. Invite the live demo now; keep the backend visible on screen.

## 6. Build constraints

- Reference implementation: `ppt/make_ppt.py` builds this exact deck — read it before generating anything; match it rather than inventing a new look.
- Colour, size and coordinate values in section 2 are not suggestions. Copy them.
- Verify before finishing: render the slides and look at them (PowerPoint can export slides to images). Fix overlaps, mid-element crops and text that runs off a card before claiming done.
- Trim bullets rather than shrink text below 12pt; never let text leave its card.
- Do not invent features, names, metrics or dates that are not listed in this brief.
- Embed only screenshots from `report/shots/`, and keep the numbers exact: 105 checks · 242 statements · 450 req/sec · 25% per deliverable.
- No clip-art, emoji, stock imagery, gradients, drop shadows or decorative icon rows.
- Keep slide count at 8 with the section 4 running order.

## 7. Regenerate the deck

```
python ppt/make_ppt.py        # rebuilds ppt/SIH_Command_Center.pptx from report/shots/
```
The script crops tall screenshots automatically (snapping cuts to blank rows) and
writes 8 slides. Requires Pillow. To refresh the screenshots themselves first:
`node backend/shots.js` (needs the backend on port 5000 and the frontend on port 8080).


