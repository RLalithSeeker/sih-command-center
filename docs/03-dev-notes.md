# How each of us built it (for viva – in our own words)

## Full-stack (me) – integration + dashboard
I started with the SPOC dashboard because that's what the sir will click first.
I thought: if readiness % is wrong, whole project looks fake, so I kept the
formula dead simple – approved/4 minus penalty for bad team or no mentor.
I wired backend first with curl, then gave the JSON shape to frontend on
WhatsApp so he could build without waiting for me. Merging was just copy-paste
because we agreed the field names on day 1 (teamName, psId, mentorId).
Kept everything in one server.js so I can explain any line in viva.

## Frontend – why it looks like this
I picked Woxsen navy (#1a237e) + plain cards because SIH site itself is blue
and our SPOC demo is on projector – dark text on white is readable from back
bench. I skipped Tailwind – sir told us in class to show we know raw CSS, and
build step fails on college PCs anyway. All 5 pages share one style.css and
app.js so a change in nav doesn't mean editing everywhere. The team form shows
all 6 member rows at once (not add-more button) because the rule is exactly 6,
so why hide it. Known flaw: filters on dashboard reset after reload – I left it,
ran out of time, will say it in viva.

## Backend – API + DB calls I made
I kept Mongo optional (in-memory default) because none of us has Atlas credit
and review PC has no internet sometimes. Same validation on both paths so demo
never breaks. Team POST blocks invalid composition with 400 – I argued with
QA about this: he wanted to allow saving draft with 5 members, I said no,
PBL says "hard validation blocks submission", so block. Kept PS duplicate
check as warning + checkbox override because two teams genuinely wanted same
PS in our class. Mentor maxTeams default 3 – took from our dept (1 faculty
handles 2-3 SIH teams max). Export is CSV not Excel – Excel lib is heavy,
CSV opens in Excel anyway, sir accepted.

## QA – what I actually tested
I don't trust happy-path demos. I tried: 5 members (blocked), 6 males
(blocked – "female mandatory"), wrong PS id (400), assigning 4th team to same
mentor (blocked at 3), updating deliverable with typo status "approve"
(blocked). Also tested backend restart – seed comes back, so review demo is
safe even if sir refreshes. Found 2 real bugs: dashboard filter crashed when
mentor dropdown empty (fixed – default All), and CSV had no quotes so team
names with commas broke columns (fixed). Bug log is in 04-test-plan.md.
