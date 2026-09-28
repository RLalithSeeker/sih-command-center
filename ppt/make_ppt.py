# Part 1: setup, helpers, slides 1-2
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

prs = Presentation()
prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)

NAVY = RGBColor(15, 23, 42)
BLUE = RGBColor(37, 99, 235)
CYAN = RGBColor(14, 165, 233)
LIGHT = RGBColor(248, 250, 252)
MUTED = RGBColor(148, 163, 184)
WHITE = RGBColor(255, 255, 255)
BORDER = RGBColor(226, 232, 240)
BODY = RGBColor(51, 65, 85)
GREEN = RGBColor(22, 163, 74)
RED = RGBColor(220, 38, 38)

def hdr(slide, title):
    cat = slide.shapes.add_textbox(Inches(0.8), Inches(0.35), Inches(11.7), Inches(0.35))
    pc = cat.text_frame.paragraphs[0]
    pc.text = "SIH COMMAND CENTER | PBL 14"
    pc.font.size = Pt(10); pc.font.bold = True; pc.font.color.rgb = BLUE
    tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.68), Inches(11.7), Inches(0.7))
    pt = tb.text_frame.paragraphs[0]
    pt.text = title
    pt.font.size = Pt(22); pt.font.bold = True; pt.font.color.rgb = NAVY

def card(slide, left, top, width, height, title):
    c = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    c.fill.solid(); c.fill.fore_color.rgb = WHITE
    c.line.color.rgb = BORDER; c.line.width = Pt(1)
    tb = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.15), width - Inches(0.4), Inches(0.45))
    p = tb.text_frame.paragraphs[0]
    p.text = title
    p.font.size = Pt(13); p.font.bold = True; p.font.color.rgb = NAVY

def bullets(slide, left, top, width, height, items):
    """items: list of (marker, head, tail, head_color)"""
    tb = slide.shapes.add_textbox(left, top, width, height)
    tf = tb.text_frame; tf.word_wrap = True
    first = True
    for marker, head, tail, hc in items:
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        p.text = marker + head
        p.font.bold = True; p.font.size = Pt(11); p.font.color.rgb = hc
        r = p.add_run(); r.text = tail; r.font.bold = False; r.font.color.rgb = BODY
        p.space_after = Pt(8)

# --- SLIDE 1: title ---
s1 = prs.slides.add_slide(prs.slide_layouts[6])
bg = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
bg.fill.solid(); bg.fill.fore_color.rgb = NAVY; bg.line.fill.background()
tb = s1.shapes.add_textbox(Inches(1.0), Inches(1.4), Inches(11.3), Inches(4.8))
tf = tb.text_frame; tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "SMART INDIA HACKATHON 2026 | COMMAND CENTER"
p.font.size = Pt(14); p.font.bold = True; p.font.color.rgb = CYAN
p2 = tf.add_paragraph()
p2.text = "Centralised SPOC Operations & Deliverable Engine"
p2.font.size = Pt(36); p2.font.bold = True; p2.font.color.rgb = LIGHT; p2.space_before = Pt(8)
p3 = tf.add_paragraph()
p3.text = "Production-grade MERN architecture - Hardened validation - Stress-tested concurrency - Zero-loss demo mode"
p3.font.size = Pt(14); p3.font.color.rgb = MUTED; p3.space_before = Pt(12)
p4 = tf.add_paragraph()
p4.text = "Woxsen University | B.Tech CSE SEM 5 | Full Stack Development (24TU05MJC1)"
p4.font.size = Pt(13); p4.font.bold = True; p4.font.color.rgb = BLUE; p4.space_before = Pt(28)
p5 = tf.add_paragraph()
p5.text = "Team of 4: Lead Integrator - Frontend Engineer - Backend Engineer - QA & Reliability Lead"
p5.font.size = Pt(12); p5.font.color.rgb = LIGHT; p5.space_before = Pt(6)

# --- SLIDE 2: problem + objectives ---
s2 = prs.slides.add_slide(prs.slide_layouts[6])
hdr(s2, "The SPOC Operational Bottleneck & Technical Objectives")
card(s2, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.4), "Current Failure Modes (Spreadsheet Hell)")
bullets(s2, Inches(1.0), Inches(2.15), Inches(5.2), Inches(4.6), [
    ("- ", "Silent Composition Violations: ", "SIH needs 6 members with 1+ female. Excel cannot enforce atomic pre-commit validation.", RED),
    ("- ", "Problem Statement Clashing: ", "Duplicates allocated across silos with no shared real-time uniqueness constraint.", RED),
    ("- ", "Unbalanced Mentor Saturation: ", "Mentors exceed bandwidth while others idle; load tracking is fully manual.", RED),
    ("- ", "Unquantified Readiness: ", "No continuous score (GitHub, PPT, video, report); SPOC inspects each Drive manually.", RED),
])
card(s2, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.4), "System Requirements & Design Guarantees")
bullets(s2, Inches(7.0), Inches(2.15), Inches(5.3), Inches(4.6), [
    ("+ ", "Atomic Hard-Blocking Validation: ", "HTTP 400 rejection of bad rosters before persistence.", GREEN),
    ("+ ", "Real-time Duplicate Prevention: ", "Unique lock per PS id with explicit SPOC override flag.", GREEN),
    ("+ ", "Heuristic Auto-Allocation Engine: ", "Least-loaded mentor assignment under max-capacity limits.", GREEN),
    ("+ ", "Multi-factor Readiness Matrix: ", "25% per approved artifact, minus 25% penalties for missing mentor or bad team.", GREEN),
    ("+ ", "Resilient Fallback Mode: ", "Zero-config in-memory demo with hot-switch MongoDB persistence.", GREEN),
])

# Part 2: slides 3-4 (imported after part1)
# --- SLIDE 3: architecture ---
s3 = prs.slides.add_slide(prs.slide_layouts[6])
hdr(s3, "High-Level Architecture & Persistence Strategy")
card(s3, Inches(0.8), Inches(1.5), Inches(3.7), Inches(3.7), "1. Client Tier (Zero-Build)")
bullets(s3, Inches(0.95), Inches(2.15), Inches(3.4), Inches(2.9), [
    ("- ", "Guided flow: ", "5 responsive HTML views, no build step.", NAVY),
    ("- ", "Fetch bridge: ", "unified async client in app.js.", NAVY),
    ("- ", "Sanitized output: ", "esc() filter on every render.", NAVY),
    ("- ", "Mobile adaptive: ", "media queries for 390-640px.", NAVY),
])
card(s3, Inches(4.8), Inches(1.5), Inches(3.7), Inches(3.7), "2. API Engine (Express)")
bullets(s3, Inches(4.95), Inches(2.15), Inches(3.4), Inches(2.9), [
    ("- ", "15 REST routes: ", "teams, PS, mentors, deliverables.", NAVY),
    ("- ", "Hardened parsing: ", "JSON shape + size enforcement.", NAVY),
    ("- ", "SIH scraper: ", "live ingest from sih.gov.in.", NAVY),
    ("- ", "Exports: ", "RFC 4180 CSV + printable report.", NAVY),
])
card(s3, Inches(8.8), Inches(1.5), Inches(3.7), Inches(3.7), "3. Dual-Tier Persistence")
bullets(s3, Inches(8.95), Inches(2.15), Inches(3.4), Inches(2.9), [
    ("- ", "In-memory default: ", "instant demo, no Mongo needed.", NAVY),
    ("- ", "Mongo via Mongoose: ", "activates on MONGO_URI.", NAVY),
    ("- ", "Graceful fallback: ", "DB failure drops to memory.", NAVY),
    ("- ", "Crash-resistant: ", "bad payloads return 400/500.", NAVY),
])
card(s3, Inches(0.8), Inches(5.35), Inches(11.7), Inches(1.6), "Data Model & Entity Relationships")
bullets(s3, Inches(1.0), Inches(5.9), Inches(11.3), Inches(1.0), [
    ("", "", "Teams {id, name, leadEmail, members[6], psId, mentorId} | PS {id, code, sihId, title, category, org, takenBy}", NAVY),
    ("", "", "Mentors {id, name, dept, maxTeams, load} | Deliverables {teamId, type, link, status} 1:4 | Milestones {id, name, date, daysLeft}", NAVY),
])

# --- SLIDE 4: what we built ---
s4 = prs.slides.add_slide(prs.slide_layouts[6])
hdr(s4, "Engineering Deliverables: What Has Been Built")
WB, HB = Inches(5.6), Inches(2.6)
card(s4, Inches(0.8), Inches(1.5), WB, HB, "1. Team Roster Enforcement")
bullets(s4, Inches(1.0), Inches(2.05), WB - Inches(0.4), HB - Inches(0.6), [
    ("- ", "", "Guided 3-step wizard with prefilled lead details.", NAVY),
    ("- ", "", "Server validation: exactly 6, min 1 female.", NAVY),
    ("- ", "", "Auto-provisions 4 deliverable slots per team.", NAVY),
])
card(s4, Inches(6.9), Inches(1.5), WB, HB, "2. PS Catalog & Live Ingestion")
bullets(s4, Inches(7.1), Inches(2.05), WB - Inches(0.4), HB - Inches(0.6), [
    ("- ", "", "One-click scraper of official sih.gov.in table.", NAVY),
    ("- ", "", "Search by SIH number (e.g. SIH25001).", NAVY),
    ("- ", "", "Duplicate detection with allowDuplicate override.", NAVY),
])
card(s4, Inches(0.8), Inches(4.3), WB, HB, "3. Mentor Assignment Engine")
bullets(s4, Inches(1.0), Inches(4.85), WB - Inches(0.4), HB - Inches(0.6), [
    ("- ", "", "Live load view: current teams vs maxTeams.", NAVY),
    ("- ", "", "One-click auto-assign to least-loaded mentor.", NAVY),
    ("- ", "", "Full mentors blocked automatically (400).", NAVY),
])
card(s4, Inches(6.9), Inches(4.3), WB, HB, "4. Readiness Dashboard")
bullets(s4, Inches(7.1), Inches(4.85), WB - Inches(0.4), HB - Inches(0.6), [
    ("- ", "", "4 items: GitHub, PPT, video, report.", NAVY),
    ("- ", "", "Readiness = approved/4 minus 25% penalties.", NAVY),
    ("- ", "", "CSV export + printable PDF-ready report.", NAVY),
])

# Part 3: slides 5-6 (imported after part2)
# --- SLIDE 5: hardening + testing ---
s5 = prs.slides.add_slide(prs.slide_layouts[6])
hdr(s5, "Security Hardening, Error Handling & Concurrency Testing")
card(s5, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.4), "Vulnerabilities Found & Fixed")
bullets(s5, Inches(1.0), Inches(2.15), Inches(5.2), Inches(4.6), [
    ("- ", "DoS crash: ", "non-array members killed Node. Fixed with type guard + global error handler.", NAVY),
    ("- ", "Stored XSS: ", "team names ran in innerHTML. Fixed with esc() on backend report + all pages.", NAVY),
    ("- ", "Link injection: ", "javascript: URLs in deliverables. Fixed: only http(s) become links.", NAVY),
    ("- ", "Silent failures: ", "blank pages on network loss. Fixed: loadFailed() banners everywhere.", NAVY),
])
card(s5, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.4), "Empirical Verification")
bullets(s5, Inches(7.0), Inches(2.15), Inches(5.3), Inches(4.6), [
    ("+ ", "40/40 functional: ", "composition, duplicates, countdowns, exports all pass.", GREEN),
    ("+ ", "27/27 stress: ", "200 GETs in 447ms (~450/s); 50 concurrent in 77ms, zero failures.", GREEN),
    ("+ ", "Parallel writes: ", "10 simultaneous team creates, no races or id collisions.", GREEN),
    ("+ ", "38/38 browser: ", "headless Chrome at 390px + 1280px, no errors, no overflow.", GREEN),
])

# --- SLIDE 6: roadmap ---
s6 = prs.slides.add_slide(prs.slide_layouts[6])
hdr(s6, "Future Roadmap: Production Scaling & Advanced Capabilities")
RW, RH = Inches(3.7), Inches(5.4)
card(s6, Inches(0.8), Inches(1.5), RW, RH, "Phase 1: Security & Identity")
bullets(s6, Inches(1.0), Inches(2.15), RW - Inches(0.4), RH - Inches(0.8), [
    ("- ", "RBAC: ", "SPOC admin, mentors, team leads with JWT sessions.", NAVY),
    ("- ", "SSO: ", "OAuth bridge with campus Microsoft 365 directory.", NAVY),
    ("- ", "Audit trails: ", "immutable log of approvals and edits.", NAVY),
])
card(s6, Inches(4.8), Inches(1.5), RW, RH, "Phase 2: Communication")
bullets(s6, Inches(5.0), Inches(2.15), RW - Inches(0.4), RH - Inches(0.8), [
    ("- ", "Email alerts: ", "SMTP notices on revision flags.", NAVY),
    ("- ", "WhatsApp pushes: ", "deadline countdowns to team leads.", NAVY),
    ("- ", "Review portals: ", "one-click approve links in mentor mail.", NAVY),
])
card(s6, Inches(8.8), Inches(1.5), RW, RH, "Phase 3: Data & Cloud")
bullets(s6, Inches(9.0), Inches(2.15), RW - Inches(0.4), RH - Inches(0.8), [
    ("- ", "Postgres: ", "relational schema via Prisma ORM.", NAVY),
    ("- ", "Artifact storage: ", "S3/R2 buckets + GitHub verification.", NAVY),
    ("- ", "Coolify deploy: ", "Docker + health checks + snapshots.", NAVY),
])

# Part 4: slides 7-8 + save (imported after part3)
# --- SLIDE 7: demo runbook + viva ---
s7 = prs.slides.add_slide(prs.slide_layouts[6])
hdr(s7, "Viva Defense & Live Demonstration Runbook")
card(s7, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.4), "Live 3-Minute Demo Sequence")
bullets(s7, Inches(1.0), Inches(2.15), Inches(5.2), Inches(4.6), [
    ("- ", "1. Rejection: ", "submit 5-member team, show HTTP 400 block.", NAVY),
    ("- ", "2. Happy path: ", "register valid team, wizard reaches Done.", NAVY),
    ("- ", "3. Duplicate guard: ", "claim taken PS, then allowDuplicate override.", NAVY),
    ("- ", "4. Auto-mentor: ", "least-loaded assignment on mentors page.", NAVY),
    ("- ", "5. Readiness climb: ", "approve 2 items, watch score rise.", NAVY),
    ("- ", "6. Export: ", "open CSV in Excel + printable report.", NAVY),
])
card(s7, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.4), "Anticipated Viva Q&A")
bullets(s7, Inches(7.0), Inches(2.15), Inches(5.3), Inches(4.6), [
    ("Q: ", "Single-file server? ", "Easy viva inspection of full lifecycle.", BLUE),
    ("Q: ", "Memory-first DB? ", "Demo-safe on any PC; Mongo via one env var.", BLUE),
    ("Q: ", "No Tailwind? ", "Zero-build; runs straight from disk.", BLUE),
    ("Q: ", "Duplicate race? ", "Atomic PS check before commit; 400 on clash.", BLUE),
])

# --- SLIDE 8: team ---
s8 = prs.slides.add_slide(prs.slide_layouts[6])
hdr(s8, "Project Summary & Engineering Contributions")
ROLES = [
    ("Full-Stack / Integrator", "You", ["Core architecture & integration", "Dashboard & readiness logic", "API wiring & hardening", "Deployment + live demo"]),
    ("Frontend Developer", "Member 2", ["5 responsive pages", "3-step team wizard", "Mobile @390px CSS", "Validation + esc() UI"]),
    ("Backend Engineer", "Member 3", ["15 REST endpoints", "Mongoose dual-tier store", "SIH portal scraper", "CSV + report exports"]),
    ("QA & Reliability Lead", "Member 4", ["105 automated cases", "Stress + browser suites", "DoS + XSS audit", "PPT + viva kit"]),
]
CW = Inches(2.7)
for i, (role, person, items) in enumerate(ROLES):
    left = Inches(0.8) + i * Inches(2.95)
    card(s8, left, Inches(1.5), CW, Inches(5.4), role)
    tb = s8.shapes.add_textbox(left + Inches(0.15), Inches(2.15), CW - Inches(0.3), Inches(4.6))
    tf = tb.text_frame; tf.word_wrap = True
    pn = tf.paragraphs[0]
    pn.text = person
    pn.font.size = Pt(13); pn.font.bold = True; pn.font.color.rgb = BLUE; pn.space_after = Pt(8)
    for it in items:
        p = tf.add_paragraph()
        p.text = "- " + it
        p.font.size = Pt(10); p.font.color.rgb = BODY; p.space_after = Pt(4)

prs.save(os.path.join(os.path.dirname(os.path.abspath(__file__)), "SIH_Command_Center.pptx"))
print("saved: SIH_Command_Center.pptx")

