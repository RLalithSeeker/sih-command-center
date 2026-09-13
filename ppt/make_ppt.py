# QA member script: builds SIH_Command_Center.pptx (8 slides, plain theme)
from pptx import Presentation
from pptx.util import Pt

prs = Presentation()
prs.slide_width, prs.slide_height = Pt(960), Pt(540)

slides = [
    ("SIH Command Center", "Hackathon Team & Deliverable Tracking (PBL 14)\nWoxsen University | Full Stack Development\nTeam: full-stack lead, frontend, backend, QA"),
    ("Problem", "SPOC tracks SIH teams in sheets + emails.\n- Invalid teams found too late\n- Same PS picked twice\n- Uneven mentor load\n- Deliverables chased on WhatsApp"),
    ("Objectives", "1. Block invalid teams (6 members, min 1 female)\n2. Official SIH number search + duplicate check\n3. Mentor load view + auto-assign\n4. Deliverable tracker + readiness %\n5. Dashboard + CSV/PDF export"),
    ("Design", "Browser -> Express REST (5000) -> Mongo or memory\nTables: Team, PS (sihId), Mentor, Deliverable\nReadiness = approved/4 - penalties\n5 pages, one CSS file"),
    ("Demo flow", "Live: register team (wizard) -> search SIH25001 -> auto-assign mentor -> approve deliverable -> readiness rises -> export report"),
    ("Key logic", "checkComposition(): exactly 6 + 1 female, 400 block\nreadiness(): approved/4*100 - 25 (bad team) - 25 (no mentor)\nQA found seed-id bug, fixed, 14/14 pass"),
    ("Testing", "17 manual cases, all pass.\n2 bugs fixed (CSV quotes, seed ids).\nKnown minor: dashboard filters reset on reload."),
    ("Conclusion", "All 8 PBL features working.\nRoles: lead integrated, frontend built UI, backend built APIs, QA tested + docs.\nNext: real email, mentor login, auth."),
]

for title, body in slides:
    s = prs.slides.add_slide(prs.slide_layouts[1])
    s.shapes.title.text = title
    s.placeholders[1].text = body

prs.save(__import__("os").path.join(__import__("os").path.dirname(__file__), "SIH_Command_Center.pptx"))
print("saved SIH_Command_Center.pptx")
