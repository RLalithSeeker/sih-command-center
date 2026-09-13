# QA Test Plan (by QA member – manual, on localhost)

API base: http://localhost:5000/api. Frontend: open frontend/index.html.

| # | Case | Steps | Expected | Result |
|---|------|-------|----------|--------|
| 1 | Register valid team | POST /teams, 6 members incl 1 female | 200 + 4 deliverables created | PASS |
| 2 | Only 5 members | POST /teams, 5 members | 400 "exactly 6" | PASS |
| 3 | 6 males, no female | POST /teams, all male | 400 "female member mandatory" | PASS |
| 4 | Empty team name | POST /teams, teamName "" | 400 "teamName required" | PASS |
| 5 | Select valid PS | POST /teams/t2/select-ps {psId: ps2} | psTitle updates | PASS |
| 6 | Duplicate PS | two teams pick ps1, no flag | 400 "Already taken" | PASS |
| 7 | Duplicate PS override | same + allowDuplicate true | 200 | PASS |
| 8 | Invalid PS id | psId "px" | 400 "invalid PS" | PASS |
| 9 | Assign mentor | POST assign-mentor {m1} | mentorName updates | PASS |
| 10 | Mentor overload | assign 4th team to m2 (max 2) | 400 "already has 2 teams" | PASS |
| 11 | Bad deliverable status | PUT {status: "approve"} | 400 "bad status" | PASS |
| 12 | Valid deliverable flow | submitted → approved, readiness rises | dashboard % updates | PASS |
| 13 | Filters | dashboard?status=pending | only <100% shown | PASS |
| 14 | Export CSV | GET /export.csv, open in Excel | 6 cols, quoted | PASS (fixed comma bug) |
| 15 | Restart persistence | kill + npm start, GET /teams | seed team t1 back | PASS (in-memory reseeds) |
| 16 | Frontend: register from teams.html | fill 6 rows, Register | "Saved", appears in list | PASS |
| 17 | Frontend: dashboard on projector | 1366x768, check table | no horizontal scroll | PASS |

Bugs found + fixed: (1) mentor filter crash on empty list – added default option;
(2) CSV comma break – wrapped fields in quotes. Left as-is: filter state not
saved on reload (minor, noted for viva).
