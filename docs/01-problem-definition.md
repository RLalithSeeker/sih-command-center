# Review 1 – Problem Definition & Objectives (5M)

## Problem
College SIH SPOC manages team registrations, problem-statement choices,
mentor allotment, deliverables (repo/PPT/video/report) in scattered sheets
and emails. Issues found after talking to seniors:
- invalid teams noticed late (not 6 members / no female member)
- 2 teams pick same PS and clash at internal hackathon
- mentor load uneven, some teams with no mentor till last week
- deliverables chased on WhatsApp, no single readiness view

## Objectives
1. One registration form that blocks invalid composition on submit.
2. PS catalog with category + organisation, one team per PS (configurable).
3. SPOC assigns mentor, sees mentor-wise load.
4. Per-team deliverable checklist with status + readiness %.
5. Filterable master dashboard + CSV export for nodal-centre records.

## Scope / non-goals
In scope: web app, single college, demo seed data, CSV export.
Out of scope: real email sending (we show reminder list instead), payment,
mobile app. Said clearly so viva doesn't ask for it.

## Users
- Team Lead (registers team, picks PS, uploads deliverable links)
- SPOC/Admin (mentors, approvals, dashboard, export)
- Mentor (views assigned teams – read-only in this version)
