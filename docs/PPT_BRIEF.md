# PPT BRIEF — SIH Command Center Technical Presentation

Use this file as the single source of truth for generating the slide deck
(viva / submission). Everything an AI slide generator needs is here.
Output: 8 slides, 16:9 (13.333 × 7.5 in / 1920×1080).

---

## 1. Design system (apply to every slide)

| Token | Value | Use |
|---|---|---|
| Background | `#FFFDF8` (white cards) on `#F6F1E7` paper | slide base |
| Primary | `#1E2A4A` (deep navy) | headings, card titles |
| Accent | `#A96B1B` (brass) | eyebrow labels, rules, highlights |
| Body text | `#334155` | bullets |
| Success | `#2F7D4F` | verified/guarantee items |
| Danger | `#B3352B` | problem/risk items |
| Display font | Georgia (serif) | slide titles + card titles |
| Body font | system sans (Segoe UI / Arial) | bullets |
| Data font | monospace (Consolas) | metrics, schema, code |
| Title slide only | navy `#0F172A` full-bleed background, white text | slide 1 |
| Eyebrow | 10pt mono uppercase, brass, above title | every content slide |
| Card style | rounded rect, 1px `#E3DCCB` border, white fill | content blocks |

Rules: max 2 columns × 2 rows of cards per slide; max 5 bullets per card;
sentence case bullets; numbers in monospace; no clip-art, no stock photos.

---

## 2. Slide-by-slide content

### Slide 1 — Title
- Eyebrow: `SMART INDIA HACKATHON 2026 | COMMAND CENTER`
- Title (36pt, white, Georgia): **Centralised SPOC Operations & Deliverable Engine**
- Sub: Production-grade MERN architecture · Hardened validation · Stress-tested concurrency · Zero-loss demo mode
- Org: Woxsen University | B.Tech CSE SEM 5 | Full Stack Development (24TU05MJC1)
- Team line: Team of 4 — Lead Integrator · Frontend Engineer · Backend Engineer · QA & Reliability Lead

### Slide 2 — The SPOC Operational Bottleneck & Technical Objectives
Left card — **Current Failure Modes (Spreadsheet Hell)** (red markers):
- Silent Composition Violations — Excel cannot enforce atomic pre-commit validation of the 6-member / 1-female SIH rule.
- Problem Statement Clashing — duplicate allocations across silos with no shared uniqueness constraint.
- Unbalanced Mentor Saturation — mentor-to-team load is tracked manually, if at all.
- Unquantified Readiness — no continuous score for GitHub / PPT / video / report; SPOC opens every Drive by hand.

Right card — **System Requirements & Design Guarantees** (green checkmarks):
- Atomic Hard-Blocking Validation — HTTP 400 rejection of bad rosters before persistence.
- Real-time Duplicate Prevention — unique lock per PS id with explicit SPOC override flag.
- Heuristic Auto-Allocation — least-loaded mentor assignment under max-capacity limits.
- Multi-factor Readiness Matrix — 25% per approved artifact, −25% penalty for missing mentor or invalid team.
- Resilient Fallback Mode — zero-config in-memory demo with hot-switch MongoDB persistence.

### Slide 3 — High-Level Architecture & Persistence Strategy
Three columns:
1. **Client Tier (Zero-Build)** — 5 responsive HTML views; unified async fetch bridge; `esc()` sanitization on every render; media queries at 390–640px.
2. **API Engine (Express)** — 15 REST routes; JSON shape/size enforcement; live scraper of sih.gov.in; RFC 4180 CSV + printable HTML report exports.
3. **Dual-Tier Persistence** — in-memory store by default (demo-safe); MongoDB via Mongoose when `MONGO_URI` set; graceful DB-failure fallback; bad payloads return 400/500, never crash.

Bottom strip — **Data Model**: `Teams {id, name, leadEmail, members[6], psId, mentorId}` · `PS {id, code, sihId, title, category, org, takenBy}` · `Mentors {id, name, dept, maxTeams, load}` · `Deliverables {teamId, type, link, status}` (1:4) · `Milestones {id, name, date, daysLeft}`

### Slide 4 — Engineering Deliverables: What Has Been Built
Four quadrants:
1. **Team Roster Enforcement** — guided 3-step wizard; server validation exactly 6 + min 1 female; auto-provisions 4 deliverable slots.
2. **PS Catalog & Live Ingestion** — one-click scraper of official sih.gov.in (242 statements); search by SIH number; duplicate detection with allowDuplicate override; offline pipe-separated bulk import.
3. **Mentor Assignment Engine** — live load view (current vs maxTeams); one-click auto-assign to least-loaded mentor; full mentors blocked with 400.
4. **Readiness Dashboard** — 4 items tracked (GitHub, PPT, video, report); readiness = approved/4 − penalties; CSV export + printable PDF-ready report.

### Slide 5 — Security Hardening, Error Handling & Concurrency Testing
Left card — **Vulnerabilities Found & Fixed**:
- DoS crash — non-array `members` killed the async Node runtime; fixed with type guard + global error handler.
- Stored XSS — team names executed in `innerHTML`; fixed with `esc()` on backend report + all 5 pages.
- Link injection — `javascript:` URLs in deliverable links; fixed: only `http(s)` becomes a link.
- Silent failures — blank pages on network loss; fixed: unified `loadFailed()` banners on every fetch.

Right card — **Empirical Verification** (monospace metrics):
- `40/40` functional tests — composition, duplicates, countdowns, exports.
- `27/27` stress tests — 200 GETs in 447 ms (~450 req/s); 50 concurrent in 77 ms, zero drops.
- Parallel writes — 10 simultaneous team creates, no races or id collisions.
- `38/38` headless Chrome — 390px + 1280px viewports, zero console errors, zero overflow.

### Slide 6 — Future Roadmap: Production Scaling & Advanced Capabilities
Three phases:
- **Phase 1 · Security & Identity** — RBAC (SPOC / mentor / team lead, JWT sessions); OAuth SSO with campus Microsoft 365; immutable audit trails.
- **Phase 2 · Communication** — SMTP email alerts on revision flags; WhatsApp deadline countdowns; one-click approve links in mentor mail.
- **Phase 3 · Data & Cloud** — PostgreSQL via Prisma ORM; S3/R2 artifact storage + GitHub verification; Dockerized Coolify deploy with health checks + snapshots.

### Slide 7 — Viva Defense & Live Demonstration Runbook
Left card — **Live 3-Minute Demo Sequence**:
1. Rejection — submit 5-member team, show HTTP 400 block.
2. Happy path — register valid team, wizard reaches Done.
3. Duplicate guard — claim taken PS, then allowDuplicate override.
4. Auto-mentor — least-loaded assignment on mentors page.
5. Readiness climb — approve 2 items, watch score rise.
6. Export — open CSV in Excel + printable report.

Right card — **Anticipated Viva Q&A**:
- Q: Single-file server? A: Intentional — examiners can read the full request lifecycle in one file.
- Q: Memory-first DB? A: Demo-safe on any college PC; MongoDB activates via one env var (`MONGO_URI`).
- Q: No Tailwind? A: Zero-build; pages run straight from disk with no toolchain.
- Q: Duplicate race? A: Atomic PS uniqueness check before commit; loser gets 400.

### Slide 8 — Project Summary & Engineering Contributions
Four columns (role / contribution):
- **Full-Stack / Integrator** — core architecture; dashboard & readiness logic; API wiring & hardening; deployment + live demo.
- **Frontend Developer** — 5 responsive pages; 3-step team wizard; mobile @390px; validation + `esc()` UI.
- **Backend Engineer** — 15 REST endpoints; dual-tier Mongoose store; SIH portal scraper; CSV + report exports.
- **QA & Reliability Lead** — 105 automated cases; stress + browser suites; DoS + XSS audit; PPT + viva kit.

---

## 3. Speaker notes (one line per slide)

1. Hook: one sentence — "Every SIH team, statement, mentor and deliverable in one scored register."
2. Name the 4 pain points; promise they're each answered later in the deck.
3. Point at the persistence box: "memory by default, Mongo by one env var — demo can't fail."
4. This is the feature checklist — map each quadrant to a PBL requirement.
5. Lead with the DoS fix: "our own stress test found a crasher; we fixed it before the demo."
6. Roadmap is sequenced — security first because it gates everything else.
7. Offer the live demo immediately after this slide; keep the backend terminal visible.
8. Close with the test total — 105 — then the team split.

## 4. Constraints for the generator

- 16:9; never overflow text off a card — trim bullets rather than shrink below 10pt.
- Keep exact metric wording (`40/40`, `27/27`, `38/38`, `105`) — numbers are the evidence.
- Do not invent features, names, or metrics not listed here.
- Do not show test-junk data (`<img src=x…>`, `bold-name`) in any screenshot or example.
- No stock photos, no emoji, no clip-art; navy/brass/cream palette only.

