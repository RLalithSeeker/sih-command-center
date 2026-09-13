# Viva Q&A (each member owns 3)

## Lead
1. Readiness formula? approved/4*100 minus 25 bad-team, 25 no-mentor. Why penalties? So SPOC sees risk, not just files.
2. Why memory + Mongo both? Review PC may be offline; MONGO_URI switches to real DB, same API.
3. Merge conflicts? Field names fixed day 1, main-only small commits.

## Frontend
1. Why no Tailwind/React? College PCs + projector; raw CSS proves fundamentals, zero build step.
2. Why wizard? Teachers enter data rarely; one box at a time prevents half-filled submits.
3. Filters reset on reload — known minor issue, would lift state to URL next.

## Backend
1. Why block invalid teams instead of drafts? PBL says hard validation; drafts hide SIH rule breaks.
2. Scrape vs paste? Scrape once (239 live), paste fallback offline. Dedup by sihId.
3. Seed-id bug? New ids collided with t1; start at 100; caught by 14-check script.

## QA
1. Edge cases? 5 members, 6 males, dupe PS, mentor overload, bad status — all blocked.
2. Composition rule source? SIH rule: 6 members, min 1 female — enforced server-side, not just UI.
3. What would you automate next? The 14-check script into pre-push hook.
