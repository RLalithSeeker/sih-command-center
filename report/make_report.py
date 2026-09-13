# QA member script: builds REPORT.docx from the markdown report
import os
from docx import Document
from docx.shared import Pt

here = os.path.dirname(__file__)
doc = Document()
style = doc.styles["Normal"]
style.font.name = "Calibri"
style.font.size = Pt(11)

doc.add_heading("SIH Command Center - Hackathon Team & Deliverable Tracking (PBL 14)", 0)
doc.add_paragraph("Full Stack Development (24TU05MJC1), Woxsen University. Team of 4: full-stack lead, frontend, backend, QA + docs. Stack: Express + MongoDB (optional) + plain HTML/CSS/JS, Node, Git.")

sections = [
    ("1. Problem + objectives", "SPOC tracked SIH teams in sheets and emails; invalid teams and pending deliverables surfaced too late. Objectives: (1) registration blocking non-6 / no-female teams, (2) official SIH-number search with duplicate check, (3) mentor assignment with load view + auto-assign, (4) deliverable tracker + readiness %, (5) deadline countdowns, (6) filterable dashboard + CSV/PDF export."),
    ("2. Design + methodology", "Express REST + Mongo-or-memory, 5 guided pages, one CSS file. Entities: Team, PS (sihId), Mentor, Deliverable, Milestone. Readiness = approved/4*100 minus penalties. Plan: W1 requirements + design, W2 backend, W3 frontend, W4 testing + report."),
    ("3. Implementation (phase-wise)", "Phase 1: scaffold + docs. Phase 2: server.js - routes, 6-member/1-female hard validation, readiness, seed, CSV export. Phase 3: 3-step team wizard, dropdowns (no id typing), teacher hints, dashboard filters. Phase 4: one-click official SIH scrape (239 statements), milestones, QA 17-case plan, this report, PPT."),
    ("4. Analysis / results", "Demo + registered teams verified: readiness rises with approvals, invalid teams blocked with clear messages, duplicate PS warned, mentor overload blocked, CSV opens in Excel, printable report saves as PDF. Limitation: no real email (reminder list shown), mentor view read-only, filters reset on reload."),
    ("5. Conclusion + future work", "All PBL features working. Next: real email, mentor login, auth. Each member demos own part (TEAM.md)."),
]
for title, body in sections:
    doc.add_heading(title, 1)
    doc.add_paragraph(body)

doc.add_heading("Test summary (full table in docs/04-test-plan.md)", 1)
rows = [("Valid team (6, 1 female)", "PASS"), ("5 members", "Blocked PASS"), ("6 males", "Blocked PASS"),
        ("Duplicate PS", "Blocked PASS"), ("Mentor overload", "Blocked PASS"), ("Bad status value", "Blocked PASS"),
        ("Readiness math", "PASS"), ("CSV export", "PASS"), ("Official scrape (239)", "PASS"),
        ("Milestone countdown", "PASS")]
table = doc.add_table(rows=1, cols=2)
table.style = "Light Grid Accent 1"
table.rows[0].cells[0].text, table.rows[0].cells[1].text = "Case", "Result"
for case, result in rows:
    cells = table.add_row().cells
    cells[0].text, cells[1].text = case, result

doc.add_heading("Screenshots", 1)
doc.add_paragraph("See report/SCREENSHOTS.md for the 5 captures (dashboard, wizard, duplicate warning, mentor load, PDF report). Paste them here before printing.")

doc.save(os.path.join(here, "REPORT.docx"))
print("saved REPORT.docx")
