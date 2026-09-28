# SIH Command Center - presentation generator (8 slides, plain-language, screenshots embedded)
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

HERE = os.path.dirname(os.path.abspath(__file__))
SHOTS = os.path.join(HERE, "..", "report", "shots")
CROP = os.path.join(HERE, "_crop")
os.makedirs(CROP, exist_ok=True)

from PIL import Image


def crop_top(name, keep):
    """crop the top of a screenshot, snapping the cut to the nearest blank row
    so images never end mid-element"""
    im = Image.open(os.path.join(SHOTS, name)).convert("RGB")
    w, h = im.size
    target = int(h * keep)
    lo, hi = max(1, int(target * 0.82)), min(h - 1, int(target * 1.18))
    best, best_std = target, None
    step = max(1, w // 160)
    px = im.load()
    for y in range(lo, hi):
        vals = [sum(px[x, y]) for x in range(0, w, step)]
        mean = sum(vals) / len(vals)
        std = (sum((v - mean) ** 2 for v in vals) / len(vals)) ** 0.5
        if best_std is None or std < best_std:
            best, best_std = y, std
    out = os.path.join(CROP, "crop_%d_%s" % (int(keep * 100), name))
    im.crop((0, 0, w, best)).save(out)
    return out

NAVY = RGBColor(15, 23, 42)
NAVY2 = RGBColor(30, 42, 74)
BRASS = RGBColor(169, 107, 27)
PAPER = RGBColor(246, 241, 231)
CARD = RGBColor(255, 253, 248)
LINE = RGBColor(227, 220, 203)
BODY = RGBColor(51, 65, 85)
MUTED = RGBColor(120, 128, 145)
WHITE = RGBColor(255, 255, 255)
GREEN = RGBColor(47, 125, 79)
SERIF = "Georgia"
SANS = "Arial"

prs = Presentation()
prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)


def bg(slide, color):
    s = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    s.fill.solid()
    s.fill.fore_color.rgb = color
    s.line.fill.background()
    s.shadow.inherit = False
    return s


def tb(slide, l, t, w, h):
    box = slide.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    f = box.text_frame
    f.word_wrap = True
    return f


def para(f, text, size, color, bold=False, font=SANS, first=False, space_before=4, space_after=4):
    p = f.paragraphs[0] if first else f.add_paragraph()
    p.text = text
    p.font.size = Pt(size)
    p.font.bold = bold
    p.font.color.rgb = color
    p.font.name = font
    p.space_before = Pt(space_before)
    p.space_after = Pt(space_after)
    return p


def header(slide, eyebrow, title):
    bg(slide, PAPER)
    f = tb(slide, 0.75, 0.35, 11.9, 0.35)
    para(f, eyebrow.upper(), 10.5, BRASS, True, "Consolas", first=True, space_before=0)
    f2 = tb(slide, 0.75, 0.68, 11.9, 0.75)
    para(f2, title, 25, NAVY2, True, SERIF, first=True, space_before=0)
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.75), Inches(1.42), Inches(11.85), Pt(2.5))
    bar.fill.solid()
    bar.fill.fore_color.rgb = BRASS
    bar.line.fill.background()
    bar.shadow.inherit = False


def bullets(slide, l, t, w, h, items, size=14):
    f = tb(slide, l, t, w, h)
    for i, it in enumerate(items):
        p = para(f, "-  " + it, size, BODY, False, SANS, first=(i == 0), space_after=9)
        p.line_spacing = 1.15
    return f


def shot(slide, name, l, t, w, cropped=False):
    path = crop_top(name, cropped) if cropped else os.path.join(SHOTS, name)
    pic = slide.shapes.add_picture(path, Inches(l), Inches(t), width=Inches(w))
    fr = pic.line
    fr.color.rgb = LINE
    fr.width = Pt(1)
    return pic


def content(slide_no, eyebrow, title, items, image, image_w=6.3):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    header(s, eyebrow, title)
    bullets(s, 0.75, 1.75, 12.0 - image_w - 0.4, 4.9, items)
    shot(s, image, 12.6 - image_w, 1.75, image_w)
    return s

# ---------------- SLIDE 1: title ----------------
s = prs.slides.add_slide(prs.slide_layouts[6])
bg(s, NAVY)
f = tb(s, 1.0, 1.55, 11.3, 1.0)
para(f, "WOXSEN  |  SMART INDIA HACKATHON 2026", 13, BRASS, True, "Consolas", first=True, space_before=0)
f = tb(s, 1.0, 2.05, 11.3, 1.4)
para(f, "SIH Command Center", 46, WHITE, True, SERIF, first=True, space_before=0)
f = tb(s, 1.0, 3.30, 11.3, 0.8)
para(f, "One place to track every hackathon team, mentor and deliverable", 18, RGBColor(200, 210, 230), False, SANS, first=True, space_before=0)
bar = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.0), Inches(4.15), Inches(2.6), Pt(3))
bar.fill.solid(); bar.fill.fore_color.rgb = BRASS; bar.line.fill.background(); bar.shadow.inherit = False
f = tb(s, 1.0, 4.45, 11.3, 1.6)
para(f, "Team register  ·  Problem statements  ·  Mentor load  ·  Deliverable deadlines", 15, WHITE, False, SANS, first=True, space_before=0)
para(f, "Woxsen University  |  B.Tech CSE SEM 5  |  Full Stack Development (24TU05MJC1)", 13, RGBColor(150, 165, 195), False, SANS, space_before=12)
para(f, "Team of 4  —  Lead & Integration  ·  Frontend  ·  Backend  ·  QA & Documentation", 13, RGBColor(150, 165, 195), False, SANS)

# ---------------- SLIDE 2: overview ----------------
s = prs.slides.add_slide(prs.slide_layouts[6])
header(s, "What we built", "The whole hackathon register in one web app")
bullets(s, 0.75, 1.8, 5.6, 4.8, [
    "One web app for the SPOC — five screens, no installation, works offline",
    "Register a team and the rules check themselves, instantly",
    "Pick a problem statement from the official list — held by one team only",
    "See every mentor's load and assign a team in one click",
    "Track 4 deliverables per team with a live readiness score out of 100",
    "Export the whole register as Excel or a printable report in one click",
], size=14)
shot(s, "phase1-dashboard.png", 6.75, 1.8, 5.85)


# ---------------- SLIDE 3: team rules ----------------
s = prs.slides.add_slide(prs.slide_layouts[6])
header(s, "How we solve it - 1", "Team rules that check themselves")
bullets(s, 0.75, 1.8, 5.9, 4.9, [
    "Exactly 6 members required — a team of 5 is rejected instantly",
    "At least 1 female member — mandatory SIH rule, also rejected if missing",
    "A valid team is saved in one step and automatically gets its 4 deliverable slots",
    "The rule is checked before anything is stored, so bad entries cannot slip in",
    "The SPOC sees the exact reason in plain words, right on the screen",
], size=14)
shot(s, "phase3-team-step1.png", 6.95, 1.72, 5.65, 0.66)
shot(s, "phase4-team-step2.png", 6.95, 4.42, 5.65, 0.66)

# ---------------- SLIDE 4: problem statements ----------------
s = prs.slides.add_slide(prs.slide_layouts[6])
header(s, "How we solve it - 2", "Finding the right problem statement")
bullets(s, 0.75, 1.8, 6.1, 4.9, [
    "One click pulls the official list from sih.gov.in — 242 statements, no typing",
    "Search by the SIH number or a keyword — matching rows appear as you type",
    "Claim a statement; if another team already holds it, the app says who",
    "The SPOC can still allow a shared statement deliberately, when needed",
    "Works without internet too — paste the rows once and the list is saved",
], size=14)
shot(s, "phase5-ps-search.png", 7.15, 1.75, 5.45)


# ---------------- SLIDE 5: mentors ----------------
s = prs.slides.add_slide(prs.slide_layouts[6])
header(s, "How we solve it - 3", "Mentors without the guesswork")
bullets(s, 0.75, 1.8, 5.9, 4.9, [
    "A load table shows each mentor's current teams against their limit",
    "A full mentor is clearly marked — the app refuses to overload them",
    "One click assigns a team to whichever mentor is freest at that moment",
    "The dashboard updates immediately, so the SPOC always sees the truth",
    "No more asking around: fairness is visible in a single screen",
], size=14)
shot(s, "phase6-mentors.png", 6.95, 1.75, 5.65)

# ---------------- SLIDE 6: deliverables + readiness ----------------
s = prs.slides.add_slide(prs.slide_layouts[6])
header(s, "How we solve it - 4", "Progress you can actually see")
bullets(s, 0.75, 1.8, 5.9, 4.9, [
    "Four deliverables per team: GitHub repo, presentation, demo video, report",
    "Each item has a link and a status — submitted, needs revision, or approved",
    "Every approval adds 25% to that team's readiness score",
    "An invalid team or a missing mentor costs 25% — problems stay visible",
    "One click exports the register as Excel or a printable report for records",
], size=14)
shot(s, "phase7-deliverables.png", 6.95, 1.75, 5.65, 0.56)
shot(s, "phase8-printable-report.png", 6.95, 4.25, 4.7, 0.50)


# ---------------- SLIDE 7: proof ----------------
s = prs.slides.add_slide(prs.slide_layouts[6])
header(s, "What we checked", "How we proved it works")
bullets(s, 0.75, 1.8, 6.6, 4.9, [
    "105 automated checks cover every rule, screen and export",
    "Every rule was tested with wrong input first — the app blocks it",
    "Fast and stable: about 450 requests handled per second under load",
    "Tested on both phone-size and desktop screens — no broken layouts",
    "Security reviewed and hardened: fake entries cannot damage the app",
    "Runs on any college PC with no database — the demo can never fail",
], size=14)
shot(s, "phase9-mobile-dashboard.png", 8.45, 1.78, 1.95)

strip = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.15), Inches(6.20), Inches(4.4), Inches(0.95))
strip.fill.solid(); strip.fill.fore_color.rgb = NAVY2; strip.line.fill.background(); strip.shadow.inherit = False
f = tb(s, 8.35, 6.32, 4.0, 0.8)
para(f, "105 checks   ·   242 statements", 13.5, WHITE, True, "Consolas", first=True, space_before=0, space_after=2)
para(f, "450 req/sec  ·   phone + desktop", 13.5, RGBColor(200, 210, 230), True, "Consolas", space_before=0)

# ---------------- SLIDE 8: next + team ----------------
s = prs.slides.add_slide(prs.slide_layouts[6])
header(s, "What's next", "Future plan and who did what")

card = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.75), Inches(1.75), Inches(5.9), Inches(4.5))
card.fill.solid(); card.fill.fore_color.rgb = CARD; card.line.color.rgb = LINE; card.shadow.inherit = False
f = tb(s, 1.0, 1.95, 5.4, 0.5)
para(f, "Next steps", 17, NAVY2, True, SERIF, first=True, space_before=0)
bullets(s, 1.0, 2.55, 5.35, 3.6, [
    "Logins for SPOC, mentors and students — each sees only their own work",
    "Automatic reminders by email and WhatsApp as deadlines approach",
    "Online hosting plus a permanent database for the whole institute",
    "Direct verification of submitted GitHub links and files",
], size=13)

card2 = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.85), Inches(1.75), Inches(5.75), Inches(4.5))
card2.fill.solid(); card2.fill.fore_color.rgb = CARD; card2.line.color.rgb = LINE; card2.shadow.inherit = False
f = tb(s, 7.1, 1.95, 5.25, 0.5)
para(f, "Team of 4", 17, NAVY2, True, SERIF, first=True, space_before=0)
f = tb(s, 7.1, 2.55, 5.25, 3.6)
rows = [
    ("Lead  /  Integration", "overall build, wiring the screens to the rules, live demo"),
    ("Frontend", "the five screens, forms and phone-friendly layout"),
    ("Backend", "the rules, official list import, Excel and report exports"),
    ("QA  &  Documentation", "105 checks, security review, report and this presentation"),
]
for i, (role, what) in enumerate(rows):
    p = para(f, role, 13.5, NAVY2, True, SANS, first=(i == 0), space_before=0 if i == 0 else 12, space_after=2)
    para(f, what, 12, BODY, False, SANS, space_before=0, space_after=2)

f = tb(s, 0.75, 6.45, 11.85, 0.6)
para(f, "SIH Command Center  —  register it right, track it till the finale.", 15, BRASS, True, SERIF, first=True, space_before=0)

out = os.path.join(HERE, "SIH_Command_Center.pptx")
prs.save(out)
print("saved " + out + "  slides=" + str(len(prs.slides._sldIdLst)))

