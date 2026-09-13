# Team of 4 – Roles

1. You – Full-Stack / Integration Lead
   Owns repo, merges, SPOC dashboard + readiness logic, backend-frontend wiring,
   deployment + viva demo. Reviews all PRs.

2. Frontend Developer
   All pages + CSS, team registration form (6 members UI), PS catalog page,
   deliverable forms, dashboard tables/filters. No API logic, just fetch calls.

3. Backend Developer (API + Database) ← 4th role, assign this
   Express routes, Mongoose schemas (Team, PS, Mentor, Deliverable),
   validations (6 members / 1 female / duplicate PS), seed data, export CSV.
   Reason: you already cover integration, frontend covers UI, QA covers testing —
   the missing piece is someone owning the API + Mongo layer end-to-end.

4. QA + Tester + Documentation
   Test cases (valid/invalid team, mentor-less flag, deliverable flow),
   bug log, final report (report/), PPT + viva Q&A, screenshots.

## Working rule
Branches: main only, small commits per phase (professor checks history).
Each member commits with own name in message prefix, e.g. `[frontend] team form css`.
